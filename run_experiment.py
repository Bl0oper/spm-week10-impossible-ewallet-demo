#!/usr/bin/env python3
"""Run one isolated EWallet task with a local CLI or a browser-based model.

The normal entry point is simply ``python run_experiment.py``.  This file uses
only Python's standard library so teammates do not need to install packages.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
TASK_FILES = ("SPEC.md", "TASK.md", "ewallet", "tests")
PROMPT_DIR = ROOT / "prompts"
ID_PATTERN = re.compile(r"^(baseline|strict)-[a-z0-9-]+-\d{8}-\d{6}(?:-\d+)?$")
ALLOWED_PATCH_ROOTS = ("SPEC.md", "TASK.md", "ewallet/", "tests/")


class RunError(RuntimeError):
    """A problem the student can fix without reading a Python traceback."""


def ask_choice(title: str, choices: Sequence[tuple[str, str]]) -> str:
    """Show a numbered menu and keep asking until the choice is valid."""
    print(title)
    for number, (value, label) in enumerate(choices, 1):
        print(f"  {number}. {label}")
    while True:
        answer = input("Choose a number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            return choices[int(answer) - 1][0]
        print(f"Enter a number from 1 to {len(choices)}.")


def make_run_id(kind: str, runner: str, now: dt.datetime | None = None) -> str:
    """Make a readable run name; add a counter if two runs start the same second."""
    moment = now or dt.datetime.now().astimezone()
    base = f"{kind}-{runner}-{moment:%Y%m%d-%H%M%S}"
    candidate = base
    counter = 2
    while (RUNS / candidate).exists():
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RunError(f"Could not read run information in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RunError(f"Run information is not a JSON object: {path}")
    return value


def check_prerequisites() -> None:
    """Fail early with a useful message instead of a long Python traceback."""
    if sys.version_info < (3, 11):
        raise RunError("Python 3.11 or newer is required. Check with: python --version")
    if shutil.which("git") is None:
        raise RunError("Git was not found. Install Git, reopen your terminal, and try again.")


def run_git(args: Sequence[str], cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if check and result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise RunError(f"Git could not {args[0]} in the isolated run folder. {details}")
    return result


def create_workspace(destination: Path, source: Path | None = None, include_heldout: bool = False) -> Path:
    """Copy only task files into a fresh folder; no run metadata goes to the agent."""
    source = source or ROOT
    destination.mkdir(parents=True, exist_ok=False)
    items = list(TASK_FILES) + (["heldout"] if include_heldout else [])
    for item in items:
        source_path = source / item
        if not source_path.exists():
            raise RunError(f"Required task file is missing: {source_path}")
        target = destination / item
        if source_path.is_dir():
            shutil.copytree(source_path, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(source_path, target)

    # Keep Python bytecode and local agent configuration out of the experiment diff.
    exclude = destination / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text("__pycache__/\n*.pyc\n.claude/\n.codex/\n.opencode/\n.runner-final.md\n", encoding="utf-8")
    return destination


def initialize_git(workspace: Path) -> str:
    """Create a private baseline commit so every changed file can be captured."""
    run_git(["init", "-q", "-b", "main"], workspace)
    run_git(["config", "core.autocrlf", "true"], workspace)
    run_git(["config", "core.safecrlf", "false"], workspace)
    run_git(["add", "-A"], workspace)
    run_git(["-c", "user.name=experiment", "-c", "user.email=experiment@localhost", "commit", "-q", "-m", "task baseline"], workspace)
    return run_git(["rev-parse", "HEAD"], workspace).stdout.strip()


def save_workspace_diff(workspace: Path, base_commit: str) -> tuple[str, list[str]]:
    """Return a complete patch and the files the agent changed, including new files."""
    run_git(["add", "-A"], workspace)
    patch = run_git(["diff", base_commit, "--binary", "--no-ext-diff"], workspace).stdout
    names = run_git(["diff", "--name-only", base_commit], workspace).stdout.splitlines()
    return patch, names


def make_task_zip(path: Path, prompt: str, source: Path | None = None) -> None:
    """Package only the task and its prompt for upload to a web chat."""
    source = source or ROOT
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("PROMPT.md", prompt)
        for item in TASK_FILES:
            source_path = source / item
            if source_path.is_dir():
                for file_path in sorted(source_path.rglob("*")):
                    if file_path.is_file() and "__pycache__" not in file_path.parts:
                        archive.write(file_path, file_path.relative_to(source).as_posix())
            else:
                archive.write(source_path, item)


def validate_patch_paths(patch: str) -> None:
    """Reject a browser-returned patch that tries to write outside the task copy."""
    paths: set[str] = set()
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4 and parts[2].startswith("a/") and parts[3].startswith("b/"):
                paths.update((parts[2][2:], parts[3][2:]))
        elif line.startswith(("--- a/", "+++ b/")):
            paths.add(line[6:])

    if not paths and patch.strip():
        raise RunError("The patch does not look like a Git unified diff. Save the model's diff as a plain .patch file.")
    for name in paths:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise RunError(f"The patch contains an unsafe file path: {name}")
        if not any(name == root or name.startswith(root) for root in ALLOWED_PATCH_ROOTS):
            raise RunError(f"The patch changes a file outside the task: {name}")


def clean_patch_text(patch: str) -> str:
    """Accept a raw diff or one complete Markdown code fence around a diff."""
    value = patch.lstrip("\ufeff").strip()
    if value.startswith("```") and value.endswith("```"):
        first_newline = value.find("\n")
        if first_newline >= 0:
            value = value[first_newline + 1 : -3].strip()
    if value and not value.endswith("\n"):
        value += "\n"
    return value


def apply_patch(workspace: Path, patch: str) -> None:
    """Check a patch first, then apply it only inside a disposable task copy."""
    patch = clean_patch_text(patch)
    validate_patch_paths(patch)
    if not patch.strip():
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".patch", delete=False) as handle:
        patch_path = Path(handle.name)
        handle.write(patch)
    try:
        check = run_git(["apply", "--check", "--binary", str(patch_path)], workspace, check=False)
        if check.returncode != 0:
            details = (check.stderr or check.stdout).strip()
            raise RunError(f"Git could not apply that patch to the clean task copy. {details}")
        run_git(["apply", "--binary", str(patch_path)], workspace)
    finally:
        patch_path.unlink(missing_ok=True)


def run_suite(workspace: Path, suite: str) -> dict[str, Any]:
    """Run one suite with the same Python interpreter that started this tool."""
    command = [sys.executable, "-m", "unittest", "discover", "-s", suite]
    if suite == "tests":
        command.extend(["-t", "."])
    result = subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    return {
        "result": "PASS" if result.returncode == 0 else "FAIL",
        "exit_code": result.returncode,
        "output": (result.stdout + result.stderr).strip(),
    }


def check_patch(patch: str, source: Path | None = None) -> tuple[dict[str, Any], str]:
    """Apply the saved patch in a clean copy and run visible plus held-out tests."""
    source = source or ROOT
    with tempfile.TemporaryDirectory(prefix="ewallet-check-") as temp:
        workspace = Path(temp) / "task"
        create_workspace(workspace, source=source, include_heldout=True)
        initialize_git(workspace)
        apply_patch(workspace, patch)
        visible = run_suite(workspace, "tests")
        heldout = run_suite(workspace, "heldout")
    checks = {"visible": {k: v for k, v in visible.items() if k != "output"},
              "heldout": {k: v for k, v in heldout.items() if k != "output"}}
    output = "\n".join(
        (
            "--- Visible tests (tests/) ---",
            visible["output"] or "(no test output)",
            f"VISIBLE: {visible['result']}",
            "",
            "--- Held-out tests (heldout/) ---",
            heldout["output"] or "(no test output)",
            f"HELD-OUT: {heldout['result']}",
        )
    )
    return checks, output


def result_cell(value: Any) -> str:
    """Keep user-supplied labels readable in the generated Markdown table."""
    text = " ".join(str(value or "not recorded").split())
    return text.replace("|", "\\|")


def generate_results(runs_dir: Path | None = None) -> Path:
    """Rebuild a local summary from per-run manifests; the summary is not shared."""
    runs_dir = runs_dir or RUNS
    rows = []
    for manifest_path in sorted(runs_dir.glob("*/manifest.json")):
        try:
            manifest = read_json(manifest_path)
        except RunError:
            continue
        checks = manifest.get("checks") or {}
        visible = (checks.get("visible") or {}).get("result", "NOT RUN")
        heldout = (checks.get("heldout") or {}).get("result", "NOT RUN")
        rows.append(
            "| {run} | {runner} | {model} | {prompt} | {date} | {label} | {changed} | {visible} | {heldout} |".format(
                run=result_cell(manifest.get("run_id")),
                runner=result_cell(manifest.get("runner")),
                model=result_cell(manifest.get("model")),
                prompt=result_cell(manifest.get("prompt_kind")),
                date=result_cell(str(manifest.get("started", ""))[:10]),
                label=result_cell(manifest.get("label", "needs-review")),
                changed="yes" if manifest.get("tests_changed") else "no",
                visible=result_cell(visible),
                heldout=result_cell(heldout),
            )
        )
    header = [
        "# Run results (generated locally)",
        "",
        "This file is rebuilt from each run's `manifest.json`. It is ignored by Git so teammates do not edit one shared table.",
        "Open a run folder for its prompt, final answer, patch, and check output.",
        "",
        "| Run | Runner | Model | Prompt | Date | Label | tests/ changed? | VISIBLE | HELD-OUT |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    output = runs_dir / "RESULTS.md"
    output.write_text("\n".join(header + rows) + "\n", encoding="utf-8")
    return output


def save_artifacts(run_dir: Path, manifest: dict[str, Any], patch: str, final: str,
                   checks: dict[str, Any], check_output: str) -> None:
    """Write one self-contained run record before refreshing the local index."""
    run_dir.mkdir(parents=True, exist_ok=True)
    # Patch files cross between Windows and Unix, so keep their line endings stable.
    with (run_dir / "diff.patch").open("w", encoding="utf-8", newline="\n") as patch_file:
        patch_file.write(patch)
    (run_dir / "final.md").write_text(final.rstrip() + "\n", encoding="utf-8")
    (run_dir / "check-output.txt").write_text(check_output.rstrip() + "\n", encoding="utf-8")
    manifest["checks"] = checks
    manifest["tests_changed"] = any(name.startswith("tests/") for name in manifest.get("changed_files", []))
    write_json(run_dir / "manifest.json", manifest)
    generate_results()


def powershell_for_windows() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell.exe") or shutil.which("powershell")


def command_for_cli(executable: str, args: Sequence[str]) -> tuple[list[str], Path | None]:
    """Run Windows .cmd/.ps1 launchers through PowerShell with safe argument passing."""
    # A Python-file launcher is also useful for the offline fake CLI tests.
    if Path(executable).suffix.lower() == ".py":
        return [sys.executable, executable, *args], None
    if os.name != "nt" or Path(executable).suffix.lower() not in {".cmd", ".bat", ".ps1"}:
        return [executable, *args], None
    powershell = powershell_for_windows()
    if not powershell:
        raise RunError("PowerShell was not found, so the Windows CLI launcher cannot start.")
    wrapper_fd, wrapper_name = tempfile.mkstemp(prefix="ewallet-cli-", suffix=".ps1")
    os.close(wrapper_fd)
    wrapper = Path(wrapper_name)
    wrapper.write_text(
        "$ErrorActionPreference = 'Stop'\n"
        "$exe = $args[0]\n"
        "$cliArgs = @()\n"
        "if ($args.Count -gt 1) { $cliArgs = @($args | Select-Object -Skip 1) }\n"
        "& $exe @cliArgs\n"
        "exit $LASTEXITCODE\n",
        encoding="utf-8",
    )
    return [powershell, "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper), executable, *args], wrapper


def run_live(command: Sequence[str], cwd: Path, stdin_text: str | None = None) -> tuple[int, str]:
    """Show CLI output while it runs and return the same text for the run record."""
    output: list[str] = []
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        if stdin_text is not None and process.stdin is not None:
            try:
                process.stdin.write(stdin_text)
                process.stdin.close()
            except BrokenPipeError:
                pass
        if process.stdout is not None:
            for line in process.stdout:
                print(line, end="", flush=True)
                output.append(line)
        return process.wait(), "".join(output)
    except KeyboardInterrupt:
        # Stop the CLI and preserve whatever it changed before Ctrl+C.
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        raise
    finally:
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
        if process.stdout is not None:
            process.stdout.close()


def codex_preflight(executable: str, workspace: Path) -> tuple[bool, str]:
    """On Windows, prove the requested Codex sandbox can write before spending quota."""
    if os.name != "nt":
        return True, "skipped on this OS; Codex workspace-write sandbox will be used"
    probe_name = ".codex-write-check.txt"
    probe_path = workspace / probe_name
    args = [
        "-c", "windows.sandbox=mxc", "sandbox", "--include-managed-config",
        "--permission-profile", ":workspace", "--", "cmd.exe", "/d", "/c",
        f"echo CODEX_WORKSPACE_WRITE_OK>{probe_name}",
    ]
    command, wrapper = command_for_cli(executable, args)
    try:
        result = subprocess.run(command, cwd=workspace, capture_output=True, text=True, encoding="utf-8", errors="replace")
        passed = result.returncode == 0 and probe_path.is_file() and probe_path.read_text(encoding="utf-8").strip() == "CODEX_WORKSPACE_WRITE_OK"
        detail = "passed (MXC sandbox wrote in the isolated task folder)" if passed else (result.stderr or result.stdout or "write check did not create its file").strip()
        return passed, detail
    except OSError as exc:
        return False, str(exc)
    finally:
        probe_path.unlink(missing_ok=True)
        if wrapper:
            wrapper.unlink(missing_ok=True)


def local_cli_args(runner: str, model: str, workspace: Path, answer_path: Path,
                   prompt: str) -> tuple[list[str], str | None]:
    """Build the provider-specific command without restricting model names."""
    args: list[str] = []
    if runner == "codex":
        if os.name == "nt":
            args.extend(["-c", "windows.sandbox=mxc"])
        args.append("exec")
        if model:
            args.extend(["--model", model])
        args.extend([
            "--sandbox", "workspace-write", "--cd", str(workspace), "--ephemeral",
            "--ignore-user-config", "--output-last-message", str(answer_path), "-",
        ])
        return args, prompt

    if runner == "claude":
        args.extend(["--print"])
        if model:
            args.extend(["--model", model])
        args.extend([
            "--output-format", "text", "--permission-mode", "acceptEdits",
            "--no-session-persistence", "--safe-mode", prompt,
        ])
        return args, None
    raise RunError(f"Unknown local runner: {runner}")


def initial_manifest(run_id: str, kind: str, runner: str, model: str, started: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "runner": runner,
        "model": model or "CLI default (not pinned)",
        "prompt_kind": kind,
        "started": started,
        "status": "starting",
        "label": "needs-review",
        "agent_exit_code": None,
        "sandbox_preflight": "not run",
        "changed_files": [],
        "tests_changed": False,
        "checks": {"visible": {"result": "NOT RUN"}, "heldout": {"result": "NOT RUN"}},
    }


def run_local(run_id: str, kind: str, runner: str, model: str) -> Path:
    """Run Codex or Claude once in a temp task copy, then save reviewable evidence."""
    prompt_path = PROMPT_DIR / f"{kind}.md"
    if not prompt_path.is_file():
        raise RunError(f"Prompt file is missing: {prompt_path}")
    run_dir = RUNS / run_id
    if run_dir.exists():
        raise RunError(f"Run folder already exists: {run_dir}. Start a new run instead.")
    run_dir.mkdir(parents=True)
    prompt = prompt_path.read_text(encoding="utf-8")
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    started = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    manifest = initial_manifest(run_id, kind, runner, model, started)
    workspace = Path(tempfile.mkdtemp(prefix="ewallet-task-")) / "workspace"
    base_commit: str | None = None
    final = ""
    patch = ""
    exit_code: int | str = "not started"
    executable = shutil.which(runner)

    try:
        create_workspace(workspace, source=ROOT)
        base_commit = initialize_git(workspace)
        if not executable:
            raise RunError(f"The {runner} CLI was not found. Install and sign in, or choose the web/manual option.")
        if runner == "codex" and (os.environ.get("CODEX_SESSION_ID") or os.environ.get("CODEX_THREAD_ID")):
            raise RunError("A Codex session is already controlling this terminal. Open a separate terminal, then start a fresh run.")
        if runner == "codex":
            passed, detail = codex_preflight(executable, workspace)
            manifest["sandbox_preflight"] = detail if passed else f"failed: {detail}"
            if not passed:
                raise RunError(f"Codex was not started because its Windows write check failed: {detail}")
            print("Codex sandbox preflight: PASS (no model used)." if os.name == "nt" else "Using Codex workspace-write sandbox.")

        # Keep Codex's final-message file inside its allowed workspace sandbox.
        answer_path = workspace / ".runner-final.md"
        cli_model = "" if model == "CLI default (not pinned)" else model
        args, stdin_text = local_cli_args(runner, cli_model, workspace, answer_path, prompt)
        command, wrapper = command_for_cli(executable, args)
        print(f"Starting one {runner} run with model '{manifest['model']}'. The CLI uses your existing account and may use its quota.")
        interrupted = False
        try:
            try:
                exit_code, cli_output = run_live(command, workspace, stdin_text)
            except KeyboardInterrupt:
                interrupted = True
                exit_code = "interrupted"
                cli_output = ""
            manifest["agent_exit_code"] = exit_code
            if runner == "codex" and answer_path.is_file():
                final = answer_path.read_text(encoding="utf-8", errors="replace")
            elif runner == "claude":
                final = cli_output
            if not final.strip():
                if interrupted:
                    final = "The run was stopped with Ctrl+C. Any partial changes were saved for review; no complete final answer was captured."
                else:
                    final = f"No final answer was captured. {runner} exit code: {exit_code}. Review the CLI output shown above."
        finally:
            answer_path.unlink(missing_ok=True)
            if wrapper:
                wrapper.unlink(missing_ok=True)
        manifest["status"] = "interrupted" if interrupted else "completed"
    except KeyboardInterrupt:
        final = "The run was interrupted before it completed. Any task changes were saved for review."
        manifest["status"] = "not-started" if exit_code == "not started" else "interrupted"
        manifest["agent_exit_code"] = "interrupted"
    except (RunError, OSError, subprocess.SubprocessError) as exc:
        final = f"Run stopped before a complete model result was captured.\n\nReason: {exc}\n\nNo result label has been assigned."
        manifest["status"] = "not-started" if exit_code == "not started" else "failed"
        manifest["error"] = str(exc)
        print(str(exc), file=sys.stderr)

    if base_commit and workspace.exists():
        try:
            patch, changed = save_workspace_diff(workspace, base_commit)
            manifest["changed_files"] = changed
        except RunError as exc:
            manifest["error"] = f"{manifest.get('error', '')} Could not save the task diff: {exc}".strip()
            manifest["status"] = "failed"
            final += f"\n\nCould not capture a diff: {exc}"

    try:
        checks, output = check_patch(patch)
    except KeyboardInterrupt:
        checks = {"visible": {"result": "NOT RUN"}, "heldout": {"result": "NOT RUN"}}
        output = "Checks were interrupted by the user. Run the offline tests again when ready."
        manifest["check_error"] = "interrupted by user"
    except (RunError, OSError, subprocess.SubprocessError, subprocess.TimeoutExpired) as exc:
        checks = {"visible": {"result": "NOT RUN"}, "heldout": {"result": "NOT RUN"}}
        output = f"Checks could not start: {exc}"
        manifest["check_error"] = str(exc)
    save_artifacts(run_dir, manifest, patch, final, checks, output)
    print(f"\nSaved run: {run_dir.relative_to(ROOT)}")
    print(f"VISIBLE: {checks['visible']['result']}   HELD-OUT: {checks['heldout']['result']}")
    print("Open that run folder, inspect diff.patch and final.md, then set the label in manifest.json.")
    if workspace.parent.exists():
        shutil.rmtree(workspace.parent, ignore_errors=True)
    return run_dir


def manual_instructions(run_id: str, model: str) -> str:
    return textwrap.dedent(
        f"""\
        # Browser model run: {run_id}

        Model label: {model}

        1. Upload `task.zip` to the browser model. It contains only PROMPT.md, SPEC.md, TASK.md, ewallet/, and tests/.
        2. Paste the contents of `prompt.md` and send it once.
        3. Ask the model to return two plain files: `changes.patch` (a Git unified diff) and `final.md` (its complete final answer).
        4. Save those files on your computer. Do not edit the patch.
        5. From this project folder, import them with:

           python run_experiment.py import {run_id} --patch "PATH_TO_changes.patch" --answer "PATH_TO_final.md"

        The importer applies the patch in a disposable task copy, runs both test suites, and stores the result here.
        If your browser cannot upload ZIP files, extract task.zip and upload only the task files listed in step 1.
        """
    )


def prepare_manual(run_id: str, kind: str, model: str) -> Path:
    """Create an uploadable task bundle; no model or network request is made."""
    run_dir = RUNS / run_id
    if run_dir.exists():
        raise RunError(f"Run folder already exists: {run_dir}. Start a new run instead.")
    prompt = (PROMPT_DIR / f"{kind}.md").read_text(encoding="utf-8")
    run_dir.mkdir(parents=True)
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    instructions = manual_instructions(run_id, model)
    (run_dir / "manual-instructions.md").write_text(instructions, encoding="utf-8")
    make_task_zip(run_dir / "task.zip", prompt, source=ROOT)
    manifest = initial_manifest(run_id, kind, "web", model, dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    manifest["status"] = "awaiting-import"
    manifest["sandbox_preflight"] = "not applicable (browser model)"
    write_json(run_dir / "manifest.json", manifest)
    generate_results()
    print(f"\nPrepared: {run_dir.relative_to(ROOT)}")
    print("Upload task.zip, paste prompt.md, and follow manual-instructions.md.")
    print(f"When ready, run: python run_experiment.py import {run_id}")
    return run_dir


def import_manual(run_id: str, patch_file: str | None, answer_file: str | None) -> Path:
    """Import a web model's patch only after checking it against a clean task copy."""
    if not ID_PATTERN.fullmatch(run_id):
        raise RunError("That run ID does not look right. Copy it from the generated runs folder name.")
    run_dir = RUNS / run_id
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise RunError(f"Run not found: {run_id}. Start it first with python run_experiment.py.")
    manifest = read_json(manifest_path)
    if manifest.get("runner") != "web" or manifest.get("status") != "awaiting-import":
        raise RunError("This run is not waiting for a browser patch, or it has already been imported.")
    if not patch_file:
        patch_file = input("Path to changes.patch: ").strip().strip('"')
    if not answer_file:
        answer_file = input("Path to final.md: ").strip().strip('"')
    patch_path = Path(patch_file).expanduser().resolve()
    answer_path = Path(answer_file).expanduser().resolve()
    if not patch_path.is_file() or not answer_path.is_file():
        raise RunError("Could not find one of those files. Check the full paths and run the import command again.")
    patch = clean_patch_text(patch_path.read_text(encoding="utf-8", errors="replace"))
    answer = answer_path.read_text(encoding="utf-8", errors="replace")
    with tempfile.TemporaryDirectory(prefix="ewallet-import-") as temp:
        workspace = Path(temp) / "task"
        create_workspace(workspace, source=ROOT)
        base_commit = initialize_git(workspace)
        apply_patch(workspace, patch)
        patch, changed_names = save_workspace_diff(workspace, base_commit)
    checks, output = check_patch(patch)
    manifest["status"] = "completed"
    manifest["changed_files"] = changed_names
    manifest["imported_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    save_artifacts(run_dir, manifest, patch, answer, checks, output)
    print(f"\nImported run: {run_dir.relative_to(ROOT)}")
    print(f"VISIBLE: {checks['visible']['result']}   HELD-OUT: {checks['heldout']['result']}")
    print("Inspect diff.patch and final.md before changing the needs-review label in manifest.json.")
    return run_dir


def list_runs() -> None:
    manifests = sorted(RUNS.glob("*/manifest.json"))
    if not manifests:
        print("No runs yet. Start one with: python run_experiment.py")
        return
    for path in manifests:
        manifest = read_json(path)
        print(f"{manifest.get('run_id', path.parent.name)}  |  {manifest.get('runner')}  |  {manifest.get('model')}  |  {manifest.get('status')}")


def interactive_run(prompt_kind: str | None = None, runner: str | None = None,
                    model: str = "", name: str | None = None) -> Path:
    check_prerequisites()
    kind = prompt_kind or ask_choice("Which task prompt?", [("baseline", "Baseline: normal task prompt"), ("strict", "Strict: says never change tests")])
    selected_runner = runner or ask_choice(
        "How will you run the model?",
        [("codex", "Codex CLI on this computer"), ("claude", "Claude Code CLI on this computer"), ("web", "A model in a browser (ChatGPT, Claude, or another site)")],
    )
    if not model.strip():
        prompt = "Exact model ID (free text; blank uses the CLI default): " if selected_runner != "web" else "Model/site label (free text, e.g. ChatGPT GPT-5 or Claude Opus): "
        model = input(prompt).strip()
    if not model.strip():
        model = "CLI default (not pinned)" if selected_runner != "web" else "web model (not recorded)"
    run_id = name or make_run_id(kind, selected_runner)
    if not ID_PATTERN.fullmatch(run_id):
        raise RunError("Run names are generated automatically. Use baseline/strict, a runner, and a date/time in the ID.")
    if selected_runner == "web":
        return prepare_manual(run_id, kind, model)
    return run_local(run_id, kind, selected_runner, model)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guided, isolated AI coding-agent runs for the EWallet demo.")
    subparsers = parser.add_subparsers(dest="action")

    run_parser = subparsers.add_parser("run", help="run with the guided menu or pass choices directly")
    run_parser.add_argument("--prompt", choices=("baseline", "strict"), help="task prompt; asks if omitted")
    run_parser.add_argument("--runner", choices=("codex", "claude", "web"), help="local CLI or browser model; asks if omitted")
    run_parser.add_argument("--model", default="", help="free-text model ID/label; no allow-list")
    run_parser.add_argument("--name", help="optional run ID; normally generated automatically")

    import_parser = subparsers.add_parser("import", help="save a browser model's patch and run the checks")
    import_parser.add_argument("run_id")
    import_parser.add_argument("--patch", help="path to the returned unified diff")
    import_parser.add_argument("--answer", help="path to the model's complete final answer")

    subparsers.add_parser("results", help="rebuild the ignored local runs/RESULTS.md summary")
    subparsers.add_parser("list", help="list saved runs")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.action in (None, "run"):
            if args.action == "run":
                interactive_run(args.prompt, args.runner, args.model, args.name)
            else:
                interactive_run()
        elif args.action == "import":
            check_prerequisites()
            import_manual(args.run_id, args.patch, args.answer)
        elif args.action == "results":
            output = generate_results()
            print(f"Updated {output.relative_to(ROOT)} (local file; not shared with Git).")
        elif args.action == "list":
            list_runs()
        return 0
    except (RunError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print(f"\nCould not finish that step: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
