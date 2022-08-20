# Secured-End-to-End-IoT-for-Door-Entry-System

# Requirements
1. A Python >= 3.7 above interpreter
2. Arduino IDE with support for ESP32 board

# Install
1. Copy assets/config-template to assets/config then fill in their respective values
2. Install nginx server and copy smartpod-nginx.conf in assets/nginx directory to /etc/nginx/sites-enabled/ directory.<br>
3. Inside smartpod-nginx.conf file change the /home/pi/Documents/SP/IOT-Security/IOT-Security-MiniProject/Secured-End-to-End-IoT-for-Door-Entry-System/ directory
in ssl_password_file, ssl_certificate and ssl_certificate_key parameters to where you downloaded this project to.

# Run website
Install Python Libraries in requirements.txt then run app.py file

# Run ESP32 code
open POD_SYSTEM directory in Arduino IDE and upload to ESP32 board. Do note to change the IP Address in POD_SYSTEM.ino
with IP Address of Webserver
