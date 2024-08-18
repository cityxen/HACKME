# 🌆🅲🅸🆃🆈🆇🅴🅽☯️ 8 & 16 bit hijinx and programming!

# Click-A-Tron
## Raspberry Pi middleware interface that allows vintage computers to use relay boards

More details here:
http://cityxen.net/2022/04/the-hackme-click-o-tron/


This is a python script that runs when the Raspberry Pi boots. It listens on the rs-232 serial port at 9600 baud for 16 character strings of 1 and 0.

### Example of input from vintage computers:
```
1110000101010001
0000000000000001
```

### Setup:
Clone (or download) this repo, into /home/pi/HACKME, then add the following line to your /etc/crontab file
```
@reboot root python /home/pi/HACKME/Click-A-Tron/Click-A-Tron.py [options]
```

### Usage:
```
python Click-A-Tron.py -s /dev/ttyAMA0 -b 1200 -t 1 -e 16B
python Click-A-Tron.py -s /dev/ttyUSB1 -b 9600 -t 1 -e 16B
python Click-A-Tron.py -b 19200 -t 1 -e 16B
python Click-A-Tron.py
```

![cat1](https://github.com/cityxen/HACKME/blob/main/Click-A-Tron/images/1%20(1).jpg)
![cat2](https://github.com/cityxen/HACKME/blob/main/Click-A-Tron/images/1%20(3).jpg)
![cat3](https://github.com/cityxen/HACKME/blob/main/Click-A-Tron/images/1%20(11).jpg)

