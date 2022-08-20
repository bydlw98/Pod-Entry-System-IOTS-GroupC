OPENSSL="C:/Program Files/Git/usr/bin/openssl"
KEYOUT=-keyout key.pem
OUT=-out cert.pem
SUBJECT=-subj "/C=SG/ST=Singapore/L=Singapore/O=Secure IoT Pte Ltd/OU=Education/CN=localhost/emailAddress=."
OPENSSL_FLAGS= req -x509 -newkey rsa:4096 -days 365
OPENSSL_FLAGS+= $(KEYOUT) $(OUT)
OPENSSL_FLAGS+= $(SUBJECT)

gen_ssl_certificate:
	$(OPENSSL) $(OPENSSL_FLAGS)


.PHONY: gen_ssl_certificate
