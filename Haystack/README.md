# HayStack

## Introduction

HayStack is an easy box in hack the box. But it does isn't easy to find the user. It's annoying to find the user and password in the messy Spanish. Hence, many think this box is quite CTF.

## Information Enumeration

As usual, nmap is utilized to detect detailed ports and services.

For port 9200, it should be familar to elasticserarch user. Elasticsearch is a popular search database recent years. There are something interesting in elasticsearch. We will talk about this later.

For port 80, we find nothing except a picture of needle. Exiftool is used to analyze. But nothing intersting found. Try to use gobuster to brute force the directory, but have not found any userful directories.

## Exploit

In the above, we have talked about the ports. The elasticsearch should be the point. Try to obtain the data of elasticsearch. There is no authentication for elasticsearch in default. Hence, we can read the data of elasticsearh. In the begining, I have tried to use kibana to analyze the data. Kinaba is one component of ELK, which is a powerful tool to analyze the data of elasticsearch. And it's easy to use. Just download the [files](https://www.elastic.co/cn/downloads/past-releases/kibana-6-4-2), then decompress the files. There is only one step to finish before run kibana. Modify `elasricsearch.url` in `config.yml`, it should be configured to `10.10.10.115:9200`. Then run it by

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
