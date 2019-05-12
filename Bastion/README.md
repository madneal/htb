# Bastion -- Hack the box

## Intrdouction

Target: 10.10.10.134 (Windows)

Kali: 10.10.16.65

In conclusion, Bastion is not a medium box. But it would be easier to solve this box with windows vm. Command vm may be a good choice. But it can be finished by kali.

## Information enumeration

Firstly, detect the open ports:

```
# Nmap 7.70 scan initiated Sun May  5 12:33:32 2019 as: nmap -sT -p- --min-rate 10000 -oN ports 10.10.10.134
Warning: 10.10.10.134 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.134
Host is up (0.33s latency).
Not shown: 60653 closed ports, 4873 filtered ports
PORT      STATE SERVICE
22/tcp    open  ssh
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
49664/tcp open  unknown
49665/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49670/tcp open  unknown
```

From the open ports, it can be induced that the box may be a windows machine that opens ssh service. Then try to obtain the detailed services of these open ports:

```
# Nmap 7.70 scan initiated Sun May  5 12:29:46 2019 as: nmap -A -oN services 10.10.10.134
Nmap scan report for 10.10.10.134
Host is up (0.53s latency).
Not shown: 996 closed ports
PORT    STATE SERVICE      VERSION
22/tcp  open  ssh          OpenSSH for_Windows_7.9 (protocol 2.0)
| ssh-hostkey:
|   2048 3a:56:ae:75:3c:78:0e:c8:56:4d:cb:1c:22:bf:45:8a (RSA)
|   256 cc:2e:56:ab:19:97:d5:bb:03:fb:82:cd:63:da:68:01 (ECDSA)
|_  256 93:5f:5d:aa:ca:9f:53:e7:f2:82:e6:64:a8:a3:a0:18 (ED25519)
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.70%E=4%D=5/5%OT=22%CT=1%CU=37821%PV=Y%DS=2%DC=T%G=Y%TM=5CCED772
OS:%P=x86_64-pc-linux-gnu)SEQ(SP=F4%GCD=1%ISR=10A%TI=I%CI=I%II=I%SS=S%TS=A)
OS:SEQ(SP=F3%GCD=1%ISR=10A%TI=I%CI=I%TS=A)OPS(O1=M54BNW8ST11%O2=M54BNW8ST11
OS:%O3=M54BNW8NNT11%O4=M54BNW8ST11%O5=M54BNW8ST11%O6=M54BST11)WIN(W1=2000%W
OS:2=2000%W3=2000%W4=2000%W5=2000%W6=2000)ECN(R=Y%DF=Y%T=80%W=2000%O=M54BNW
OS:8NNS%CC=Y%Q=)T1(R=Y%DF=Y%T=80%S=O%A=S+%F=AS%RD=0%Q=)T2(R=Y%DF=Y%T=80%W=0
OS:%S=Z%A=S%F=AR%O=%RD=0%Q=)T3(R=Y%DF=Y%T=80%W=0%S=Z%A=O%F=AR%O=%RD=0%Q=)T4
OS:(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=80%W=0%S=Z%A=S+%
OS:F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%
OS:T=80%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=80%IPL=164%UN=0%RIPL=G%R
OS:ID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=80%CD=Z)

Network Distance: 2 hops
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -43m13s, deviation: 1h09m14s, median: -3m15s
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Bastion
|   NetBIOS computer name: BASTION\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2019-05-05T14:27:12+02:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2019-05-05 12:27:09
|_  start_date: 2019-05-05 12:10:06

TRACEROUTE (using port 143/tcp)
HOP RTT       ADDRESS
1   693.81 ms 10.10.16.1
2   694.08 ms 10.10.10.134

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun May  5 12:30:42 2019 -- 1 IP address (1 host up) scanned in 56.60 seconds
```

## Exploitation

There seem to be nothing special. For normal box, http service will be the starting. For this box, we should try smb service for port 445. For smb service exploitation in kali, we choose to use smbmap, smbclient, enum4linux, etc. Let's try smbclient:

```
smbclient -L 10.10.10.134
```

![E4k8CF.png](https://s2.ax1x.com/2019/05/12/E4k8CF.png)

With smcclient we can see the smb shares of this box without any password. Try to access the share by `smbclient //10.10.10.134/sharename`. But the three shares cannot be accessed except `Backups`.

![E4kygH.png](https://s2.ax1x.com/2019/05/12/E4kygH.png)
guestmount --add //10.10.10.134/backups/WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351/9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /root/htb/Bastion/VHD

mount -t cifs //10.10.10.134/Backups -o user=guest,password= /mnt/backups
