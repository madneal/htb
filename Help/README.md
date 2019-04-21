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

There two exploits about `HelpDeskZ`. `Arbitrary File Upload` is interesting, it seems that it can be exploited with valid credentials.
