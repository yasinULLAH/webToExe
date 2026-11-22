import subprocess

arg1 = '--user-data-dir="C:\\Users\\Yasin\\AppData\\Local\\WebAppKiosks\\Hospital_Management_Portal_Profile"'
cmd1 = subprocess.list2cmdline(['chrome.exe', arg1])
print("cmd1:", cmd1)

arg2 = '--user-data-dir=C:\\Users\\Yasin\\AppData\\Local\\WebAppKiosks\\Hospital_Management_Portal_Profile'
cmd2 = subprocess.list2cmdline(['chrome.exe', arg2])
print("cmd2:", cmd2)
