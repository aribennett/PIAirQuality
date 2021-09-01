import os

SERVICE_FILE = '/etc/systemd/system/PIAirQuality.service'

with open(SERVICE_FILE, 'w') as f:
    f.write("""[Unit]
Description=Pi Air Quality Service
After=multi-user.target
 
[Service]
Type=simple
ExecStart=/usr/bin/python3 -m PIAirQuality
Restart=always
Environment=/home/pi/PIAirQuality/.env
User=pi
 
[Install]
WantedBy=multi-user.target""")

os.system("sudo systemctl daemon-reload")
os.system("sudo systemctl enable PIAirQuality.service")