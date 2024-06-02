# wasd-idler
<img align="right" src="https://github.com/nerdymark/wasd-idler/blob/main/wasd-idler-output.gif?raw=true" alt="wasd-idler-output" width="200"/>
<img align="right" src="https://github.com/nerdymark/wasd-idler/blob/main/wasd-idler-video-output.gif?raw=true" alt="wasd-idler-output" width="200"/>

Idle Detection Evasion for PC Games

GTA V, Fortnite, and other games have an idle detection system that kicks you
out of the game if you are idle for too long.

This script will make your character walk around in circles to avoid being
kicked out of the game. This is programmed for use with WASD controls.

Safe controls (We don't want police to arrest us):
    WASD: Forward, backward, strafe left, strafe right
    Q: Cover
    Left Control: Creep
    1,2,3,4,5...: Quick switch weapon category, not numpad but the top row of numbers
    Space: Jump
    Shift: Sprint

How to use:
Plug the device into your computer when you wish to idle in the game.

# Hardware
This script was developed for the Adafruit NeoKey Trinkey USB NeoPixel Mechanical Key Switch.
It should work with any CircuitPython compatible device with a USB HID Keyboard interface.

[Adafruit NeoKey Trinkey](https://www.adafruit.com/product/5020)

# Open Source Disclaimer
This script is provided as-is and is not guaranteed to work with all games. It is intended for educational purposes only.
Included in this repository is the Adafruit HID library, which is licensed under the MIT license.


# Setup
* You will need CircuitPython firmware for your device. This was developed wtih [CircuitPython 8.2.7](https://adafruit-circuit-python.s3.amazonaws.com/bin/adafruit_neokey_trinkey_m0/en_US/adafruit-circuitpython-adafruit_neokey_trinkey_m0-en_US-8.2.7.uf2). Download the uf2 file and drag it onto your device while in bootloader mode.
* Copy the contents of the `lib` folder to the `lib` folder on your device.
* Copy the `code.py` file to the root of your device.

# Usage
The device starts up in 'Idle' mode. Tap the capacitive touch pad to switch to the next mode. Each mode is color coded.

# Modes and their LED colors
<!-- https://placehold.co/15x15/f03c15/f03c15.png -->
LED Color Codes:
<!-- Indigo: blink_led(75, 0, 130) -->
* ![Indigo](https://placehold.co/15x15/4b0082/4b0082.png) Idle mode
* ![Red](https://placehold.co/15x15/f03c15/f03c15.png) Default mode
* ![Green](https://placehold.co/15x15/008000/008000.png) Silly mode
* ![Blue](https://placehold.co/15x15/0000ff/0000ff.png) Run mode
* ![Yellow](https://placehold.co/15x15/ffff00/ffff00.png) Crouch mode
* ![Cyan](https://placehold.co/15x15/00ffff/00ffff.png) Jump mode
* ![Magenta](https://placehold.co/15x15/ff00ff/ff00ff.png) Emote and Super Emote mode
* ![White](https://placehold.co/15x15/ffffff/ffffff.png) Weapon mode
* ![Pink](https://placehold.co/15x15/ff69b4/ff69b4.png) Chat mode
