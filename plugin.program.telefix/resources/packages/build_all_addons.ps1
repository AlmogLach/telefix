# Build all addon zips into this folder (run with Kodi CLOSED to avoid locked files)
$addonsRoot = "C:\Users\Almog\AppData\Roaming\Kodi\addons"
$packagesDir = "C:\Users\Almog\AppData\Roaming\Kodi\addons\plugin.program.telefix\resources\packages"
$exclude = @("plugin.program.telefix", "packages", "temp")

Get-ChildItem $addonsRoot -Directory | Where-Object { $exclude -notcontains $_.Name } | ForEach-Object {
    $name = $_.Name
    $zipPath = Join-Path $packagesDir "$name.zip"
    try {
        Compress-Archive -Path $_.FullName -DestinationPath $zipPath -CompressionLevel Optimal -Force
        Write-Output "OK: $name"
    } catch {
        Write-Output "SKIP: $name - $($_.Exception.Message)"
    }
}
Write-Output "Done. Zips in: $packagesDir"
