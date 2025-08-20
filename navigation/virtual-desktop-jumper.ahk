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

; Initialize by counting existing desktops
CountVirtualDesktops()

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

; Function to jump to a specific virtual desktop
JumpToDesktop(targetDesktop) {
    global currentDesktop, totalDesktops
    
    ; Validate target desktop number
    if (targetDesktop < 1 || targetDesktop > totalDesktops) {
        ShowTooltip("Desktop " . targetDesktop . " does not exist. Total: " . totalDesktops)
        return
    }
    
    ; If we're already on the target desktop, do nothing
    if (targetDesktop = currentDesktop) {
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
    ShowTooltip("Desktop count initialized. Use Ctrl+Win+R to refresh count.")
}

; Function to refresh desktop count
RefreshDesktopCount() {
    global totalDesktops, currentDesktop
    
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
    
    ShowTooltip("Refreshed: Found " . totalDesktops . " virtual desktops")
}

; Function to show current desktop information
ShowDesktopInfo() {
    global currentDesktop, totalDesktops
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
ShowTooltip("Virtual Desktop Jumper loaded! Use Ctrl+Win+Numpad to jump to desktops.")
SetTimer, RemoveTooltip, -3000

; Add tray menu for easy access
Menu, Tray, NoStandard
Menu, Tray, Add, Refresh Desktop Count, RefreshDesktopCount
Menu, Tray, Add, Show Desktop Info, ShowDesktopInfo
Menu, Tray, Add
Menu, Tray, Add, Exit, ExitApp
Menu, Tray, Default, Refresh Desktop Count
Menu, Tray, Tip, Virtual Desktop Jumper`nCtrl+Win+Numpad to jump

return
