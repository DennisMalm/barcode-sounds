import threading
import wave

import pyaudio
from inputimeout import inputimeout, TimeoutOccurred
from timeit import default_timer
from playsound import playsound


def loop_child(sound, start, length, loops):
    wave_file = wave.open(f'{sound}.wav', 'rb')

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(wave_file.getsampwidth()),
                           channels=wave_file.getnchannels(),
                           rate=wave_file.getframerate(),
                           output=True)
    # skip unwanted frames
    n_frames = int(start * wave_file.getframerate())
    #print(wave_file.getframerate())
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
    loop = []
    played_sounds = []


    total_duration = 0
    sound = None
    while True:
        while True:
            start = default_timer()
            sound = input('Test scan: ')
            duration = default_timer() - start
            played_sounds.append({'sound': sound, 'duration': duration})
            try:
                if played_sounds[-1].get('sound') == sound:
                    if duration < 0.5:
                        try:
                            sss = inputimeout(prompt='Test scan: ', timeout=0.5)
                            if sound == sss:
                                print('>>>gör snabba loopen')
                                loop_one(sound, 1, 5, 4)
                        except TimeoutOccurred:
                            print('>>>>>>>gör långsamma loopen')
                            loop_one(sound, 2, 2, 8)

            except IndexError:
                pass
            playsound(f'{sound}.wav', block=False)
            #played_sounds.append({'sound': sound, 'duration': duration})
