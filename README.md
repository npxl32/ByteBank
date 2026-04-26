# ByteBank
ByteBank is a project that acts as a virtual currency (without value). You can find it here: https://scratch.mit.edu/projects/1026899140/ . TurboWarp support is in progress.

## Versions
Versions will be specified as per this: The first number signifies a full change that is easier to just delete your scripts and start over, the second number signifies a client change, you will need to update your scratch client and the third number is a python scripts update you will need to update your scripts.
## Installation
Please note that this has only been tested on a raspberry pi running bookworm and buster. This might not work on all operating systems. 

Step 1:

### Modules needed: 
If you are on a raspberry pi you may need to create a virtual environment to install modules. The following modules: smtplib, py7zr, re, numpy, heapq and last but not least scratchattach V1.4.7

The rest Is comeing soon 


crontab: 
first use the command
```

0 0 * * * /home/pi/bytebank/bin/python3.11 /home/pi/Python_Projects/ByteBank/auto_sort.py && /home/pi/bytebank/bin/python3.11 /home/pi/Python_Projects/ByteBank/backups/Main_Scripts.py
```


Atomatic start:

First execute this command:

```

sudo nano /etc/systemd/system/cloud_requests.service
```

then paste:
```
[Unit]
Description=Cloud Requests Script
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/home/pi/bytebank/bin/python3.11 /home/pi/Python_Projects/ByteBank/cloud_requests.py
WorkingDirectory=/home/pi/Python_Projects/ByteBank/
StandardOutput=append:/home/pi/cloud_requests.log
StandardError=append:/home/pi/cloud_requests.err
Restart=on-failure
RestartSec=10
User=pi

[Install]
WantedBy=multi-user.target
```
save and close

last execute these 3 commands:
```
sudo systemctl daemon-reload
sudo systemctl enable cloud_requests.service
sudo systemctl start cloud_requests.service
```


sorry again for docs they will slowly get better
