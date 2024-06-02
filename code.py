"""
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

"""
import time
import random
import board  # type: ignore
import touchio
import usb_hid
import neopixel  # type: ignore
from adafruit_hid.keyboard import Keyboard  # type: ignore
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS  # type: ignore
from adafruit_hid.keycode import Keycode  # type: ignore
import gc


QUOTES_FILE = 'quotes.txt'

time.sleep(5)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixels.brightness = 0.3


try:
    touch = touchio.TouchIn(board.TOUCH)
except AttributeError:
    touch = None

walk_keys = [Keycode.W, Keycode.D, Keycode.S, Keycode.A]
weapon_keys = [Keycode.ONE,
               Keycode.TWO,
               Keycode.THREE,
               Keycode.FOUR,
               Keycode.FIVE,
               Keycode.SIX,
               Keycode.SEVEN,
               Keycode.EIGHT,
               Keycode.NINE,
               Keycode.ZERO]
crouch_key = Keycode.Q
caps_lock_key = Keycode.CAPS_LOCK
creep_key = Keycode.LEFT_CONTROL
jump_key = Keycode.SPACE
sprint_key = Keycode.LEFT_SHIFT
all_keys = walk_keys + [crouch_key, caps_lock_key, creep_key, jump_key, sprint_key] + weapon_keys


def get_random_quote():
    with open(QUOTES_FILE, 'r') as file:
        quotes = file.readlines()
        return random.choice(quotes)


def tsleep(seconds):
    start = time.monotonic()
    while time.monotonic() - start < seconds:
        if touch.value:
            keyboard.release_all()
            return


def blink_led(r, g, b):
    pixels.fill((r, g, b))
    tsleep(0.5)
    pixels.fill((0, 0, 0))
    tsleep(0.5)


def press_and_release(pkey, quick=False):
    keyboard.press(pkey)

    if not quick:
        tsleep(0.1)
    else:
        time.sleep(0.1)

    keyboard.release(pkey)


def double_tap(dkey):
    press_and_release(dkey, quick=True)
    tsleep(0.1)
    press_and_release(dkey, quick=True)
    keyboard.release_all()


def idle_message():
    print("idle_message")
    dice = random.randint(0, 100)
    if dice < 10:
        keyboard.release(Keycode.CAPS_LOCK)

        message = get_random_quote()
        press_and_release(Keycode.T)
        keyboard_layout.write(message)
        press_and_release(Keycode.ENTER)
        gc.collect()


def silly_time():
    print("silly_time")
    while not touch.value:
        for i in range(0, 5):
            random.choice(all_keys)
            press_and_release(random.choice(all_keys), quick=True)
            tsleep(0.1)
    keyboard.release_all()


def walk_run():
    print("walk_run")
    while not touch.value:
        for wkey in walk_keys:
            # Random choice run or walk
            dice = random.randint(0, 100)
            if dice < 50:
                keyboard.press(sprint_key)
                press_and_release(wkey)
                press_and_release(wkey)
                keyboard.release(sprint_key)
            else:
                press_and_release(wkey)
                press_and_release(wkey)
    keyboard.release_all()

def run_forward():
    print("run_forward")
    keyboard.press(sprint_key)
    press_and_release(Keycode.W)
    press_and_release(Keycode.W)
    keyboard.release(sprint_key)


def crouch():
    print("crouch")
    press_and_release(crouch_key)


def creep():
    print("creep")
    press_and_release(creep_key)


def jump():
    print("jump")
    press_and_release(jump_key)


def emote():
    print("emote")
    press_and_release(caps_lock_key)
    press_and_release(caps_lock_key)


def super_emote():
    print("super_emote")
    double_tap(caps_lock_key)


def weapon_scroll():
    print("weapon_scroll")
    for wkey in weapon_keys:
        press_and_release(wkey, quick=True)


"""
Main loop for idle detection evasion.

LED Color Codes:
- Indigo: Idle mode
- Red: Default mode
- Green: Silly mode
- Blue: Run mode
- Yellow: Crouch mode
- Cyan: Jump mode
- Magenta: Emote mode
- White: Weapon mode
- Pink: Chat mode
"""

for x in range(0, 255):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    pixels.fill((r, g, b))

print("Starting Idle Detection Evasion")

while True:
    # Idle mode
    while not touch.value:
        print("idle")
        tsleep(0.1)
        blink_led(75, 0, 130)
        if touch.value:
            time.sleep(2)
            break

    # Default mode
    while not touch.value:
        mode_actions = [
            walk_run,
            crouch,
            jump,
            emote,
            super_emote,
            emote,
            run_forward,
            idle_message,
            silly_time,
            weapon_scroll]
        action = random.choice(mode_actions)
        action()
        blink_led(255, 0, 0)
        if touch.value:
            time.sleep(2)
            break

    # Silly mode
    while not touch.value:
        blink_led(0, 255, 0)
        silly_time()
        blink_led(0, 255, 0)
        if touch.value:
            time.sleep(2)
            break

    # Run mode
    while not touch.value:
        run_forward()
        blink_led(0, 0, 255)
        if touch.value:
            time.sleep(2)
            break

    # Crouch mode
    while not touch.value:
        crouch()
        blink_led(255, 255, 0)
        if touch.value:
            time.sleep(2)
            break

    # Jump mode
    while not touch.value:
        jump()
        blink_led(0, 255, 255)
        if touch.value:
            time.sleep(2)
            break

    # Emote mode 
    while not touch.value:
        emote()
        blink_led(255, 0, 255)
        if touch.value:
            time.sleep(2)
            break

    # Super emote mode
    while not touch.value:
        super_emote()
        blink_led(255, 0, 255)
        if touch.value:
            time.sleep(2)
            break

    # Weapon mode
    while not touch.value:
        weapon_scroll()
        blink_led(255, 255, 255)
        if touch.value:
            time.sleep(2)
            break
    
    # Chat mode
    while not touch.value:
        idle_message()
        blink_led(255, 0, 255)
        if touch.value:
            time.sleep(2)
            break
