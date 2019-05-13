# Bastion -- Hack the box

![E4RxRs.png](https://s2.ax1x.com/2019/05/13/E4RxRs.png)

## Intrdouction

Target: 10.10.10.134 (Windows)

Kali: 10.10.16.65

In conclusion, Bastion is not a medium box. But it would be easier to solve this box with windows VM. Command VM may be a good choice. But it can be finished by kali.

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

There seem to be nothing special. For a normal box, http service will be the starting. For this box, we should try smb service for port 445. For smb service exploitation in kali, we choose to use smbmap, smbclient, enum4linux, etc. Let's try smbclient:

```
smbclient -L 10.10.10.134
```

![E4k8CF.png](https://s2.ax1x.com/2019/05/12/E4k8CF.png)

With smbclient, we can see the smb shares of this box without any password. Try to access the share by `smbclient //10.10.10.134/sharename`. But the three shares cannot be accessed except `Backups`.

![E4kygH.png](https://s2.ax1x.com/2019/05/12/E4kygH.png)

Access to the share of `Backups`: `smbclient //10.10.10.134/Backups`:

![E4dx2D.png](https://s2.ax1x.com/2019/05/13/E4dx2D.png)

There is a note.txt in the share:

```
Sysadmins: please don't transfer the entire backup file locally, the VPN to the subsidiary office is too slow.
```

It does is a hint for something useful in the exploitation. It is inconvenient to access files by smbclient, as you cannot browse the file directly. So try to mount the shared folder to kali:

```
mount -t cifs //10.10.10.134/Backups -o user=guest,password= /mnt/backups
```

![E40VT1.png](https://s2.ax1x.com/2019/05/13/E40VT1.png)

Here, we can access the files directly. It may be a backup folder. After some exploration, we have found some interesting files.

![E40w6g.png](https://s2.ax1x.com/2019/05/13/E40w6g.png)

VHD(virtual hard disk) files seem to be very interesting. According to the wiki, `VHD is a file format which represents a virtual hard disk drive (HDD). It may contain what is found on a physical HDD, such as disk partitions and a file system, which in turn can contain files and folders. It is typically used as the hard disk of a virtual machine`. So we may find more interesting contents in the VHD files. There are two vhd files, one is 37M, and the other is 5.1 G. The larger one seems to be attractive to us. But it will be inconvenient to download the whole vhd file. According to the discussions in the forum, the author has said that you don't have to download the vhd file. Try to mount the vhd file to kai:

```
guestmount --add /mnt/backups/WindowsImageBackup/L4mpje-PC/Backup\ 2019-02-22\ 124351/9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /mnt/vhd
```

The operation may cost some time if the network is not very stable. Then, the vhd file in mounted successfully. It seems to be an OS disk. There seem nothing special. Security Account Manager(SAM) is the database file in Windows which stores user passwords. Try to access the SAM files, `samdump2` can be utilized to dump the hash.

![E40w6g.png](https://s2.ax1x.com/2019/05/13/E40w6g.png)

![E4syKU.png](https://s2.ax1x.com/2019/05/13/E4syKU.png)

From the dumped hash, the hash of L4mpje seems to be useful. We can access [HashKiller](https://hashkiller.co.uk/Cracker) to crack the hash.

![E4yEin.png](https://s2.ax1x.com/2019/05/13/E4yEin.png)

We cracked it! As we know the box opens ssh service, so try to access ssh with the user of L4mpje. Of course, we are in. 

![E4yzk9.png](https://s2.ax1x.com/2019/05/13/E4yzk9.png)

## Privilege escalation

After login with user L4mpje, we find that we have relatively limited permission. PrivEsc is often vulnerable to some specific software vulnerability. It is significant to see the program files of the box.

![E4chPs.png](https://s2.ax1x.com/2019/05/13/E4chPs.png)

We can find an interesting folder `mRemoteNG`. [It](https://github.com/mRemoteNG/mRemoteNG) is an open source remote connections management tool. But there is a problem that the connections user information can be obtained by the config files. For this box, someone has created a tool to crack the password in this config file. The config file is store is the AppData folder.

![E4g4Te.png](https://s2.ax1x.com/2019/05/13/E4g4Te.png)

![E42wct.png](https://s2.ax1x.com/2019/05/13/E42wct.png)

It seems that the password of Administrator is stored in the XML file. Someone has created [mremoteng-decrypt](https://github.com/kmahyyg/mremoteng-decrypt) to crack the password. It is so convenient thanks to his awesome work.

```
java -jar decipher_mremoteng.jar "aEWNFV5uGcjUHF0uS17QTdT9kVqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw=="
```

![E42O3R.png](https://s2.ax1x.com/2019/05/13/E42O3R.png)

Wow, we get the password of Administrator.

![E42xu6.png](https://s2.ax1x.com/2019/05/13/E42xu6.png)

