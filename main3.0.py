import threading
import wave

import pyaudio
from inputimeout import inputimeout, TimeoutOccurred
from timeit import default_timer
from playsound import playsound
from sounds import sounds


def valid_sound(sound):
    for row in sounds:
        for ele in row:
            if ele == sound:
                return True
    return False


def loop_child(sound, start, length, loops):
    wave_file = wave.open(f'{sound}.wav', 'rb')

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(wave_file.getsampwidth()),
                           channels=wave_file.getnchannels(),
                           rate=wave_file.getframerate(),
                           output=True)
    # skip unwanted frames
    n_frames = int(start * wave_file.getframerate())
    wave_file.setpos(n_frames)

    # write desired frames to audio buffer
    n_frames = int(length * wave_file.getframerate())
    frames = wave_file.readframes(n_frames)
    stream.write(frames)

    for _ in range(loops):
        stream.write(frames)
        # playsound(f'{sound}.wav', block=False)

    # close and terminate everything properly
    stream.close()
    py_audio.terminate()
    wave_file.close()


def loop_one(q, start, length, loops):
    print(f'Looping sound: {q}')
    threading.Thread(target=loop_child, args=(q, start, length, loops)).start()


if __name__ == '__main__':
    while True:
        print(f'Threads: {threading.activeCount()}')
        start = default_timer()
        sound_one = input('Test scan: ')
        duration = default_timer() - start
        if duration < 1:
            start = default_timer()
            sound_two = input('Test scan: ')
            duration = default_timer() - start
            if duration < 0.5:
                start = default_timer()
                sound_three = input('Test scan: ')
                duration = default_timer() - start
                if duration < 0.5:
                    print('>>>gör snabba loopen')
                    loop_one(sound_three, 1, 5, 4)
                else:
                    continue

            else:
                print('>>>>>>>gör långsamma loopen')
                loop_one(sound_two, 2, 2, 8)
        else:
            playsound(f'{sound_one}.wav', block=False)

