import multiprocessing
from playsound import playsound
from time import sleep

import sounds


def loop_one(sound):
    global loop_one_available
    while True:
        new_sound = sound.get()
        for _ in range(4):
            playsound(f'{new_sound}.wav', block=False)
            sleep(4)
        loop_one_available.value = True


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    loop_one_sound = manager.Queue()
    loop_one_available = multiprocessing.Value('i', True)

    sound_list = manager.list()
    previous_sound = None

    pool = multiprocessing.Pool()
    loop_one_process = pool.apply_async(loop_one, (loop_one_sound,))
    while True:
        sound_input = input('Input sound: ')
        if previous_sound == sound_input and loop_one_available.value:
            loop_one_available.value = False
            loop_one_sound.put(sound_input)
            print(f'Looping sound: {sound_input}')
        else:
            playsound(f'{sound_input}.wav', block=False)
            previous_sound = sound_input
