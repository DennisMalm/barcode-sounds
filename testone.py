import multiprocessing
import concurrent.futures
import threading
from playsound import playsound
from time import sleep

import sounds


def loop_child(sound):
    while True:
        for _ in range(4):
            playsound(f'{sound}.wav', block=False)
            sleep(4)
        sound.task_done()


def loop_one(queue):
    while True:
        # loopings = []
        # loopings.append(sound.get())
        msg = queue.get()
        print(msg)
        #loop_child(sound.get())

        # t = threading.Thread(target=loop_child, args=(sound.get(),))
        # t.start()
            #t.join()
        # loopings.pop()


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
        if previous_sound == sound_input:
            loop_one_sound.put(sound_input)
            print(f'Looping sound: {sound_input}')
        else:
            playsound(f'{sound_input}.wav', block=False)
            previous_sound = sound_input
