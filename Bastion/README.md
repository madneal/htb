guestmount --add //10.10.10.134/backups/WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351/9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /root/htb/Bastion/VHD

mount -t cifs //10.10.10.134/Backups -o user=guest,password= /mnt/backups
