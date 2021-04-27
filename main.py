from playsound import playsound
from threading import Thread
import time

looping = False
last_sound_played = None

def play(sound):
    playsound(f'{sound}.wav', block=False)


def loop_sound(sound):
    global looping
    for i in range(4):
        playsound(f'{sound}.wav', block=False)
        time.sleep(4)
    looping = False


def search(sound, sound_grid):
    for row in sound_grid:
        for ele in row:
            if ele == sound:
                return True
    return False


if __name__ == '__main__':
    while True:
        sound_to_play = input("Scan a barcode right now:")
        print(search(sound_to_play, sounds))

        if search(sound_to_play, sounds):
            # loop_sound(f'{sound_to_play}')
            if sound_to_play == last_sound_played:
                loop_sound(sound_to_play)
            playsound(f'{sound_to_play}.wav', block=False)
            last_sound_played = sound_to_play
        else:
            print('No such sound.')
