https://curesec.com/blog/article/blog/NibbleBlog-403-Code-Execution-47.html

# Nibbles - Hack the box

## Introduction

Target: 10.10.10.75(OS: Linux)
Kali linux: 10.10.16.44

## Information Enumeration

Firstly, detect the open ports:

```
nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.75
```

![Ae19BQ.png](https://s2.ax1x.com/2019/03/17/Ae19BQ.png)

There are not too many open ports, just `80` and `22`. Detect the detailed services of the open ports:

```
nmap -sC -sV -oA services 10.10.10.75
```

![Ae1E90.png](https://s2.ax1x.com/2019/03/17/Ae1E90.png)

Nothing special found. The only clue may be the open port of `80`. To be honest, the box with less open ports is easier in general.

## Exploit

### Http




