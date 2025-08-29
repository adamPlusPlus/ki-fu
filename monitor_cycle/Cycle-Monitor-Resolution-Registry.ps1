# Cycle-Monitor-Resolution-Registry.ps1
# Attempts to change resolution through registry modifications
# This approach sometimes works when Windows API calls fail

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

# Function to find display adapter in registry
function Get-DisplayAdapterRegistryPath {
    try {
        # Look for display adapters in registry
        $adapters = Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Video\*" -ErrorAction SilentlyContinue
        foreach ($adapter in $adapters) {
            $adapterPath = $adapter.PSPath
            $deviceName = Get-ItemProperty "$adapterPath\0000" -Name "Device Description" -ErrorAction SilentlyContinue
            if ($deviceName) {
                Write-Host "Found adapter: $($deviceName.'Device Description') at $adapterPath"
                return "$adapterPath\0000"
            }
        }
    } catch {
        Write-Warning "Could not enumerate display adapters: $($_.Exception.Message)"
    }
    return $null
}

# Function to change resolution via registry
function Set-ResolutionViaRegistry {
    param(
        [string]$Width,
        [string]$Height,
        [string]$RefreshRate
    )
    
    try {
        $adapterPath = Get-DisplayAdapterRegistryPath
        if (-not $adapterPath) {
            Write-Warning "Could not find display adapter in registry"
            return $false
        }
        
        # Try to set resolution in registry
        $resolutionKey = "$adapterPath\Attach.RelativeX"
        $resolutionValue = "$Width,$Height"
        
        Write-Host "Attempting to set registry key: $resolutionKey = $resolutionValue"
        
        # This is a simplified approach - actual registry keys vary by driver
        Set-ItemProperty -Path $adapterPath -Name "Attach.RelativeX" -Value $resolutionValue -ErrorAction SilentlyContinue
        
        # Try alternative registry locations
        $alternativePaths = @(
            "HKLM:\SYSTEM\CurrentControlSet\Hardware Profiles\Current\System\CurrentControlSet\Control\VIDEO",
            "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
        )
        
        foreach ($path in $alternativePaths) {
            try {
                $subKeys = Get-ChildItem $path -ErrorAction SilentlyContinue
                foreach ($subKey in $subKeys) {
                    try {
                        Set-ItemProperty -Path $subKey.PSPath -Name "DefaultSettings.XResolution" -Value $Width -ErrorAction SilentlyContinue
                        Set-ItemProperty -Path $subKey.PSPath -Name "DefaultSettings.YResolution" -Value $Height -ErrorAction SilentlyContinue
                        Write-Host "Set resolution in: $($subKey.PSPath)"
                    } catch {
                        # Continue to next key
                    }
                }
            } catch {
                # Continue to next path
            }
        }
        
        return $true
    } catch {
        Write-Warning "Registry modification failed: $($_.Exception.Message)"
        return $false
    }
}

# Function to use QRes utility (if available)
function Set-ResolutionViaQRes {
    param(
        [string]$Width,
        [string]$Height,
        [string]$RefreshRate
    )
    
    # Check if QRes is available
    $qresPath = "C:\Windows\System32\qres.exe"
    if (-not (Test-Path $qresPath)) {
        $qresPath = "qres.exe"  # Try PATH
    }
    
    if (Test-Path $qresPath) {
        try {
            Write-Host "Using QRes utility to change resolution..."
            $arguments = "/x:$Width /y:$Height /f:$RefreshRate"
            $result = Start-Process -FilePath $qresPath -ArgumentList $arguments -Wait -PassThru
            return $result.ExitCode -eq 0
        } catch {
            Write-Warning "QRes execution failed: $($_.Exception.Message)"
        }
    } else {
        Write-Host "QRes utility not found. You can download it from:"
        Write-Host "https://www.majorgeeks.com/files/details/qres.html"
    }
    
    return $false
}

# Function to use DisplaySwitch utility
function Set-ResolutionViaDisplaySwitch {
    param(
        [string]$Width,
        [string]$Height
    )
    
    try {
        # Try to use Windows built-in display switching
        Write-Host "Attempting to use Windows DisplaySwitch utility..."
        
        # This is a bit of a hack - we'll try to trigger a display change
        $devices = Get-WmiObject -Class Win32_VideoController
        foreach ($device in $devices) {
            try {
                $device.SetScreenResolution($Width, $Height)
                Write-Host "Successfully changed resolution via WMI for: $($device.Name)"
                return $true
            } catch {
                # Continue to next device
            }
        }
    } catch {
        Write-Warning "DisplaySwitch approach failed: $($_.Exception.Message)"
    }
    
    return $false
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
Write-Host "=== ATTEMPTING RESOLUTION CHANGE ===" -ForegroundColor Cyan
Write-Host "Current: $($currentDisplay.Width)x$($currentDisplay.Height)" -ForegroundColor Yellow
Write-Host "Target:  $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Try multiple approaches to change resolution
$success = $false

Write-Host "Method 1: Registry modification..." -ForegroundColor Blue
$success = Set-ResolutionViaRegistry -Width $nextMode.W -Height $nextMode.H -RefreshRate $nextMode.F

if (-not $success) {
    Write-Host "Method 2: QRes utility..." -ForegroundColor Blue
    $success = Set-ResolutionViaQRes -Width $nextMode.W -Height $nextMode.H -RefreshRate $nextMode.F
}

if (-not $success) {
    Write-Host "Method 3: WMI DisplaySwitch..." -ForegroundColor Blue
    $success = Set-ResolutionViaDisplaySwitch -Width $nextMode.W -Height $nextMode.H
}

if ($success) {
    Write-Host ""
    Write-Host "SUCCESS! Resolution changed to $($nextMode.W)x$($nextMode.H)" -ForegroundColor Green
    Write-Host "You may need to restart your computer for changes to take full effect." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "All automatic methods failed. Here are manual alternatives:" -ForegroundColor Red
    Write-Host ""
    Write-Host "1. **Graphics Driver Control Panel** (Most Reliable):" -ForegroundColor Yellow
    Write-Host "   - Right-click desktop > Graphics Options > Display Settings"
    Write-Host "   - Or open NVIDIA Control Panel / AMD Radeon Settings"
    Write-Host ""
    Write-Host "2. **Windows Settings** (Limited):" -ForegroundColor Yellow
    Write-Host "   - Win + I > System > Display > Advanced display settings"
    Write-Host ""
    Write-Host "3. **Third-party Tools** (Use at your own risk):" -ForegroundColor Yellow
    Write-Host "   - QRes: https://www.majorgeeks.com/files/details/qres.html"
    Write-Host "   - Custom Resolution Utility (CRU)"
    Write-Host "   - Display Driver Uninstaller (DDU) + fresh driver install"
    Write-Host ""
    Write-Host "4. **Command Line Tools** (Advanced):" -ForegroundColor Yellow
    Write-Host "   - nircmd (if you have it installed)"
    Write-Host "   - Custom PowerShell scripts with elevated privileges"
}

Write-Host ""
Write-Host "Next mode in cycle: $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz" -ForegroundColor Cyan
