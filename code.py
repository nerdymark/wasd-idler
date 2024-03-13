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
import random
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

walk_keys = [Keycode.W, Keycode.D, Keycode.S, Keycode.A]
crouch_key = Keycode.Q
caps_lock_key = Keycode.CAPS_LOCK

idle_messages = [
    "I'm not idle, I'm just thinking!",
    "I'm not idle, I'm just resting my eyes!",
    "I'm not idle, I'm just taking a break!",
    "I'm not idle, I'm just stretching!",
    "I'm not idle, I'm just getting a snack!",
    "I'm not idle, I'm just getting a drink!",
    "Hey, don't shoot me!",
    "search for nerdymark wasd-idler on GitHub",
    "nerdymark's WASD Idler v1.1",
    "hi",
    "Walk with me",
    "nerdymark is now accepting modder gifts",
    "What a NERD!",
    "I'm not idle, I'm just being a nerd!",
    "I'm not idle, I'm just being a geek!",
    "I'm not idle, I'm just being a dork!",
    "Add me to your friends list",
    "On twitch I'm nerdymark408",
    "I miss twitter.",
    "Griefer Sutherland over here",
    "Hey noobs and nerds",
    "Are there cats in GTA Online yet?",
    "Hey, wait, I have a new complaint",
    "skibidi", # More memes please
    "This is a test of the emergency broadcast system",
    "This is not a test",
    "What year is it?",
    "Kobe!",
    "Skidoosh!",
    "Ka-chow!",
    "m'lady",
    "Is it safe?",
    "You sit on a throne of lies",
    "It's just a flesh wound",
    "Looks like meat's back on the menu",
    "Looks like I picked the wrong week to quit sniffing glue",
    "You're killing me, Smalls",
    "Leave the gun, take the cannoli",
    "You'll shoot your eye out, kid",
    "Bye, Felicia",
    "Sp you're telling me there's a chance",
    "Eat my shorts",
    "Exsqueeze me?",
    "Inconceivable!",
    "There's no crying in GTA Online!",
    "I'm a cotton-headed ninny muggins",
    "I'm not crying, you're crying",
    "As if",
    "Bend.... and snap!",
    "I'm in a glass case of emotion!",
    "Tina you fat lard, come get some dinner!",
    "Tiny Rick!",
    "Pickle Rick!",
    "That is my least vulnerable spot",
    "That boy's good.",
    "Keep the change, ya filthy animal.",
    "The Dude abides",
    "The snozzberries taste like snozzberries!",
    "It's official, old buddy. I'm a has-been.",
    "What's your damage?",
    "Really, really ridiculously good looking",
    "I'll have what she's having",
    "I'll be back",
    "I'm walking here!",
    "I'm the king of the world!",
    "I'm the ghost with the most, babe",
    "What? Like it's hard?",
    "It's like I have ESPN or something",
    "I'm a peacock, you gotta let me fly!",
    "I'm a leaf on the wind",
    "I'm a leaf on the wind, watch how I soar",
    "I award you no points, and may God have mercy on your soul.",
    "I see dead people",
    "I see you",
    "I see you're drinking 1%. Is that 'cause you think you're fat?",
    "Do you understand the words that are coming out of my mouth?",
    "That rug really tied the room together, did it not?",
    "You're a wizard, Harry",
    "You're a virgin who can't drive",
    "We get the warhead and we hold the world ransom for.... ONE MILLION DOLLARS",
    "We're not worthy!",
    "Bueller... Bueller... Bueller...",
    "Greater good? I'm nerdymark! I'm the greatest good you are ever gonna get!",
    "Did I stutter?",
    "Did you ever find Bugs Bunny attractive when he put on a dress?",
    "Show me the money!",
    "I'm about to do to you what Limp Bizkit did to music in the late '90s",
    "I feel comfortable using legal jargon in everyday life",
    "Vegas, baby! Vegas!",
    "I'm a loner, Dottie. A rebel.",
    "I'm not like a regular nerd, I'm a cool nerd.",
    "I got a stage 5 clinger",
    "You can't sit with us!",
    "You can't handle the truth!",
    "You complete me",
    "You had me at hello",
    "You had me at meat tornado",
    "Get in loser, we're going shopping",
    "Get in my belly!",
    "This building has to be at least... three times bigger than this!",
    "This is my BOOMSTICK!",
    "This is my rifle. There are many like it, but this one is mine.",
    "Yeah, but I shoot with this hand",
    "It's not a man purse. It's called a satchel. Indiana Jones wears one.",
    "That's why her hair is so big. It's full of secrets.",
    "That's what she said",
    "That escalated quickly",
    "Great Odin's raven!",
    "Great Scott!",
    "Great white buffalo",
    "Great success!!",
    "Great, kid. Don't get cocky",
    "Great, now you've killed the invisible swordsman!",
    "*laughs* We're laughing",
    "How can I be a fascist? I don't control the railways or the flow of commerce!",
    "How do you like them apples?",
    "How do you know if you're in love?",
    "Is that a gun in your pocket or are you just happy to see me?",
    "When life gives you lemons, just say 'F*** the lemons' and bail",
    "I don't want to ber rude, but may I have a drink? I had three of four before I got here, but they're beginning to wear off. And you know how that is",
    "I'm not a doctor, but I play one on TV",
    "Gentlemen, you can't fight in here! This is the War Room!",
    "Did you just look at me? Did you? Look at me! Look at me! How dare you! Close your eyes!",
    "Did you just grab my butt?",
    "Someday, you're gonna get b****-slapped and I'm not gonna do a thing to stop it",
    "By all means, move at a glacial pace. You know how that thrills me",
    "Pardon my french, but nerdymark is so tight that if you stuck a lump of coal up his a**, in two weeks you'd have a diamond",
    "Instead of the mahi mahi, may I just get the one mahi because I'm not that hungry?",
    "Insert coin to continue",
    "I am serious... and don't call me Shirley",
    "Snap out of it!",
    "Oh, right, to call you stupid would be an insult to stupid people. I've known sheep that could outwit you. I've worn dresses with higher IQs. But you think you're an intellectual, don't you, ape?",
    "Don't point that gun at him, he's an unpaid intern",
    "If I'm not back in five minutes... just wait longer",
    "If we get any nerds in here, this is going to be a suburb",
    "Ariel, you're under a lot of pressure. You're a princess. You've got a lot of responsibilities. People are looking up to you. You can't just run off and be a... a... a... a nerd",
    "I've had it with these motherf***ing nerds on this motherf***ing plane!",
    "This job would be great if it wasn't for the f***ing customers",
    "I'm not even supposed to be here today!",
    "I have nipples, Greg. Could you milk me?",
    "Here's the deal. I'm the best there is. Plain and simple. I wake up in the morning and I piss excellence",
    "I have a bad feeling about this",
    "You are a sad, strange little man, and you have my pity",
    "You're dizzy because you played Russian roulette with a nerf gun",
    "My fater would womanize, he would drink, he would make outrageous claims like he invented the question mark",
    "I don't want to have to read you the riot act, but I am goin g to have to read you some extracts from the riot act",
    "Please. Have mercy. I've been wearing the same underwear since Tuesday",
    "He's so fluffy I'm gonna die!",
    "One human alcohol beer, please",
    "BAT!",
    "Pablo Picasso. More like Pablo Picasshole.",
    "It says I am 100 percent nerd."
    "I don't want these virgins. They are going to taste too sad.",
    "All secret meetings take place in the fancy room.",
    "Yes, they are near. The smell of beef and sulfur is overwhelming.",
    "No, thank you, I prefer to die giving you the finger.",
    "How does it feel to be the least nerdy person at the bus station?",
    "The world is mine, your death should be quick and painless.",
    "The only reason we die is because we accept it as an inevitability.",
    "I'm not a nerd, I'm a high-functioning nerd.",
    "Mother, I come bearing a gift. I'll give you a hint. It's in my diaper and it's not a toaster.",
    "Love is like a fart. If you have to force it, it's probably s***.",
    "Whatever kills me makes me stronger.",
    "I'm not the smartest man in the world, but I can always look back on my life and say, 'I was never a nerd.'",
    "Oh, you people can kiss the fattest part of my a**.",
    "When you poop in your dreams, you poop for real.",
    "I hate to sound like every woman ever, but I am depressed.",
    "This is a man who thinks the plural of goose is sheep."
    ]
    

def morse_code(message):
    """
    Decode text to morse code and blink the LED

    Args:
        message (string): A text string to decode into morse code.
    
    Returns:
        None, LED is blinked on the hardware.
    """

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
                        led.value = True
                        time.sleep(0.1)
                        led.value = False
                        time.sleep(0.1)
                    elif code == "-":
                        led.value = True
                        time.sleep(0.3)
                        led.value = False
                        time.sleep(0.1)
                    else:
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


def double_tap(key):
    """
    Double tap a key

    Args:
        key (Keycode): The key to double tap.
    
    Returns:
        None, key is double tapped on the hardware.
    """
    press_and_release(key)
    time.sleep(0.1)
    press_and_release(key)


def idle_message():
    """
    Sends a message to the lobby.
    Every 100 runs, take a 1/10 chance of sending a message from the idle_messages list.
    """
    dice = random.randint(0, 100)
    if dice < 10:
        message = random.choice(idle_messages)
        press_and_release(Keycode.T)
        keyboard_layout.write(message)
        press_and_release(Keycode.ENTER)


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
        press_and_release(caps_lock_key)
        double_tap(caps_lock_key)
        press_and_release(caps_lock_key)
        idle_message()



