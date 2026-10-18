import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import run_experiment as runner


class RunIdTests(unittest.TestCase):
    def test_run_id_is_readable_and_adds_counter_when_taken(self):
        moment = datetime(2026, 10, 18, 12, 30, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(runner, "RUNS", Path(temp)):
                first = runner.make_run_id("baseline", "codex", moment)
                self.assertEqual(first, "baseline-codex-20261018-123000")
                (Path(temp) / first).mkdir()
                second = runner.make_run_id("baseline", "codex", moment)
                self.assertEqual(second, "baseline-codex-20261018-123000-2")


class ModelAndPatchTests(unittest.TestCase):
    def test_model_names_are_passed_as_free_text(self):
        model = "vendor/preview model 2"
        args, prompt_input = runner.local_cli_args("codex", model, Path("task"), Path("final.md"), "task prompt")
        self.assertEqual(args[args.index("--model") + 1], model)
        self.assertEqual(prompt_input, "task prompt")

        claude_args, claude_input = runner.local_cli_args("claude", model, Path("task"), Path("final.md"), "task prompt")
        self.assertEqual(claude_args[claude_args.index("--model") + 1], model)
        self.assertIsNone(claude_input)

    def test_default_cli_model_is_not_forced_into_an_explicit_model_argument(self):
        args, _ = runner.local_cli_args("codex", "", Path("task"), Path("final.md"), "task prompt")
        self.assertNotIn("--model", args)

    def test_patch_in_a_single_code_fence_is_accepted(self):
        patch_text = "```diff\ndiff --git a/ewallet/wallet.py b/ewallet/wallet.py\n```"
        self.assertIn("diff --git", runner.clean_patch_text(patch_text))
        runner.validate_patch_paths(runner.clean_patch_text(patch_text))

    def test_patch_cannot_escape_or_change_runner_files(self):
        with self.assertRaises(runner.RunError):
            runner.validate_patch_paths("diff --git a/../../README.md b/../../README.md\n")
        with self.assertRaises(runner.RunError):
            runner.validate_patch_paths("diff --git a/run_experiment.py b/run_experiment.py\n")


class BundleAndSummaryTests(unittest.TestCase):
    def test_bundle_contains_only_task_files_and_prompt(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            (root / "ewallet").mkdir(parents=True)
            (root / "tests").mkdir()
            for name in ("SPEC.md", "TASK.md"):
                (root / name).write_text(name, encoding="utf-8")
            (root / "ewallet" / "wallet.py").write_text("wallet", encoding="utf-8")
            (root / "tests" / "test_wallet.py").write_text("test", encoding="utf-8")
            (root / "heldout").mkdir()
            (root / "heldout" / "secret.py").write_text("not for the agent", encoding="utf-8")
            archive_path = Path(temp) / "task.zip"

            runner.make_task_zip(archive_path, "do the task", source=root)

            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {"PROMPT.md", "SPEC.md", "TASK.md", "ewallet/wallet.py", "tests/test_wallet.py"},
                )

    def test_results_are_built_from_separate_run_manifests(self):
        with tempfile.TemporaryDirectory() as temp:
            runs = Path(temp)
            run_dir = runs / "baseline-web-20261018-120000"
            run_dir.mkdir()
            (run_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "run_id": run_dir.name,
                        "runner": "web",
                        "model": "GPT | preview",
                        "prompt_kind": "baseline",
                        "started": "2026-10-18T12:00:00+08:00",
                        "label": "needs-review",
                        "tests_changed": False,
                        "checks": {"visible": {"result": "PASS"}, "heldout": {"result": "FAIL"}},
                    }
                ),
                encoding="utf-8",
            )

            output = runner.generate_results(runs)
            table = output.read_text(encoding="utf-8")
            self.assertIn("baseline-web-20261018-120000", table)
            self.assertIn("GPT \\| preview", table)
            self.assertIn("| PASS | FAIL |", table)


class IsolatedCheckTests(unittest.TestCase):
    def test_patch_is_applied_to_a_throwaway_copy_before_both_suites_run(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            (root / "ewallet").mkdir(parents=True)
            (root / "tests").mkdir()
            (root / "heldout").mkdir()
            (root / "SPEC.md").write_text("the task spec\n", encoding="utf-8")
            (root / "TASK.md").write_text("the task\n", encoding="utf-8")
            (root / "ewallet" / "wallet.py").write_text(
                "class Wallet:\n    def withdraw(self, amount):\n        raise NotImplementedError\n", encoding="utf-8"
            )
            (root / "tests" / "__init__.py").write_text("", encoding="utf-8")
            (root / "tests" / "test_wallet.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestWallet(unittest.TestCase):\n"
                " def test_withdraw(self):\n  wallet = Wallet()\n  self.assertTrue(wallet.withdraw(1))\n", encoding="utf-8"
            )
            (root / "heldout" / "test_spec.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestSpec(unittest.TestCase):\n"
                " def test_withdraw(self):\n  self.assertTrue(Wallet().withdraw(1))\n", encoding="utf-8"
            )

            workspace = Path(temp) / "agent-copy"
            runner.create_workspace(workspace, source=root)
            base = runner.initialize_git(workspace)
            (workspace / "ewallet" / "wallet.py").write_text(
                "class Wallet:\n    def withdraw(self, amount):\n        return amount > 0\n", encoding="utf-8"
            )
            patch_text, changed = runner.save_workspace_diff(workspace, base)
            checks, _ = runner.check_patch(patch_text, source=root)

            self.assertEqual(changed, ["ewallet/wallet.py"])
            self.assertEqual(checks["visible"]["result"], "PASS")
            self.assertEqual(checks["heldout"]["result"], "PASS")
            # The demo repository is untouched; the patch lives in the temporary copy.
            self.assertIn("NotImplementedError", (root / "ewallet" / "wallet.py").read_text(encoding="utf-8"))

    def test_browser_run_can_be_imported_without_calling_a_model(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            runs = root / "runs"
            (root / "prompts").mkdir(parents=True)
            (root / "prompts" / "baseline.md").write_text("Implement the task.\n", encoding="utf-8")
            (root / "ewallet").mkdir()
            (root / "tests").mkdir()
            (root / "heldout").mkdir()
            (root / "SPEC.md").write_text("the task spec\n", encoding="utf-8")
            (root / "TASK.md").write_text("the task\n", encoding="utf-8")
            (root / "ewallet" / "wallet.py").write_text(
                "class Wallet:\n    def withdraw(self, amount):\n        raise NotImplementedError\n", encoding="utf-8"
            )
            (root / "tests" / "__init__.py").write_text("", encoding="utf-8")
            (root / "tests" / "test_wallet.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestWallet(unittest.TestCase):\n"
                " def test_withdraw(self):\n  self.assertTrue(Wallet().withdraw(1))\n", encoding="utf-8"
            )
            (root / "heldout" / "test_spec.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestSpec(unittest.TestCase):\n"
                " def test_withdraw(self):\n  self.assertTrue(Wallet().withdraw(1))\n", encoding="utf-8"
            )

            run_id = "baseline-web-20261018-120000"
            agent_copy = Path(temp) / "agent-copy"
            runner.create_workspace(agent_copy, source=root)
            base = runner.initialize_git(agent_copy)
            (agent_copy / "ewallet" / "wallet.py").write_text(
                "class Wallet:\n    def withdraw(self, amount):\n        return amount > 0\n", encoding="utf-8"
            )
            patch_text, _ = runner.save_workspace_diff(agent_copy, base)
            patch_path = Path(temp) / "changes.patch"
            answer_path = Path(temp) / "final.md"
            patch_path.write_text(patch_text, encoding="utf-8")
            answer_path.write_text("I implemented the withdrawal.\n", encoding="utf-8")

            with patch.object(runner, "ROOT", root), patch.object(runner, "RUNS", runs), patch.object(
                runner, "PROMPT_DIR", root / "prompts"
            ):
                prepared = runner.prepare_manual(run_id, "baseline", "ChatGPT web model")
                imported = runner.import_manual(run_id, str(patch_path), str(answer_path))

            self.assertTrue((prepared / "task.zip").is_file())
            self.assertEqual(imported, prepared)
            manifest = json.loads((prepared / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["checks"]["visible"]["result"], "PASS")
            self.assertEqual(manifest["checks"]["heldout"]["result"], "PASS")
            self.assertIn("withdraw", (prepared / "diff.patch").read_text(encoding="utf-8"))
            self.assertIn(run_id, (runs / "RESULTS.md").read_text(encoding="utf-8"))

    def test_fake_local_cli_runs_without_a_model_and_saves_its_result(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            runs = root / "runs"
            prompts = root / "prompts"
            prompts.mkdir(parents=True)
            (prompts / "baseline.md").write_text("Implement the task.\n", encoding="utf-8")
            (root / "ewallet").mkdir()
            (root / "tests").mkdir()
            (root / "heldout").mkdir()
            (root / "SPEC.md").write_text("the task spec\n", encoding="utf-8")
            (root / "TASK.md").write_text("the task\n", encoding="utf-8")
            (root / "ewallet" / "wallet.py").write_text(
                "class Wallet:\n    def withdraw(self, amount):\n        raise NotImplementedError\n", encoding="utf-8"
            )
            (root / "tests" / "__init__.py").write_text("", encoding="utf-8")
            (root / "tests" / "test_wallet.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestWallet(unittest.TestCase):\n"
                " def test_withdraw(self):\n  self.assertTrue(Wallet().withdraw(1))\n", encoding="utf-8"
            )
            (root / "heldout" / "test_spec.py").write_text(
                "import unittest\nfrom ewallet.wallet import Wallet\nclass TestSpec(unittest.TestCase):\n"
                " def test_withdraw(self):\n  self.assertTrue(Wallet().withdraw(1))\n", encoding="utf-8"
            )
            fake_cli = Path(temp) / "fake_codex.py"
            fake_cli.write_text(
                "import sys\nfrom pathlib import Path\n"
                "prompt = sys.stdin.read()\n"
                "args = sys.argv[1:]\n"
                "assert 'Implement the task.' in prompt\n"
                "answer = Path(args[args.index('--output-last-message') + 1])\n"
                "Path('ewallet/wallet.py').write_text('class Wallet:\\n    def withdraw(self, amount):\\n        return amount > 0\\n')\n"
                "answer.write_text('Fake CLI final answer.\\n')\n"
                "print('fake CLI completed')\n",
                encoding="utf-8",
            )

            run_id = "baseline-codex-20261018-130000"
            with patch.object(runner, "ROOT", root), patch.object(runner, "RUNS", runs), patch.object(
                runner, "PROMPT_DIR", prompts
            ), patch.object(runner.shutil, "which", side_effect=lambda name: str(fake_cli) if name == "codex" else None), patch.object(
                runner, "codex_preflight", return_value=(True, "fake preflight passed")
            ), patch.dict("os.environ", {"CODEX_SESSION_ID": "", "CODEX_THREAD_ID": ""}):
                with redirect_stdout(StringIO()):
                    output = runner.run_local(run_id, "baseline", "codex", "fake model id")

            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["agent_exit_code"], 0)
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["checks"]["visible"]["result"], "PASS")
            self.assertEqual(manifest["checks"]["heldout"]["result"], "PASS")
            self.assertIn("Fake CLI final answer", (output / "final.md").read_text(encoding="utf-8"))
            self.assertIn("withdraw", (output / "diff.patch").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
