#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#SingleInstance force  ; Ensures only one instance runs
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; Virtual Desktop Jumper Script
; Allows jumping to specific virtual desktops using Ctrl+Win+Numpad combinations
; Run this script as administrator for best compatibility

; Global variables
global currentDesktop := 1
global totalDesktops := 1
global logEntries := []
global maxVisibleLogs := 50
global maxFileLogs := 200
global logFilePath := A_ScriptDir . "\allogs.txt"

; Initialize by counting existing desktops
CountVirtualDesktops()

; Initialize logging
InitializeLogging()

; Hotkeys for jumping to specific virtual desktops
^#Numpad1::JumpToDesktop(1)
^#Numpad2::JumpToDesktop(2)
^#Numpad3::JumpToDesktop(3)
^#Numpad4::JumpToDesktop(4)
^#Numpad5::JumpToDesktop(5)
^#Numpad6::JumpToDesktop(6)
^#Numpad7::JumpToDesktop(7)
^#Numpad8::JumpToDesktop(8)
^#Numpad9::JumpToDesktop(9)

; Alternative hotkeys for non-numpad users (Ctrl+Win+1-9)
^#1::JumpToDesktop(1)
^#2::JumpToDesktop(2)
^#3::JumpToDesktop(3)
^#4::JumpToDesktop(4)
^#5::JumpToDesktop(5)
^#6::JumpToDesktop(6)
^#7::JumpToDesktop(7)
^#8::JumpToDesktop(8)
^#9::JumpToDesktop(9)

; Refresh desktop count (Ctrl+Win+R)
^#r::RefreshDesktopCount()

; Show current desktop info (Ctrl+Win+I)
^#i::ShowDesktopInfo()

; Show recent logs (Ctrl+Win+L)
^#l::ShowRecentLogs()

; Function to initialize logging system
InitializeLogging() {
    global logEntries, logFilePath
    
    ; Create log file if it doesn't exist
    if (!FileExist(logFilePath)) {
        FileAppend, ;, %logFilePath%
    }
    
    ; Load existing logs from file (limited to maxFileLogs)
    LoadLogsFromFile()
    
    ; Add initial log entry
    AddLog("INFO", "Virtual Desktop Jumper initialized")
}

; Function to add log entry
AddLog(level, message, context := "") {
    global logEntries, maxVisibleLogs, maxFileLogs, logFilePath
    
    ; Create log entry
    timestamp := A_Now
    entry := timestamp . " [" . level . "] " . message
    if (context != "") {
        entry := entry . " {" . context . "}"
    }
    
    ; Add to memory array (limited to maxVisibleLogs)
    logEntries.InsertAt(1, entry)
    if (logEntries.Length() > maxVisibleLogs) {
        logEntries.Pop()
    }
    
    ; Write to file
    FileAppend, %entry%`n, %logFilePath%
    
    ; Check if file has too many entries and rotate if needed
    CheckAndRotateLogFile()
}

; Function to load logs from file
LoadLogsFromFile() {
    global logEntries, maxVisibleLogs, logFilePath
    
    if (FileExist(logFilePath)) {
        Loop, Read, %logFilePath%
        {
            if (A_LoopReadLine != "") {
                logEntries.InsertAt(1, A_LoopReadLine)
                if (logEntries.Length() > maxVisibleLogs) {
                    logEntries.Pop()
                }
            }
        }
    }
}

; Function to check and rotate log file
CheckAndRotateLogFile() {
    global logFilePath, maxFileLogs
    
    ; Count lines in file
    lineCount := 0
    Loop, Read, %logFilePath%
    {
        lineCount++
    }
    
    ; If file has more than maxFileLogs entries, overwrite it
    if (lineCount > maxFileLogs) {
        ; Keep only the most recent entries
        tempArray := []
        Loop, Read, %logFilePath%
        {
            if (A_LoopReadLine != "") {
                tempArray.InsertAt(1, A_LoopReadLine)
            }
        }
        
        ; Clear file and write only recent entries
        FileDelete, %logFilePath%
        Loop, %tempArray.Length()
        {
            if (A_Index <= maxFileLogs) {
                FileAppend, % tempArray[A_Index] . "`n", %logFilePath%
            }
        }
    }
}

; Function to show recent logs
ShowRecentLogs() {
    global logEntries, maxVisibleLogs
    
    if (logEntries.Length() = 0) {
        ShowTooltip("No logs available")
        return
    }
    
    ; Create log display (limited to maxVisibleLogs)
    logDisplay := "Recent Logs:`n"
    Loop, % Min(logEntries.Length(), maxVisibleLogs)
    {
        logDisplay := logDisplay . logEntries[A_Index] . "`n"
    }
    
    ; Show in a simple message box (limited size to prevent crashes)
    if (StrLen(logDisplay) > 1000) {
        logDisplay := SubStr(logDisplay, 1, 1000) . "`n... (truncated)"
    }
    
    MsgBox, %logDisplay%
}

; Function to jump to a specific virtual desktop
JumpToDesktop(targetDesktop) {
    global currentDesktop, totalDesktops
    
    ; Log the jump attempt
    AddLog("INFO", "Jump attempt to desktop " . targetDesktop, "current:" . currentDesktop)
    
    ; Validate target desktop number
    if (targetDesktop < 1 || targetDesktop > totalDesktops) {
        AddLog("WARN", "Invalid desktop number " . targetDesktop, "total:" . totalDesktops)
        ShowTooltip("Desktop " . targetDesktop . " does not exist. Total: " . totalDesktops)
        return
    }
    
    ; If we're already on the target desktop, do nothing
    if (targetDesktop = currentDesktop) {
        AddLog("INFO", "Already on target desktop " . currentDesktop)
        ShowTooltip("Already on Desktop " . currentDesktop)
        return
    }
    
    ; Calculate how many desktops to move
    local desktopsToMove := targetDesktop - currentDesktop
    
    ; Use Windows built-in shortcuts to navigate
    if (desktopsToMove > 0) {
        ; Move right (forward)
        Loop, %desktopsToMove% {
            Send, #^{Right}
            Sleep, 100  ; Small delay to ensure desktop switch completes
        }
    } else {
        ; Move left (backward)
        Loop, %Abs(desktopsToMove)% {
            Send, #^{Left}
            Sleep, 100  ; Small delay to ensure desktop switch completes
        }
    }
    
    ; Update current desktop tracking
    currentDesktop := targetDesktop
    
    ; Log successful jump
    AddLog("INFO", "Successfully jumped to desktop " . currentDesktop, "moved:" . desktopsToMove)
    
    ; Show confirmation
    ShowTooltip("Jumped to Desktop " . currentDesktop)
}

; Function to count existing virtual desktops
CountVirtualDesktops() {
    global totalDesktops
    
    ; This is a rough estimation - Windows doesn't expose a direct API for this
    ; We'll start with 1 and let the user refresh as needed
    totalDesktops := 1
    
    ; Try to detect existing desktops by attempting to navigate
    ; Note: This is not 100% reliable but gives a reasonable starting point
    AddLog("INFO", "Desktop count initialized", "count:" . totalDesktops)
    ShowTooltip("Desktop count initialized. Use Ctrl+Win+R to refresh count.")
}

; Function to refresh desktop count
RefreshDesktopCount() {
    global totalDesktops, currentDesktop
    
    AddLog("INFO", "Refreshing desktop count")
    
    ; Reset to 1 and try to count by navigating
    totalDesktops := 1
    currentDesktop := 1
    
    ; Try to navigate right until we can't anymore
    Loop, 20 {  ; Limit to prevent infinite loops
        Send, #^{Right}
        Sleep, 200
        
        ; Check if we're still on a valid desktop
        ; This is a heuristic approach
        if (A_Index > 1) {
            totalDesktops++
        }
        
        ; Small delay to let Windows process the navigation
        Sleep, 100
    }
    
    ; Navigate back to desktop 1
    Loop, %totalDesktops% {
        Send, #^{Left}
        Sleep, 100
    }
    currentDesktop := 1
    
    AddLog("INFO", "Desktop count refreshed", "found:" . totalDesktops)
    ShowTooltip("Refreshed: Found " . totalDesktops . " virtual desktops")
}

; Function to show current desktop information
ShowDesktopInfo() {
    global currentDesktop, totalDesktops
    AddLog("INFO", "Desktop info requested", "current:" . currentDesktop . "/" . totalDesktops)
    ShowTooltip("Current: Desktop " . currentDesktop . " of " . totalDesktops)
}

; Function to show tooltips
ShowTooltip(message) {
    ToolTip, %message%
    SetTimer, RemoveTooltip, -2000  ; Remove tooltip after 2 seconds
}

; Timer function to remove tooltip
RemoveTooltip:
ToolTip
return

; Show startup message
AddLog("INFO", "Virtual Desktop Jumper loaded")
ShowTooltip("Virtual Desktop Jumper loaded! Use Ctrl+Win+Numpad to jump to desktops.")
SetTimer, RemoveTooltip, -3000

; Add tray menu for easy access
Menu, Tray, NoStandard
Menu, Tray, Add, Refresh Desktop Count, RefreshDesktopCount
Menu, Tray, Add, Show Desktop Info, ShowDesktopInfo
Menu, Tray, Add, Show Recent Logs, ShowRecentLogs
Menu, Tray, Add
Menu, Tray, Add, Exit, ExitApp
Menu, Tray, Default, Refresh Desktop Count
Menu, Tray, Tip, Virtual Desktop Jumper`nCtrl+Win+Numpad to jump

return
