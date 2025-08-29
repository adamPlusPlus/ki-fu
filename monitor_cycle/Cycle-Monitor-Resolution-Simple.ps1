# Cycle-Monitor-Resolution-Simple.ps1
# Simple version that cycles monitor resolutions using Windows Forms
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

# Function to change display resolution using ChangeDisplaySettings
function Change-DisplayResolution {
    param(
        [string]$DisplayName,
        [int]$Width,
        [int]$Height
    )
    
    # Use the Windows API through P/Invoke
    $signature = @"
    [DllImport("user32.dll")]
    public static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);
    
    [DllImport("user32.dll")]
    public static extern bool EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);
    
    [StructLayout(LayoutKind.Sequential)]
    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public ushort dmSpecVersion;
        public ushort dmDriverVersion;
        public ushort dmSize;
        public ushort dmDriverExtra;
        public uint dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public uint dmDisplayOrientation;
        public uint dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public ushort dmLogPixels;
        public uint dmBitsPerPel;
        public uint dmPelsWidth;
        public uint dmPelsHeight;
        public uint dmDisplayFlags;
        public uint dmDisplayFrequency;
    }
"@
    
    try {
        Add-Type -MemberDefinition $signature -Name Win32 -Namespace Console
        $devMode = New-Object Console.Win32+DEVMODE
        $devMode.dmDeviceName = $DisplayName
        $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf([Console.Win32+DEVMODE])
        $devMode.dmFields = 0x80000 -bor 0x100000  # DM_PELSWIDTH | DM_PELSHEIGHT
        $devMode.dmPelsWidth = $Width
        $devMode.dmPelsHeight = $Height
        
        $result = [Console.Win32]::ChangeDisplaySettings([ref]$devMode, 0)
        return $result
    } catch {
        Write-Warning "Could not change resolution using Windows API: $($_.Exception.Message)"
        return -1
    }
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

Write-Host "Switching to: $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz"

# Try to change resolution
$result = Change-DisplayResolution -DisplayName $DisplayName -Width $nextMode.W -Height $nextMode.H

switch ($result) {
    0   { Write-Output "OK: $DisplayName -> $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz" }
    1   { Write-Output "Changed (restart recommended): $DisplayName -> $($nextMode.W)x$($nextMode.H)" }
    -2  { Write-Output "BAD MODE: $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz not supported."; exit 2 }
    default { 
        Write-Warning "Could not change resolution programmatically. Please change manually to: $($nextMode.W)x$($nextMode.H)"
        Write-Output "Next mode: $($nextMode.W)x$($nextMode.H) @ $($nextMode.F)Hz"
    }
}
