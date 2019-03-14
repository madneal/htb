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

