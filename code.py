"""
Idle Detection Evasion for PC Games

GTA V, Fortnite, and other games have an idle detection system that kicks you 
out of the game if you are idle for too long.

This script will make your character walk around in circles to avoid being 
kicked out of the game. This is programmed for use with WASD controls.

Safe controls (We don't want police to arrest us):
    WASD: Forward, backward, strafe left, strafe right
    Q: Cover
    1,2,3,4,5: Quick switch weapon category

How to use:
Plug the device into your computer when you wish to idle in the game.
"""
import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def morse_code(message):
    """
    Decode text to morse code and blink the LED

    Args:
        message (string): A text string to decode into morse code.
    
    Returns:
        None, LED is blinked on the hardware.
    """

    print("Decoding message: " + message)
    character_map = [
        { "letter": "a", "code": ".-" },
        { "letter": "b", "code": "-..." },
        { "letter": "c", "code": "-.-." },
        { "letter": "d", "code": "-.." },
        { "letter": "e", "code": "." },
        { "letter": "f", "code": "..-." },
        { "letter": "g", "code": "--." },
        { "letter": "h", "code": "...." },
        { "letter": "i", "code": ".." },
        { "letter": "j", "code": ".---" },
        { "letter": "k", "code": "-.-" },
        { "letter": "l", "code": ".-.." },
        { "letter": "m", "code": "--" },
        { "letter": "n", "code": "-." },
        { "letter": "o", "code": "---" },
        { "letter": "p", "code": ".--." },
        { "letter": "q", "code": "--.-" },
        { "letter": "r", "code": ".-." },
        { "letter": "s", "code": "..." },
        { "letter": "t", "code": "-" },
        { "letter": "u", "code": "..-" },
        { "letter": "v", "code": "...-" },
        { "letter": "w", "code": ".--" },
        { "letter": "x", "code": "-..-" },
        { "letter": "y", "code": "-.--" },
        { "letter": "z", "code": "--.." },
    ]
    for letter in message:
        for character in character_map:
            if letter == character["letter"]:
                for code in character["code"]:
                    if code == ".":
                        print(code)
                        led.value = True
                        time.sleep(0.1)
                        led.value = False
                        time.sleep(0.1)
                    elif code == "-":
                        print(code)
                        led.value = True
                        time.sleep(0.3)
                        led.value = False
                        time.sleep(0.1)
                    else:
                        print("")
                        time.sleep(0.3)
                time.sleep(0.3)
        time.sleep(0.7)


def press_and_release(key):
    """
    Press and release a key

    Args:
        key (Keycode): The key to press and release.
    
    Returns:
        None, key is pressed and released on the hardware.
    """
    keyboard.press(key)
    time.sleep(1.0)
    keyboard.release(key)


walk_keys = [Keycode.W, Keycode.S, Keycode.A, Keycode.D]
crouch_key = Keycode.Q
        

while True:
    # Walk (strafe) in a circle, crouch at every turn, morse_code the keypresses
    for key in walk_keys:
        press_and_release(key)
        if key == Keycode.W:
            morse_code("w")
        elif key == Keycode.S:
            morse_code("s")
        elif key == Keycode.A:
            morse_code("a")
        elif key == Keycode.D:
            morse_code("d")
        press_and_release(crouch_key)
        morse_code("q")
