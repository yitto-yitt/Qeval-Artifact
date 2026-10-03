param(
    [string]$RunId = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ"),
    [string]$Python = "python",
    [string]$Models = "all",
    [string]$Tasks = "all",
    [string]$MainFrameworks = "cirq,pennylane,qpanda",
    [switch]$ExecuteCandidates,
    [switch]$SupplementaryQpanda2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $RepoRoot
try {
    & $Python "scripts/validate_inputs.py"

    if (-not $ExecuteCandidates) {
        Write-Host ""
        Write-Host "Input validation completed. Candidate execution was not requested."
        Write-Host "Re-run with -ExecuteCandidates only inside a disposable evaluation environment."
        return
    }

    foreach ($ClassId in 1, 2, 3) {
        & $Python "scripts/run_direct.py" `
            --class-id $ClassId `
            --models $Models `
            --tasks $Tasks `
            --run-id $RunId `
            --execute-candidates
    }

    foreach ($ClassId in 1, 2, 3) {
        & $Python "scripts/run_translation.py" `
            --class-id $ClassId `
            --models $Models `
            --frameworks $MainFrameworks `
            --tasks $Tasks `
            --run-id $RunId `
            --execute-candidates
    }

    & $Python "scripts/aggregate_results.py" --run-id $RunId

    if ($SupplementaryQpanda2) {
        $Qpanda2RunId = "$RunId-qpanda2"
        foreach ($ClassId in 1, 2, 3) {
            & $Python "scripts/run_translation.py" `
                --class-id $ClassId `
                --models $Models `
                --frameworks "qpanda2" `
                --tasks $Tasks `
                --run-id $Qpanda2RunId `
                --execute-candidates
        }
        & $Python "scripts/aggregate_results.py" `
            --run-id $Qpanda2RunId `
            --settings "translation"
    }
}
finally {
    Pop-Location
}
