ports="40809 50212 46969"

for port in $ports; do 
    
    echo "[*] Knocking on ${port}"
    echo "a" | nc -u -w 1 10.10.10.96 ${port}
    sleep 0.1
done; 

echo "[*] Knocking done."
echo "[*] Password:"
echo "N0Pl4c3L1keH0me"

ssh -i id_rsa-oz-dorthi dorthi@10.10.10.96
