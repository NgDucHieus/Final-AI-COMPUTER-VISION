import os
import winshell
from win32com.client import Dispatch

# Đường dẫn tới tệp batch
bat_path = os.path.abspath("run.bat")
shortcut_path = os.path.join(winshell.desktop(), "hello.lnk")

# Tạo shortcut
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut(shortcut_path)
shortcut.TargetPath = bat_path
shortcut.WorkingDirectory = os.path.dirname(bat_path)
shortcut.Save()

print(f"Shortcut tạo thành công tại: {shortcut_path}")
