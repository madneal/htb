for pwd in $(cat /root/SecLists/Passwords/Leaked-Databases/rockyou-75.txt)
  do openssl enc -aes-256-cbc -d -a -in drupal.txt.enc -out file.txt -k $pwd
  if [ $? -eq 0 ]
  then
    exit 1
  fi
done
