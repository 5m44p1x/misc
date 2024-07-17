#!/usr/bin/python3
import time
import math
from pyaudio import PyAudio

freq = 26160 # Hz
amp = 0.05 # between 0 to 1
dotLength = 0.1 # seconds
dashLength = dotLength * 3
pauseWords = dotLength * 7

alphaToMorse = {'a': ".-", 'b': "-...", 'c': "-.-.", 'd': "-..", 'e': ".",
                'f': "..-.", 'g': "--.", 'h': "....", 'i': "..", 'j': ".---", 'k': "-.-",
                'l': ".-..", 'm': "--", 'n': "-.", 'o': "---", 'p': ".--.", 'q': "--.-",
                'r': ".-.", 's': "...", 't': "-", 'u': "..-", 'v': "...-", 'w': ".--",
                'x': "-..-", 'y': "-.--", 'z': "--..",
                '1': ".----", '2': "..---", '3': "...--", '4': "....-", '5': ".....",
                '6': "-....", '7': "--...", '8': "---..", '9': "----.", '0': "-----",
                ' ': "/", '.': ".-.-.-", ',': "--..--", '?': "..--..", "'": ".----.",
                '@': ".--.-.", '-': "-....-", '"': ".-..-.", ':': "---...", ';': "---...",
                '=': "-...-", '!': "-.-.--", '/': "-..-.", '(': "-.--.", ')': "-.--.-",
                'á': ".--.-", 'é': "..-.."}

def morsecode():
    """
    converts text to morse code.
    prints result and calls morseaudio.
    """
    while True:
        message = ' '.join(input(">").strip().split())
        # if you enter nothing, exits method
        if message == "":
            return

        # remembers characters that do not have standard morse code equivalent
        unabletoconvert = ""
        morse = ""
        for char in message.lower():
            if char in alphaToMorse:
                morse += alphaToMorse[char] + ' '
            else:
                unabletoconvert += char
        if len(unabletoconvert) != 0:
            print("These characters are unable to be converted:\n" + ' '.join(unabletoconvert))
        morse = morse[:-1]
        print(morse)
        morseaudio(morse)

def beep(duration, frequency=freq, amplitude=amp):
    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 16000 #number of frames per second/frameset.

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    FREQUENCY = frequency #Hz, waves per second
    LENGTH = duration #seconds to play sound

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''

    for x in range(NUMBEROFFRAMES):
        WAVEDATA += chr(int(amplitude * math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128))

    #fill remainder of frameset with silence
    for x in range(RESTFRAMES):
        WAVEDATA += chr(128)

    p = PyAudio()
    stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=BITRATE,
        output=True,
        )
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()

def pause(duration):
    """
    pauses audio for duration seconds
    :param duration: duration of pause in seconds
    """
    time.sleep(duration)

def morseaudio(morse):
    """
    plays audio conversion of morse string using inbuilt windows module.
    :param morse: morse code string.
    """
    for char in morse:
        if char == ".":
            beep(dotLength)
        elif char == "-":
            beep(dashLength)
        elif char == "/":
            pause(pauseWords)
        else:
            # char is blank space
            pause(dashLength)

morsecode()
