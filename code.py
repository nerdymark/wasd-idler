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
from time import sleep, monotonic
from random import randint, choice
import board  # type: ignore
import touchio
import usb_hid
import neopixel  # type: ignore
from adafruit_hid.keyboard import Keyboard  # type: ignore
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS  # type: ignore
from adafruit_hid.keycode import Keycode  # type: ignore


# Sleep magic numbers
QUICK_SLEEP_TIME = 0.1  # Default sleep time for actions
LONG_SLEEP_TIME = 1.0  # Longer sleep time for actions

sleep(LONG_SLEEP_TIME * 5)  # Initial delay to allow setup

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixels.brightness = 0.1


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
honk_key = Keycode.E

# Touch debouncing globals
DEBOUNCE_TIME = 0.2  # 200ms debounce
last_touch_time = 0
last_touch_state = False


def get_debounced_touch():
    """Get debounced touch state to prevent spurious triggers."""
    global last_touch_time, last_touch_state

    if not touch:  # Handle case where touch sensor doesn't exist
        return False

    current_time = monotonic()
    current_touch = touch.value

    # If touch state changed, update timestamp
    if current_touch != last_touch_state:
        last_touch_time = current_time
        last_touch_state = current_touch
        return False  # Don't register change until debounce period passes

    # If state has been stable for debounce time, return the state
    if current_time - last_touch_time >= DEBOUNCE_TIME:
        return current_touch

    return False  # Still in debounce period


def keyboard_action(func):
    """Decorator to ensure keyboard actions start and end cleanly."""
    def wrapper(*args, **kwargs):
        keyboard.release_all()  # Start clean
        try:
            return func(*args, **kwargs)
        finally:
            keyboard.release_all()  # End clean
    return wrapper


def tsleep(seconds):
    """Sleep for a specified number of seconds, checking touch sensor."""
    start = monotonic()
    while monotonic() - start < seconds and not get_debounced_touch():
        pass
    keyboard.release_all()


def blink_led(r, g, b):
    """Blink the neopixel LED with specified RGB color."""
    pixels.fill((r, g, b))
    tsleep(QUICK_SLEEP_TIME)
    pixels.fill((0, 0, 0))
    tsleep(QUICK_SLEEP_TIME)


@keyboard_action
def press_and_release(pkey, quick=False):
    """Press and release a key with an optional quick release."""
    keyboard.press(pkey)
    if not quick:
        tsleep(QUICK_SLEEP_TIME)
    else:
        tsleep(LONG_SLEEP_TIME)


@keyboard_action
def double_tap(dkey):
    """Double tap a key with a quick release."""
    press_and_release(dkey, quick=True)
    tsleep(QUICK_SLEEP_TIME)
    press_and_release(dkey, quick=True)


@keyboard_action
def walk_run():
    """Simulate walking or running based on a random choice."""
    print("walk_run")
    start = monotonic()
    while not get_debounced_touch() and monotonic() - start < 5:
        for wkey in walk_keys:
            # Random choice run or walk
            dice = randint(0, 100)
            if dice < 50:
                keyboard.press(sprint_key)
                press_and_release(wkey)
                keyboard.release(sprint_key)
            else:
                press_and_release(wkey)


@keyboard_action
def run_forward():
    """Simulate running forward until touch sensor is activated or timeout."""
    print("run_forward")
    start = monotonic()
    while not get_debounced_touch() and monotonic() - start < 5:
        keyboard.press(sprint_key)
        press_and_release(Keycode.W)
        keyboard.release(sprint_key)


@keyboard_action
def jump():
    """Simulate jumping until touch sensor is activated or timeout."""
    print("jump")
    start = monotonic()
    while not get_debounced_touch() and monotonic() - start < 5:
        keyboard.press(sprint_key)
        keyboard.press(Keycode.W)
        keyboard.press(jump_key)
        tsleep(QUICK_SLEEP_TIME)
        keyboard.release(jump_key)
        keyboard.release(Keycode.W)
        keyboard.release(sprint_key)


@keyboard_action
def emote():
    """Simulate an emote action by pressing the caps lock key."""
    print("emote")
    press_and_release(caps_lock_key)
    tsleep(LONG_SLEEP_TIME)


@keyboard_action
def super_emote():
    """Simulate a super emote action by double-tapping the caps lock key."""
    print("super_emote")
    double_tap(caps_lock_key)
    tsleep(LONG_SLEEP_TIME)


@keyboard_action
def weapon_scroll():
    """Simulate scrolling through weapons by pressing weapon keys."""
    print("weapon_scroll")
    for wkey in weapon_keys:
        press_and_release(wkey, quick=True)
        tsleep(QUICK_SLEEP_TIME)


@keyboard_action
def annoy_o_honk():
    """Simulate an annoying honking action by pressing the honk key repeatedly."""
    print("annoy_o_honk")
    start = monotonic()

    for i in range(1, 101):
        # Exit conditions at start of each iteration
        # if touch.value or monotonic() - start >= 5:
        if get_debounced_touch() or monotonic() - start >= 5:
            break

        if i % 10 == 0:
            tsleep(LONG_SLEEP_TIME)
            continue  # Check exit conditions again after sleep

        keyboard.press(honk_key)
        tsleep(LONG_SLEEP_TIME / i)
        keyboard.release(honk_key)


while True:
    # Idle mode
    while not get_debounced_touch():
        print("idle")
        tsleep(QUICK_SLEEP_TIME)
        blink_led(255, 0, 0)
        if get_debounced_touch():
            tsleep(QUICK_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)

    # Default mode
    while not get_debounced_touch():
        mode_actions = [
            walk_run,
            jump,
            emote,
            super_emote,
            emote,
            run_forward,
            weapon_scroll]
        action = choice(mode_actions)
        action()
        blink_led(255, 165, 0)
        tsleep(LONG_SLEEP_TIME * 2)
        break
    sleep(LONG_SLEEP_TIME)

    # Run mode
    while not get_debounced_touch():
        run_forward()
        blink_led(0, 255, 0)
        if get_debounced_touch():
            tsleep(LONG_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)

    # Jump mode
    while not get_debounced_touch():
        jump()
        blink_led(75, 0, 130)
        if get_debounced_touch():
            tsleep(LONG_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)

    # Emote mode
    while not get_debounced_touch():
        emote()
        super_emote()
        blink_led(148, 0, 211)
        if get_debounced_touch():
            tsleep(LONG_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)

    # Weapon mode
    while not get_debounced_touch():
        weapon_scroll()
        blink_led(255, 255, 255)
        if get_debounced_touch():
            tsleep(LONG_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)

    # Annoy-o-honk mode
    while not get_debounced_touch():
        annoy_o_honk()
        blink_led(255, 165, 0)
        if get_debounced_touch():
            tsleep(LONG_SLEEP_TIME * 2)
            break
    sleep(LONG_SLEEP_TIME)
