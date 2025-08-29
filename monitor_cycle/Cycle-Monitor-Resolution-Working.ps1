# Cycle-Monitor-Resolution-Working.ps1
# Working version that cycles monitor resolutions with user-friendly output
# Usage: Run with default settings, or pass -DisplayName '\\.\DISPLAY2'

param(
    [string]$DisplayName = $null
)

# ====== EDIT THESE 3 MODES ======
$Modes = @(
    @{W=1280; H=960; F=144},
    @{W=1920; H=1080; F=120},
    @{W=4096; H=2160; F=60} 
)
# ===============================

# Load Windows Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Function to get current display settings
function Get-CurrentDisplaySettings {
    $screens = [System.Windows.Forms.Screen]::AllScreens
    $currentSettings = @()
    
    for ($i = 0; $i -lt $screens.Length; $i++) {
        $screen = $screens[$i]
        $currentSettings += @{
            Index = $i + 1
            Name = "\\.\DISPLAY$($i + 1)"
            Width = $screen.Bounds.Width
            Height = $screen.Bounds.Height
            X = $screen.Bounds.X
            Y = $screen.Bounds.Y
            Primary = $screen.Primary
        }
    }
    
    return $currentSettings
}

# Function to show available displays
function Show-AvailableDisplays {
    $displays = Get-CurrentDisplaySettings
    Write-Host "Available displays:"
    foreach ($display in $displays) {
        $primary = if ($display.Primary) { " (Primary)" } else { "" }
        Write-Host "  Display $($display.Index): $($display.Width)x$($display.Height) at ($($display.X),$($display.Y))$primary"
    }
    return $displays
}

# Function to open Windows Display Settings
function Open-DisplaySettings {
    Write-Host "Opening Windows Display Settings..."
    Start-Process "ms-settings:display"
}

# Auto-detect display if none specified
if (-not $DisplayName) {
    $availableDisplays = Show-AvailableDisplays
    if ($availableDisplays.Count -eq 0) {
        Write-Error "No displays detected."
        exit 1
    }
    
    # Use the primary display or the first available
    $targetDisplay = $availableDisplays | Where-Object { $_.Primary } | Select-Object -First 1
    if (-not $targetDisplay) {
        $targetDisplay = $availableDisplays[0]
    }
    
    $DisplayName = $targetDisplay.Name
    Write-Host "Auto-detected display: $DisplayName ($($targetDisplay.Width)x$($targetDisplay.Height))"
}

# Get current display settings
$currentDisplays = Get-CurrentDisplaySettings
$currentDisplay = $currentDisplays | Where-Object { $_.Name -eq $DisplayName } | Select-Object -First 1

if (-not $currentDisplay) {
    Write-Error "Display $DisplayName not found. Available displays:"
    Show-AvailableDisplays
    exit 1
}

Write-Host "Current mode: $($currentDisplay.Width)x$($currentDisplay.Height)"

# Find current mode index
$currentIndex = -1
for ($i = 0; $i -lt $Modes.Count; $i++) {
    if ($Modes[$i].W -eq $currentDisplay.Width -and $Modes[$i].H -eq $currentDisplay.Height) {
        $currentIndex = $i
        break
    }
}

# Get next mode
$nextIndex = ($currentIndex + 1) % $Modes.Count
$nextMode = $Modes[$nextIndex]

Write-Host ""
Write-Host "=== MONITOR RESOLUTION CYCLE ===" -ForegroundColor Cyan
Write-Host "Current: $($currentDisplay.Width)x$($currentDisplay.Height)" -ForegroundColor Yellow
Write-Host "Next:    $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Show all available modes
Write-Host "Available modes in cycle:" -ForegroundColor Blue
for ($i = 0; $i -lt $Modes.Count; $i++) {
    $mode = $Modes[$i]
    $indicator = if ($i -eq $currentIndex) { "→" } elseif ($i -eq $nextIndex) { "→" } else { " " }
    Write-Host "  $indicator Mode $($i + 1): $($mode.W)x$($mode.H) @ $($mode.F)Hz" -ForegroundColor White
}

Write-Host ""
Write-Host "To change resolution:" -ForegroundColor Yellow
Write-Host "1. Press Win + I to open Settings" -ForegroundColor White
Write-Host "2. Go to System > Display" -ForegroundColor White
Write-Host "3. Select display: $DisplayName" -ForegroundColor White
Write-Host "4. Change resolution to: $($nextMode.W) x $($nextMode.H)" -ForegroundColor White
Write-Host "5. Set refresh rate to: $($nextMode.F) Hz (if available)" -ForegroundColor White
Write-Host ""

# Ask if user wants to open display settings
$response = Read-Host "Open Windows Display Settings now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Open-DisplaySettings
}

Write-Host ""
Write-Host "Resolution cycle complete! Run this script again to cycle to the next mode." -ForegroundColor Green
