#!/usr/bin/python3

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


# Using the `with` method to open file, which is more secure
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("* recording")
frames = [
  stream.read(CHUNK) for i in range(0, int(RATE / CHUNK * RECORD_SECONDS))
]
print("* done recording")
stream.stop_stream()
p.terminate()


# Using the `with` method to open file, which is more secure
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))

