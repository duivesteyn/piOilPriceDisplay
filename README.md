# piOilPriceDisplay 2020 Design Notes
### Raspberry pi zero with epaper display that constantly presents the WTI oil price
script runs periodically, updates screen and then closes

designed to run on the half hour, every x minutes -> */x * * * * 

https://github.com/duivesteyn/piOilPriceDisplay

2020-05-21 v1.0

bmd


# BOM
- pi zero WIFI
- pimoroni pi w case
- inky phat epaper screen
- sd card

# PI Setup
## Headless installation
- SD Card Flashed with Raspberry Pi Imager.app
- /Volumes/boot/wpa_supplicant.conf file with WIFI Settings
- create blank /Volumes/boot/ssh to enable ssh access

## Access
ssh pi@piOilPriceDisplay.local

## Pre-requisites
- python3
- inkyphat library -> curl https://get.pimoroni.com/inky | bash

## Raspbian Setup
- ssh passwordless login. 
- autologin on boot to CLI.
- renamed to piOilPriceDisplay (/etc/hosts)
- user/pass pi:oilpricedisplay
- apt-get update && upgrade
- installed neofetch
- curl https://get.pimoroni.com/inky | bash
 
## Installation
1. git clone https://github.com/duivesteyn/piOilPriceDisplay    -> this puts the project into ~/piOilPriceDisplay/
3. crontab -e
4. add the following lines:
*/15 * * * * cd /home/pi/piOilPriceDisplay/ && python3 updateDisplay.py
@reboot cd /home/pi/piOilPriceDisplay/ && python3 boot.py

## Code Structure 
boot.py
 	Script that displays the Loading Screen, demonstrates internet connection and cme data pull OK. R
	
updateDisplay.py 
    Script that displays price onto screen. (and updates on subsequent runs).

getPrice.py
    Script that gets price from data provider.

## User Interface
No user accessible options, all setup done in python file.
- Loading Screen. 	Shown on Startup for 30 seconds. Visual intro to communicate what device does, link and internet connectivity
- Main Display 		Main Display updated every 30 seconds

LOADING SCREEN

    --------------------------------------------------
    |                                     2020-05-16 |
    |            piOilPriceDisplay v1.0              |
    |                                                |
    |    github.com/duivesteyn/piOilPriceDisplay     |
    |                                                | internet: -> internet: OK (if internet works)		
    |          internet:ok         Data:CME          | Data: -> Data:CME         (when the download reports status 200)
    --------------------------------------------------

MAIN DISPLAY - (Status @ $29.65/bbl)

    --------------------------------------------------
    |                                     2020-05-16 | 
    |            ____  ___     ___   ___ 		     |
    |           (___ \/ _ \   / __) / __)		     |
    |            / __/\__  )_(  _ \(___ \		     |
    |           (____)(___/(_)\___/(____/            |
    |                                                |
    --------------------------------------------------