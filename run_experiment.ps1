<#
.SYNOPSIS
  Run one isolated task with the Codex or Claude Code CLI, then save and check it.
.EXAMPLE
  .\run_experiment.ps1 -Name baseline-gpt-1 -Runner codex -Model "your GPT model ID"
.EXAMPLE
  .\run_experiment.ps1 -Name baseline-claude-1 -Runner claude -Model "your Claude model ID"
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^(baseline|strict)(-[A-Za-z0-9._]+)*-[0-9]+$')]
    [string]$Name,

    # This selects the installed CLI. It does not limit the model name.
    [Parameter(Mandatory = $true)]
    [ValidateSet('codex', 'claude')]
    [string]$Runner,

    # Passed directly to the selected CLI. The CLI checks whether it supports it.
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Model
)

function Get-RunDir([string]$RunName) {
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($RunName))
    $hex = -join ($bytes[0..3] | ForEach-Object { $_.ToString('x2') })
    Join-Path $env:TEMP "ewallet-$hex"
}

# Node-based CLIs on Windows can expose both a .cmd launcher and an extensionless
# shim. Choose one real launcher explicitly so PowerShell does not pass both as
# one malformed command name.
$runnerCommand = Get-Command -Name $Runner -CommandType Application -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -match '\.(cmd|bat|exe)$' } |
    Select-Object -First 1
if (-not $runnerCommand) {
    Write-Host "The '$Runner' CLI was not found. Install and sign in to it, or use the manual steps in README.md." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python was not found. Install Python 3.11+ before starting a model run." -ForegroundColor Red
    exit 1
}

$kind = $Name.Split('-')[0]
$promptPath = Join-Path $PSScriptRoot "prompts\$kind.md"
if (-not (Test-Path $promptPath)) {
    Write-Host "Prompt file not found: $promptPath" -ForegroundColor Red
    exit 1
}

$runDir = Get-RunDir $Name
if (Test-Path $runDir) {
    Write-Host "Run '$Name' already exists. Use a new name; saved runs are never overwritten." -ForegroundColor Red
    exit 1
}
$savedDiff = Join-Path $PSScriptRoot "runs\$Name.diff"
$savedNotes = Join-Path $PSScriptRoot "runs\$Name.md"
if ((Test-Path $savedDiff) -or (Test-Path $savedNotes)) {
    Write-Host "Run '$Name' already has saved evidence. Use a new name; saved runs are never overwritten." -ForegroundColor Red
    exit 1
}

$answerPath = Join-Path $env:TEMP "$Name-agent-final.md"
if (Test-Path $answerPath) {
    Write-Host "Temporary answer file already exists: $answerPath. Review or move it, then try a new run name." -ForegroundColor Red
    exit 1
}

if (-not $PSCmdlet.ShouldProcess("run '$Name' with $Runner and model '$Model'", 'Create an isolated copy, invoke the model once, then save and check the result')) {
    return
}

# Avoid launching a second Codex inside a Codex-controlled shell. The parent
# session can enforce read-only policy even when this script requests writes.
if ($Runner -eq 'codex' -and ($env:CODEX_SESSION_ID -or $env:CODEX_THREAD_ID)) {
    Write-Host "This PowerShell is inside a Codex session, so a nested Codex run may inherit its read-only policy." -ForegroundColor Yellow
    Write-Host "Open a separate PowerShell window from the Windows Start menu and run this command there. No model was started."
    exit 1
}

# PrepareOnly skips VS Code and the clipboard; the selected CLI receives the prompt directly.
$preparedOutput = @(& (Join-Path $PSScriptRoot 'new_run.ps1') -Name $Name -Model $Model -Runner $Runner -PrepareOnly)
if ($preparedOutput.Count -eq 0) {
    Write-Host "Could not prepare the isolated run. No model was started." -ForegroundColor Red
    exit 1
}
$runDir = [string]$preparedOutput[$preparedOutput.Count - 1]
if (-not (Test-Path (Join-Path $runDir '.git'))) {
    Write-Host "The isolated run folder is incomplete: $runDir" -ForegroundColor Red
    exit 1
}

$promptText = [System.IO.File]::ReadAllText($promptPath)
$agentExitCode = 1
$agentFailure = ''
Write-Host "Starting one $Runner run with model label '$Model'. This uses the CLI's existing account and may use its quota."

Push-Location $runDir
try {
    if ($Runner -eq 'codex') {
        $codexArgs = @(
            'exec',
            '--model', $Model,
            '--sandbox', 'workspace-write',
            '--cd', $runDir,
            '--ephemeral',
            '--ignore-user-config',
            '--output-last-message', $answerPath,
            '-'
        )
        $promptText | & $runnerCommand.Path @codexArgs
        $agentExitCode = $LASTEXITCODE
    }
    else {
        # Safe mode removes project/user customizations; acceptEdits allows file edits without bypassing CLI protections.
        $claudeArgs = @(
            '--print',
            '--model', $Model,
            '--output-format', 'text',
            '--permission-mode', 'acceptEdits',
            '--no-session-persistence',
            '--safe-mode',
            $promptText
        )
        $agentLines = & $runnerCommand.Path @claudeArgs
        $agentExitCode = $LASTEXITCODE
        $agentText = ($agentLines | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
        if (-not [string]::IsNullOrWhiteSpace($agentText)) {
            [System.IO.File]::WriteAllText($answerPath, $agentText, (New-Object System.Text.UTF8Encoding $false))
        }
    }
}
catch {
    $agentFailure = "The $Runner CLI could not finish: $($_.Exception.Message)"
    Write-Host $agentFailure -ForegroundColor Yellow
    $agentExitCode = 1
}
finally {
    Pop-Location
}

$answerMissing = -not (Test-Path $answerPath)
$answerEmpty = $false
if (-not $answerMissing) {
    $answerEmpty = [string]::IsNullOrWhiteSpace([System.IO.File]::ReadAllText($answerPath))
}
if ($answerMissing -or $answerEmpty) {
    if ($agentFailure) {
        $message = "$agentFailure`nCLI exit code: $agentExitCode. No final model message was captured."
    }
    else {
        $message = "No final message was captured from $Runner. CLI exit code: $agentExitCode."
    }
    [System.IO.File]::WriteAllText($answerPath, $message, (New-Object System.Text.UTF8Encoding $false))
}

# save_run stores the final message, diff, run label, and both check results.
& (Join-Path $PSScriptRoot 'save_run.ps1') -Name $Name -Runner $Runner -Model $Model -FinalMessageFile $answerPath -AgentExitCode ([string]$agentExitCode)

$notesPath = Join-Path $PSScriptRoot "runs\$Name.md"
if (-not (Test-Path $notesPath)) {
    Write-Host "The run folder is still available at $runDir, but the result notes were not saved." -ForegroundColor Red
    Write-Host "Keep the answer file at $answerPath for recovery."
    exit 1
}

$diffPath = Join-Path $PSScriptRoot "runs\$Name.diff"
$resultsPath = Join-Path $PSScriptRoot 'runs\RESULTS.md'
$resultsText = [System.IO.File]::ReadAllText($resultsPath)
$rowPattern = "(?m)^\|\s*$([regex]::Escape($Name))\s*\|"
if (-not (Test-Path $diffPath) -or $resultsText -notmatch $rowPattern) {
    Write-Host "The run folder is still available at $runDir, but the diff or results row is missing." -ForegroundColor Red
    Write-Host "Keep the answer file at $answerPath for recovery."
    exit 1
}

Remove-Item -LiteralPath $answerPath -Force -ErrorAction SilentlyContinue
Write-Host ""
Write-Host "Saved: runs\$Name.diff, runs\$Name.md, and a row in runs\RESULTS.md" -ForegroundColor Green
Write-Host "CLI exit code: $agentExitCode. Review the diff and notes before changing needs-review."
