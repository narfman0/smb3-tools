; capture and pass along a keypress
#include <MsgBoxConstants.au3>
#include <WinApi.au3>

HotKeySet("{Home}", "captureHome")
AutoItSetOption ( "SendKeyDownDelay", 20 )
Func captureHome()
    HotKeySet("{Home}")
    WinActivate ("FCEUX")
    Send("{Home}")
    HotKeySet("{Home}", "captureHome")
 EndFunc

 While 1
    Sleep(1)
WEnd