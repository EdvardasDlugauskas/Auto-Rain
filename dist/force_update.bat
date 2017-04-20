powershell -noprofile -command ^
Invoke-WebRequest -OutFile "rain.kv" -URI https://raw.githubusercontent.com/EdvardasDlugauskas/Auto-Rain/master/dist/rain.kv;^
Invoke-WebRequest -OutFile "AutoRain.exe" -URI https://github.com/EdvardasDlugauskas/Auto-Rain/raw/master/dist/AutoRain.exe