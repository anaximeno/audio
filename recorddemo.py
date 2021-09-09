#!/usr/bin/env python3

tqdm_available: bool = False

try:
    from tqdm import tqdm
    tqdm_available = True
except ImportError:
    pass

import pyaudio
import wave
import os
from time import sleep


def record(seconds: int, format, channels: int, rate: int, chunk: int, *, save: bool = True, name: str = 'output.wav') -> None:
    """Records the audio and save it inside the file named `name` if `save` is set to True.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    secs = round(rate / chunk * seconds)
    if tqdm_available is True:
        loop = tqdm(range(0, secs), desc='Recording', ncols=60, bar_format='{desc} ({remaining_s})s: |-{bar}-|')
    else:
        print(" Recording ...")
        loop = range(0, secs)

    os.system('clear')
    sleep(0.1)
    frames = [stream.read(chunk) for _ in loop]
    stream.stop_stream()
    p.terminate()

    if tqdm_available is False:
        print(" Done Recording!")

    if save is True:
        with wave.open(name, 'wb') as wf:
          wf.setnchannels(channels)
          wf.setsampwidth(p.get_sample_size(format))
          wf.setframerate(rate)
          wf.writeframes(b''.join(frames))


if __name__ == '__main__':
    CHUNK: int = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS: int = 2
    RATE: int = 44100
    RECORD_SECONDS: int = 5
    WAVE_OUTPUT_FILENAME: str = "output.wav"

    record(RECORD_SECONDS, FORMAT, CHANNELS, RATE, CHUNK, save=True, name='output.wav')
