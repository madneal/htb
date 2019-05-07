set OPENSSL_CONF=.\openssl.cnf
..\openssl.exe dhparam -out dh.pem -2 1024 2> dh.log