# HayStack

## Introduction

HayStack is an easy box in hack the box. But it does isn't easy at all. It's annoying to find the user and password in the messy Spanish. For the root, you should have a basic understanding of ELK. Hence, the box is quite fresh in htb.

## Information Enumeration

As usual, nmap is utilized to detect detailed ports and services.

```
# Nmap 7.70 scan initiated Sun Jun 30 01:10:53 2019 as: nmap -sT -p- --min-rate 1500 -oN ports 10.10.10.115
Nmap scan report for 10.10.10.115
Host is up (0.27s latency).
Not shown: 65532 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
9200/tcp open  wap-wsp
```

Then detect the detailed services:

```
# Nmap 7.70 scan initiated Sun Jun 30 01:13:05 2019 as: nmap -sC -sV -p22,80,9200 -oN services 10.10.10.115
Nmap scan report for 10.10.10.115
Host is up (0.38s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey:
|   2048 2a:8d:e2:92:8b:14:b6:3f:e4:2f:3a:47:43:23:8b:2b (RSA)
|   256 e7:5a:3a:97:8e:8e:72:87:69:a3:0d:d1:00:bc:1f:09 (ECDSA)
|_  256 01:d2:59:b2:66:0a:97:49:20:5f:1c:84:eb:81:ed:95 (ED25519)
80/tcp   open  http    nginx 1.12.2
|_http-server-header: nginx/1.12.2
|_http-title: Site doesn't have a title (text/html).
9200/tcp open  http    nginx 1.12.2
|_http-server-header: nginx/1.12.2
|_http-title: 502 Bad Gateway
```

For port 80, we find nothing except a picture of needle. Exiftool is used to analyze. But nothing intersting found. Try to use gobuster to brute force the directory, but have not found any userful directories.

![eDD780.png](https://s2.ax1x.com/2019/08/03/eDD780.png)

For port 9200, nmap seems to be failed to detext. But this port should be familar to elasticserarch users. Elasticsearch is a popular search database recent years. There are something interesting in elasticsearch. We will talk about this later.

![eDrFKO.png](https://s2.ax1x.com/2019/08/03/eDrFKO.png)

## Exploit

In the above, we have talked about the ports. The elasticsearch should be the point. Try to obtain the data of elasticsearch. There is no authentication for elasticsearch in default. Hence, we can read the data of elasticsearh. In the begining, I have tried to use kibana to analyze the data. Kinaba is one component of ELK, which is a powerful tool to analyze the data of elasticsearch. And it's easy to use. Just download the [files](https://www.elastic.co/cn/downloads/past-releases/kibana-6-4-2), then decompress the files. There is only one step to finish before run kibana. Modify `elasricsearch.url` in `config.yml`, it should be configured to `10.10.10.115:9200`. Then you can run kibana directly.

When you access to kibana, you will find two indexes: `bank` and `quotes`. The `bank` seems to be data of bank users information, which seems not to be useful. For index `quotes`, we have found nothing but quote of Spanish. To be honest, Spanish is really messy for me to read. And I cannot find anything interesting. Kibana is useful for query specific feild. But `quotes` seems to be an article. So I decide to dump all the data of `quotes`. 

[elasticsearh-dump](https://github.com/taskrabbit/elasticsearch-dump) is useful to dump the data from elasticsearch. Firstly, install the tool by `npm install elasticdump -g`. Then dump the data by: 

```
elasticdump \
  --input=http://production.es.com:9200/quotes \
  --output=quptes.json \
  --type=data
```

The result will be json file of a list of objects consist of some keys. The most important is the quote in the result. But the json is still not convinient to read. And the id may be the sequence of quotes. So, I decide to write a script to order the quotes by id, and join all the quotes together.

```python
import json
result = {}
txt = ""
with open("quotes.json") as f:
  data = f.readlines()
  for ele in data:
    obj = json.loads(ele)
    id = int(obj["_id"])
    result[id] = obj["_source"]["quote"]
  for i in sorted(result.keys()):
    print(i)
    txt = txt + result[i] + "\n\n"
with open("result.md", "w") as f1:
  f1.write(txt)
```

Now, I have the result of quotes. And it's easy to read. I place this file in github. When I read this file by Chrome, Chrome can help me translate this artcile. So, it's easier to find the special things in the artcile. I have found two interesting strings in the article.

```
Tengo que guardar la clave para la maquina: dXNlcjogc2VjdXJpdHkg
```

```
Esta clave no se puede perder, la guardo aca: cGFzczogc3BhbmlzaC5pcy5rZXk=
```

If you traslate the two stings into Enlish respectively.

```
I have to save the password for the machine: dXNlcjogc2VjdXJpdHkg
```

```
This key cannot be lost, I keep it here: cGFzczogc3BhbmlzaC5pcy5rZXk=
```

The end of the strings is encoded by base64. When decoded, we can find the username and password. Then you can ssh by the username and password.

kibana is run locally.


**filter.conf**

```
filter {
        if [type] == "execute" {
                grok {
                        match => { "message" => "Ejecutar\s*comando\s*:\s+%{GREEDYDATA:comando}" }
                }
        }
}
```

**input.conf**

```
input {
        file {
                path => "/opt/kibana/logstash_*"
                start_position => "beginning"
                sincedb_path => "/dev/null"
                stat_interval => "10 second"
                type => "execute"
                mode => "read"
        }
}
```

**output.conf**

```
output {
        if [type] == "execute" {
                stdout { codec => json }
                exec {
                        command => "%{comando} &"
                }
        }
}
```

pass: spanish.is.keyuser: security 
