import os

SERVICE_FILE = '/etc/systemd/system/PIAirQuality.service'

os.system('pip3 install --editable PIAirQuality')

if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        username = input("ADAFRUIT_IO_USERNAME=")
        f.write(f'ADAFRUIT_IO_USERNAME="{username}"\n')
        key = input("ADAFRUIT_IO_KEY=")
        f.write(f'ADAFRUIT_IO_KEY="{key}"\n')
        feed = input("ADAFRUIT_IO_FEED=")
        f.write(f'ADAFRUIT_IO_FEED="{feed}"\n')
        device = input("SERIAL_DEVICE=")
        f.write(f'SERIAL_DEVICE="{device}"\n')

with open(SERVICE_FILE, 'w') as f:
    f.write("""[Unit]
Description=Pi Air Quality Service
After=multi-user.target
 
[Service]
Type=simple
ExecStart=/usr/bin/python3 -u -m PIAirQuality
Restart=always
EnvironmentFile=/home/pi/PIAirQuality/.env
User=pi
StandardOutput=inherit
StandardError=inherit
 
[Install]
WantedBy=multi-user.target""")

os.system("sudo systemctl daemon-reload")
os.system("sudo systemctl enable PIAirQuality.service")
os.system("sudo systemctl restart PIAirQuality.service")