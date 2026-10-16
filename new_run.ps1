<#
.SYNOPSIS
  Make a fresh, clean copy of the task for one agent run and open it in VS Code.
.EXAMPLE
  .\new_run.ps1 -Name baseline-gpt5-1 -Model "GPT-5"
.EXAMPLE
  .\new_run.ps1 -Name strict-claude-opus-1 -Model "Claude Opus 4.6"
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^(baseline|strict)(-[A-Za-z0-9._]+)*-[0-9]+$')]
    [string]$Name,

    # Free-text metadata. The one-command runner passes this label to the chosen CLI.
    [string]$Model = '',

    # Free-text label for the agent used; the one-command runner sets this.
    [string]$Runner = '',

    # Create the isolated task but leave CLI launch and result saving to the caller.
    [switch]$PrepareOnly
)

# Use an opaque folder name so the run label does not hint which prompt the agent got.
function Get-RunDir([string]$RunName) {
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($RunName))
    $hex = -join ($bytes[0..3] | ForEach-Object { $_.ToString('x2') })
    Join-Path $env:TEMP "ewallet-$hex"
}

# Keep run metadata outside the task folder so the agent cannot see it.
function Get-RunMetadataPath([string]$RunName) {
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($RunName))
    $hex = -join ($bytes[0..3] | ForEach-Object { $_.ToString('x2') })
    Join-Path $env:TEMP "ewallet-$hex.json"
}

# Anchor file paths to this repo even if PowerShell was opened in another folder.
$repo = $PSScriptRoot
$runDir = Get-RunDir $Name
$metadataPath = Get-RunMetadataPath $Name
$kind = $Name.Split('-')[0]
$promptFile = Join-Path $repo "prompts\$kind.md"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Install it from https://git-scm.com and reopen PowerShell." -ForegroundColor Red
    exit 1
}
if (Test-Path $runDir) {
    Write-Host "Run '$Name' already exists at $runDir" -ForegroundColor Red
    Write-Host "Use the next number instead (runs are never overwritten)."
    exit 1
}
$savedDiff = Join-Path $repo "runs\$Name.diff"
$savedNotes = Join-Path $repo "runs\$Name.md"
if ((Test-Path $savedDiff) -or (Test-Path $savedNotes)) {
    Write-Host "Run '$Name' already has saved evidence. Use the next number instead; runs are never overwritten." -ForegroundColor Red
    exit 1
}

# Give each run a clean task copy with only the files the agent is meant to see.
New-Item -ItemType Directory -Path $runDir | Out-Null
foreach ($item in 'SPEC.md', 'TASK.md', 'ewallet', 'tests') {
    Copy-Item -Path (Join-Path $repo $item) -Destination $runDir -Recurse
}
Get-ChildItem -Path $runDir -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force

$metadata = [ordered]@{
    name = $Name
    kind = $kind
    model = $Model
    runner = $Runner
    started = (Get-Date).ToString('o')
}
[System.IO.File]::WriteAllText(
    $metadataPath,
    ($metadata | ConvertTo-Json),
    (New-Object System.Text.UTF8Encoding $false)
)

Push-Location $runDir
try {
    # Keep a clean starting commit so save_run.ps1 can capture all later changes.
    git init -q -b main
    git config core.autocrlf true
    git config core.safecrlf false
    # Keep Python caches and local agent settings out of the saved diff.
    Set-Content -Path '.git\info\exclude' -Value @('__pycache__/', '*.pyc', '.claude/', '.codex/', '.opencode/') -Encoding Ascii
    git add -A
    git -c user.name=run -c user.email=run@localhost commit -q -m "initial"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "git commit failed in $runDir" -ForegroundColor Red
        exit 1
    }
}
finally {
    Pop-Location
}

if ($PrepareOnly) {
    Write-Host "Prepared isolated run folder for '$Name': $runDir"
    return $runDir
}

$copied = $false
try {
    # baseline-* uses baseline.md; strict-* uses strict.md.
    [System.IO.File]::ReadAllText($promptFile) | Set-Clipboard
    $copied = $true
}
catch { }

if (Get-Command code -ErrorAction SilentlyContinue) {
    code -n "$runDir"
}
else {
    Write-Host "VS Code 'code' command not found. Open this folder yourself: $runDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Run folder : $runDir"
if ($Model) { Write-Host "Model      : $Model" }
else { Write-Host "Model      : not set yet (use -Model or add it to the run notes)" -ForegroundColor Yellow }
if ($Runner) { Write-Host "Runner     : $Runner" }
if ($copied) {
    Write-Host "Prompt     : prompts\$kind.md  (already copied to your clipboard)" -ForegroundColor Green
}
else {
    Write-Host "Prompt     : prompts\$kind.md  (open it and copy all of it)" -ForegroundColor Green
}
Write-Host ""
Write-Host "Next:"
Write-Host "  1. In the NEW VS Code window, open your coding agent and start a fresh conversation."
Write-Host "  2. Paste the prompt (Ctrl+V) and send it. Do not type anything else."
Write-Host "  3. When the agent stops, copy its final message, then run here:"
Write-Host "       .\save_run.ps1 -Name $Name"
