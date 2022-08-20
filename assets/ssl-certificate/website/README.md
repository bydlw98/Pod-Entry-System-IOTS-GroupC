## Creating SSL Certificate

Command to generate a self signed SSL Certificate using Openssl

    openssl req -x509 --newkey rsa:4096 --out cert.pem --keyout key.pem --days 365 -subj "/C=SG/ST=Singapore/L=Singapore/O=Secure IoT Pte Ltd/OU=Education/CN=localhost/emailAddress=."

A Makefile has been provided to easily generate a self signed certificate

    make

### For Windows Users

#### MINGW or MSYS2 make
    make SHELL=cmd.exe
This is because git bash or msys2 shell will treat /C in -subj flag as C:\

#### Visual Studio
Open up Developer Command Prompt and run

    nmake -f Makefile.vc
