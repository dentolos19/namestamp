Set-Location -Path $PSScriptRoot
if (-not (Test-Path -Path "public/examples")) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory("public/examples.zip", "public/examples")
}
Start-Process -FilePath "start.bat" -ArgumentList "-d", "public/examples"