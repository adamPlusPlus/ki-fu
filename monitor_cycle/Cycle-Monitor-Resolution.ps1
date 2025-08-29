# Cycle-Monitor-Resolution.ps1
# Cycles a single monitor through predefined resolutions on each run.
# Usage: Run with default settings, or pass -DisplayName '\\.\DISPLAY2'

param(
    [string]$DisplayName = '\\.\DISPLAY4',
    [Parameter()][ValidateSet('W','H','F')]$SortKey = 'W'  # not used, but handy if you extend
)

# ====== EDIT THESE 3 MODES ======
$Modes = @(
    @{W=1280; H=960; F=144},
    @{W=1920; H=1080; F=120},
    @{W=4096; H=2160; F=60} 
)
# ===============================

Add-Type -Namespace Win32 -Name Native -MemberDefinition @"
using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
public struct DEVMODEA {
    public const int CCHDEVICENAME = 32;
    public const int CCHFORMNAME = 32;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = CCHDEVICENAME)]
    public string dmDeviceName;
    public UInt16 dmSpecVersion;
    public UInt16 dmDriverVersion;
    public UInt16 dmSize;
    public UInt16 dmDriverExtra;
    public UInt32 dmFields;

    public Int16 dmOrientation;
    public Int16 dmPaperSize;
    public Int16 dmPaperLength;
    public Int16 dmPaperWidth;
    public Int16 dmScale;
    public Int16 dmCopies;
    public Int16 dmDefaultSource;
    public Int16 dmPrintQuality;

    public Int16 dmColor;
    public Int16 dmDuplex;
    public Int16 dmYResolution;
    public Int16 dmTTOption;
    public Int16 dmCollate;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = CCHFORMNAME)]
    public string dmFormName;
    public UInt16 dmLogPixels;
    public UInt32 dmBitsPerPel;
    public UInt32 dmPelsWidth;
    public UInt32 dmPelsHeight;
    public UInt32 dmDisplayFlags;
    public UInt32 dmDisplayFrequency;

    public UInt32 dmICMMethod;
    public UInt32 dmICMIntent;
    public UInt32 dmMediaType;
    public UInt32 dmDitherType;
    public UInt32 dmReserved1;
    public UInt32 dmReserved2;
    public UInt32 dmPanningWidth;
    public UInt32 dmPanningHeight;
}

public static class NativeMethods {
    public const int ENUM_CURRENT_SETTINGS = -1;

    public const int DM_PELSWIDTH       = 0x00080000;
    public const int DM_PELSHEIGHT      = 0x00100000;
    public const int DM_DISPLAYFREQUENCY= 0x00400000;
    public const int CDS_UPDATEREGISTRY = 0x00000001;
    public const int CDS_TEST           = 0x00000002;

    public const int DISP_CHANGE_SUCCESSFUL = 0;
    public const int DISP_CHANGE_RESTART    = 1;
    public const int DISP_CHANGE_BADMODE    = -2;

    [DllImport("user32.dll", CharSet = CharSet.Ansi)]
    public static extern bool EnumDisplaySettingsA(string lpszDeviceName, int iModeNum, ref DEVMODEA lpDevMode);

    [DllImport("user32.dll", CharSet = CharSet.Ansi)]
    public static extern int ChangeDisplaySettingsExA(string lpszDeviceName, ref DEVMODEA lpDevMode, IntPtr hwnd, int dwflags, IntPtr lParam);
}
"@

function Get-CurrentMode($devName) {
    $dm = New-Object Win32.DEVMODEA
    $dm.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf([type]::GetType('Win32.DEVMODEA'))
    $ok = [Win32.NativeMethods]::EnumDisplaySettingsA($devName, [Win32.NativeMethods]::ENUM_CURRENT_SETTINGS, [ref]$dm)
    if (-not $ok) { throw "EnumDisplaySettings failed for $devName" }
    [pscustomobject]@{
        W = [int]$dm.dmPelsWidth
        H = [int]$dm.dmPelsHeight
        F = [int]$dm.dmDisplayFrequency
        Raw = $dm
    }
}

function Apply-Mode($devName, $w, $h, $f) {
    $dm = New-Object Win32.DEVMODEA
    $dm.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf([type]::GetType('Win32.DEVMODEA'))
    $ok = [Win32.NativeMethods]::EnumDisplaySettingsA($devName, [Win32.NativeMethods]::ENUM_CURRENT_SETTINGS, [ref]$dm)
    if (-not $ok) { throw "EnumDisplaySettings failed for $devName" }

    $dm.dmFields        = [Win32.NativeMethods]::DM_PELSWIDTH -bor [Win32.NativeMethods]::DM_PELSHEIGHT
    $dm.dmPelsWidth     = [uint32]$w
    $dm.dmPelsHeight    = [uint32]$h

    $tryRefresh = $true
    $lastCode = $null

    foreach ($freq in @($f, 0)) { # 0 -> let OS pick closest
        if (-not $tryRefresh) { break }
        $dm2 = $dm
        if ($freq -gt 0) {
            $dm2.dmFields = $dm2.dmFields -bor [Win32.NativeMethods]::DM_DISPLAYFREQUENCY
            $dm2.dmDisplayFrequency = [uint32]$freq
        }
        $code = [Win32.NativeMethods]::ChangeDisplaySettingsExA($devName, [ref]$dm2, [IntPtr]::Zero, 0, [IntPtr]::Zero)
        $lastCode = $code
        if ($code -eq [Win32.NativeMethods]::DISP_CHANGE_SUCCESSFUL -or $code -eq [Win32.NativeMethods]::DISP_CHANGE_RESTART) {
            return $code
        }
        if ($code -eq [Win32.NativeMethods]::DISP_CHANGE_BADMODE -and $freq -ne 0) {
            # retry without forcing refresh
            continue
        }
        break
    }
    return $lastCode
}

# ---- main ----
# find current index
$cur = Get-CurrentMode $DisplayName
$idx = ($Modes | ForEach-Object { $_ }) |
    ForEach-Object -Begin { $i=0 } -Process {
        if ($_.W -eq $cur.W -and $_.H -eq $cur.H) {
            if ($_.F -eq $cur.F) { $script:match=$i }
            elseif (-not $script:match) { $script:match=$i } # width/height match, ignore F
        }
        $i++
    }; $match = $script:match; if ($null -eq $match) { $match = -1 }

$next = $Modes[ ($match + 1) % $Modes.Count ]
$code = Apply-Mode $DisplayName $next.W $next.H $next.F

switch ($code) {
    0   { Write-Output "OK: $DisplayName -> ${($next.W)}x${($next.H)} @ ${($next.F)}Hz" }
    1   { Write-Output "Changed (restart recommended): $DisplayName -> ${($next.W)}x${($next.H)}" }
    -2  { Write-Output "BAD MODE: ${($next.W)}x${($next.H)} @ ${($next.F)}Hz not supported."; exit 2 }
    default { Write-Output "Error code $code applying ${($next.W)}x${($next.H)} @ ${($next.F)}Hz"; exit 1 }
}
