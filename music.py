import multiprocessing
from playsound import playsound
from time import sleep

import sounds

manager = multiprocessing.Manager()
loop_sound = manager.list()
loop_busy = False
sound_list = []


def loop():
    i = 0
    global loop_sound
    global loop_busy
    while True:
        if loop_sound and not loop_busy:
            for _ in range(4):
                playsound(f'{loop_sound[0]}.wav', block=False)
                sleep(4)
            loop_sound.pop(0)
            loop_busy = False
        #sleep(1)


def scan():
    global loop_sound
    global loop_busy
    while True:
        sound_input = input('Input sound: ')
        sound_list.append(sound_input)
        print(len(sound_list))
        if len(sound_list) > 1 and not loop_busy:
            if sound_list[-1] == sound_list[-2]:
                print(f'Looping sound: {sound_list[-1]}')
                loop_sound.append(sound_list[-1])
                loop_busy = True
            else:
                playsound(f'{sound_input}.wav', block=False)
        if len(sound_list) <= 1:
            playsound(f'{sound_input}.wav', block=False)
            #print('sound to play')
            #playsound(f'{sound_input}.wav', block=False)


if __name__ == '__main__':
    # p1 = multiprocessing.Process(target=scan)
    p2 = multiprocessing.Process(target=loop)
    # p1.start()
    p2.start()
    while True:
        scan()
