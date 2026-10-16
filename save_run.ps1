<#
.SYNOPSIS
  Save what the agent changed in a run folder to runs\<Name>.diff and
  create runs\<Name>.md, run both check suites, and add a row to RESULTS.md.
.EXAMPLE
  .\save_run.ps1 -Name baseline-gpt5-1
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^(baseline|strict)(-[A-Za-z0-9._]+)*-[0-9]+$')]
    [string]$Name,

    # Optional free-text overrides. Models are not restricted to a provider or list.
    [string]$Model = '',
    [string]$FinalMessage = ''
)

# Use the same folder-name recipe as new_run.ps1 to find that exact run.
function Get-RunDir([string]$RunName) {
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($RunName))
    $hex = -join ($bytes[0..3] | ForEach-Object { $_.ToString('x2') })
    Join-Path $env:TEMP "ewallet-$hex"
}

function Get-RunMetadataPath([string]$RunName) {
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $bytes = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($RunName))
    $hex = -join ($bytes[0..3] | ForEach-Object { $_.ToString('x2') })
    Join-Path $env:TEMP "ewallet-$hex.json"
}

function ConvertTo-TableCell([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return 'not recorded' }
    (($Value -replace '\|', '\|') -replace '[\r\n]+', ' ').Trim()
}

$repo = $PSScriptRoot
$runDir = Get-RunDir $Name
$metadataPath = Get-RunMetadataPath $Name
$kind = $Name.Split('-')[0]
$runsDir = Join-Path $repo 'runs'
$diffPath = Join-Path $runsDir "$Name.diff"
$mdPath = Join-Path $runsDir "$Name.md"

if (-not (Test-Path (Join-Path $runDir '.git'))) {
    Write-Host "No run folder for '$Name' (expected $runDir). Did you run .\new_run.ps1 -Name $Name ?" -ForegroundColor Red
    exit 1
}

if ((Test-Path $diffPath) -or (Test-Path $mdPath)) {
    Write-Host "Run '$Name' was already saved. Existing evidence was left untouched." -ForegroundColor Red
    Write-Host "Use a new run name for another attempt."
    exit 1
}

$metadata = $null
if (Test-Path $metadataPath) {
    try { $metadata = Get-Content -Raw -Path $metadataPath | ConvertFrom-Json } catch { }
}
$savedModel = if ($Model) { $Model } elseif ($metadata.model) { [string]$metadata.model } else { '' }
$started = if ($metadata.started) { ([datetime]$metadata.started).ToString('yyyy-MM-dd HH:mm:ss zzz') } else { (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz') }
if (-not $FinalMessage) {
    try {
        $clipboardText = Get-Clipboard -Raw
        $promptText = [System.IO.File]::ReadAllText((Join-Path $repo "prompts\$kind.md"))
        if ($clipboardText -and $clipboardText.Trim() -ne $promptText.Trim()) {
            $FinalMessage = $clipboardText.TrimEnd()
        }
    }
    catch { }
}

# Include new files and agent-created commits by comparing with the clean first commit.
git -C "$runDir" add -A
$root = (git -C "$runDir" rev-list --max-parents=0 HEAD | Select-Object -First 1)
git -C "$runDir" diff --cached $root "--output=$diffPath"
if ($LASTEXITCODE -ne 0) {
    Write-Host "git diff failed." -ForegroundColor Red
    exit 1
}
$changed = @(git -C "$runDir" diff --cached --name-status $root)
# The CI gate watches tests/, so record whether this run touched that folder.
$testsChanged = @($changed | Where-Object { $_ -match '\stests/' }).Count -gt 0

Write-Host "Saved diff : runs\$Name.diff"
if ($changed.Count -eq 0) {
    Write-Host "             (empty: the agent changed nothing)"
}
else {
    $changed | ForEach-Object { Write-Host "             $_" }
}
if ($testsChanged) {
    Write-Host "tests/ changed: YES" -ForegroundColor Yellow
}
else {
    Write-Host "tests/ changed: no"
}

if (Test-Path $mdPath) {
    # Never replace notes that may already contain the model, transcript, or results.
    Write-Host "runs\$Name.md already exists; left untouched." -ForegroundColor Yellow
}
else {
    if ($changed.Count -eq 0) { $fileList = '    (none)' }
    else { $fileList = ($changed | ForEach-Object { "    $_" }) -join "`n" }
    $testsText = if ($testsChanged) { 'yes' } else { 'no' }
    $lines = @(
        "# Run: $Name",
        "",
        "- Prompt: $kind (prompts/$kind.md)",
        "- Model: $(if ($savedModel) { $savedModel } else { 'not recorded' })",
        "- Started: $started",
        "- Label: needs-review (inspect the diff, then choose a label)",
        "- Diff: runs/$Name.diff",
        "- tests/ changed (auto): $testsText",
        "- Files changed (auto):",
        "",
        '```',
        $fileList,
        '```',
        "",
        "## Agent's final message (paste unedited)",
        "",
        "$(if ($FinalMessage) { $FinalMessage.TrimEnd() } else { '[Final message was not captured. Paste it here from the agent conversation.]' })",
        "",
        "## Automated check results",
        "",
        "Checks are run automatically by save_run.ps1 in a disposable copy.",
        "",
        '```',
        'VISIBLE: NOT RUN',
        'HELD-OUT: NOT RUN',
        '```',
        ""
    )
    [System.IO.File]::WriteAllText($mdPath, ($lines -join "`n"), (New-Object System.Text.UTF8Encoding $false))
    Write-Host "Created    : runs\$Name.md" -ForegroundColor Green
}

$resultPath = Join-Path $env:TEMP ("ewallet-$Name-results.txt")
$checker = Join-Path $repo 'check_heldout.ps1'
$powerShell = Get-Command powershell.exe -ErrorAction SilentlyContinue
if ($powerShell) {
    Write-Host ""
    Write-Host "Running visible and held-out checks in a temporary copy..."
    & $powerShell.Source -NoProfile -ExecutionPolicy Bypass -File $checker -DiffFile $diffPath -ResultPath $resultPath
    $checkExitCode = $LASTEXITCODE
}
else {
    $checkExitCode = 1
}

$visibleResult = 'NOT RUN'
$heldoutResult = 'NOT RUN'
if (Test-Path $resultPath) {
    $resultLines = Get-Content -Path $resultPath
    if ($resultLines.Count -ge 2) {
        $visibleResult = ($resultLines[0] -replace '^VISIBLE:\s*', '').Trim()
        $heldoutResult = ($resultLines[1] -replace '^HELD-OUT:\s*', '').Trim()
    }
    Remove-Item -Path $resultPath -Force -ErrorAction SilentlyContinue
}

$mdText = [System.IO.File]::ReadAllText($mdPath)
$mdText = $mdText -replace 'VISIBLE: NOT RUN\r?\nHELD-OUT: NOT RUN', "VISIBLE: $visibleResult`nHELD-OUT: $heldoutResult"
[System.IO.File]::WriteAllText($mdPath, $mdText, (New-Object System.Text.UTF8Encoding $false))

$resultsPath = Join-Path $runsDir 'RESULTS.md'
$resultsText = [System.IO.File]::ReadAllText($resultsPath)
if ($resultsText -match "(?m)^\|\s*$([regex]::Escape($Name))\s*\|") {
    Write-Host "RESULTS.md already has a row for '$Name'; it was left untouched." -ForegroundColor Yellow
}
else {
    $safeModel = ConvertTo-TableCell $savedModel
    $date = ConvertTo-TableCell (([datetime]$started).ToString('yyyy-MM-dd'))
    $testsText = if ($testsChanged) { 'yes' } else { 'no' }
    $row = "| $Name | $safeModel | $date | needs-review | $testsText | $visibleResult | $heldoutResult |"
    $separator = '|---|---|---|---|---|---|---|'
    $separatorIndex = $resultsText.IndexOf($separator)
    if ($separatorIndex -ge 0) {
        $insertAt = $separatorIndex + $separator.Length
        $resultsText = $resultsText.Insert($insertAt, "`n$row")
        [System.IO.File]::WriteAllText($resultsPath, $resultsText, (New-Object System.Text.UTF8Encoding $false))
        Write-Host "RESULTS.md: added $Name (label set to needs-review)."
    }
    else {
        Write-Host "Could not find the results table header; add this row manually:" -ForegroundColor Yellow
        Write-Host $row
    }
}

if ($checkExitCode -ne 0) {
    Write-Host "The check command did not complete cleanly; inspect runs\$Name.md and rerun .\check_heldout.ps1 if needed." -ForegroundColor Yellow
}
Write-Host "Review the diff and final message, then replace needs-review with the right label in both notes and RESULTS.md."
