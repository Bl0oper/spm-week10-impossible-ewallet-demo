<#
.SYNOPSIS
  Apply a diff to a throwaway copy of this repo, then run the visible tests
  (tests/) and the held-out tests (heldout/).
.EXAMPLE
  .\check_heldout.ps1 examples\special_case.diff
.EXAMPLE
  .\check_heldout.ps1 runs\baseline-1.diff
.EXAMPLE
  .\check_heldout.ps1 runs\baseline-1.diff -ResultPath $env:TEMP\ewallet-results.txt
#>
param(
    [Parameter(Position = 0)]
    [string]$DiffFile,

    # Optional two-line result file used by save_run.ps1 to fill run notes.
    [string]$ResultPath
)

$repo = $PSScriptRoot

if (Get-Command py -ErrorAction SilentlyContinue) { $py = 'py' }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = 'python' }
else {
    Write-Host "Python not found. Install Python 3.11+ from https://www.python.org and reopen PowerShell." -ForegroundColor Red
    exit 1
}

$diffFull = $null
if ($DiffFile) {
    if (-not (Test-Path $DiffFile)) {
        Write-Host "Diff file not found: $DiffFile" -ForegroundColor Red
        exit 1
    }
    $diffFull = (Resolve-Path $DiffFile).Path
}

$work = Join-Path $env:TEMP ("ewallet-check-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $work | Out-Null
# Apply and test changes in a disposable copy, never in the presentation repo itself.
foreach ($item in 'SPEC.md', 'TASK.md', 'ewallet', 'tests', 'heldout') {
    Copy-Item -Path (Join-Path $repo $item) -Destination $work -Recurse
}
Get-ChildItem -Path $work -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force

Push-Location $work
try {
    git init -q -b main
    git config core.autocrlf true
    git config core.safecrlf false
    git add -A
    git -c user.name=check -c user.email=check@localhost commit -q -m "base"

    if ($diffFull) {
        Write-Host "Applying $DiffFile"
        git apply --whitespace=nowarn "$diffFull"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Could not apply $DiffFile to this repo." -ForegroundColor Red
            exit 1
        }
    }
    else {
        Write-Host "No diff given: checking the repo as it is."
    }

    Write-Host ""
    Write-Host "--- Visible tests (tests/) ---"
    cmd /c "$py -m unittest discover -s tests -t . 2>&1"
    $visiblePass = ($LASTEXITCODE -eq 0)

    Write-Host ""
    # Run the owner-only checks separately so the two outcomes are easy to compare.
    Write-Host "--- Held-out tests (heldout/) ---"
    cmd /c "$py -m unittest discover -s heldout 2>&1"
    $heldoutPass = ($LASTEXITCODE -eq 0)
}
finally {
    Pop-Location
    Remove-Item -Path $work -Recurse -Force -ErrorAction SilentlyContinue
}

function Write-Result([string]$Label, [bool]$Pass) {
    if ($Pass) { Write-Host ($Label + 'PASS') -ForegroundColor Green }
    else { Write-Host ($Label + 'FAIL') -ForegroundColor Red }
}

Write-Host ""
# A zero exit code means both checks completed; use the printed PASS/FAIL lines as results.
Write-Result 'VISIBLE:  ' $visiblePass
Write-Result 'HELD-OUT: ' $heldoutPass
if ($ResultPath) {
    $visibleResult = if ($visiblePass) { 'PASS' } else { 'FAIL' }
    $heldoutResult = if ($heldoutPass) { 'PASS' } else { 'FAIL' }
    [System.IO.File]::WriteAllLines(
        $ResultPath,
        @("VISIBLE: $visibleResult", "HELD-OUT: $heldoutResult"),
        (New-Object System.Text.UTF8Encoding $false)
    )
}
exit 0
