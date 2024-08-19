Set-Location "$PSScriptRoot/.."

if (-not (Test-Path "public/examples")) {
    Expand-Archive -Path "public/examples.zip" -DestinationPath "public/examples"
}

$arguments = @("public/examples", "-t")
& $PSScriptRoot/start.ps1 $arguments