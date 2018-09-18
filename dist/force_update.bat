:: Force-updates AutoRain.exe and rain.kv with the latest versions available on github
powershell -noprofile -command
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12;^
Invoke-WebRequest -OutFile "rain.kv" -URI https://raw.githubusercontent.com/EdvardasDlugauskas/Auto-Rain/master/rain.kv;
Invoke-WebRequest -OutFile "AutoRain.exe" -URI https://github.com/EdvardasDlugauskas/Auto-Rain/raw/master/dist/AutoRain.exe;
Invoke-WebRequest -OutFile "force_update.bat" -URI https://github.com/EdvardasDlugauskas/Auto-Rain/raw/master/dist/force_update.bat;
