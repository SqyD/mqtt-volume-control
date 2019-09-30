# mqtt-volume-control
A simple mqtt client to control audio volume

## What this project does:
* Control and report back audio volume levels using mqtt
* Control alsa mixer levels
* Control PT2259 based digital potentiometer over i2c
* Make it work with my Home Assistant setup. https://www.home-assistant.io

I build this to fit my own use case. Maybe it's of use to others.
I used this project for inspiration: https://github.com/Thyraz/snips-volume
Some C code examples for the PT2259 chip: https://forum.arduino.cc/index.php?topic=543100.0
The PT2259 datasheet: http://www.wlxmall.com/images/item_pdf_new/20180427/L20173131/PT2259-S-en.pdf
