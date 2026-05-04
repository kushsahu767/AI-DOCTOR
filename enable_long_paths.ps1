# Enable Windows Long Path Support for Python packages
# Run this script as Administrator

Write-Host "Enabling Windows Long Path Support..." -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click on this script and select 'Run with PowerShell' as Administrator." -ForegroundColor Yellow
    exit 1
}

# Enable Long Path support in registry
try {
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
                     -Name "LongPathsEnabled" `
                     -Value 1 `
                     -PropertyType DWORD `
                     -Force | Out-Null
    Write-Host "✓ Long Path support enabled successfully!" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Failed to enable Long Path support" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "You can now install elevenlabs with: pip install elevenlabs" -ForegroundColor Green
