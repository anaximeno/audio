#!/usr/bin/env python3
import argparse
import pyaudio
import wave
import os


CHUNK: int = 1024
FORMAT: int = pyaudio.paInt16
CHANNELS: int = 2
RATE: int = 44100
RECORD_SECONDS: int = 5
WAVE_OUTPUT_FILENAME: str = "output.wav"


try:
    # 'tqdm' is used to show progress bar when recording,
    # so if it isn't installed no progress bar will be shown
    from tqdm import tqdm
    tqdm_available = True
except ImportError:
    tqdm_available = False

required_modules = []
try:
    import pyaudio
except ImportError:
    required_modules.append('pyaudio')
try:
    import wave
except ImportError:
    required_modules.append('wave')


if any(required_modules):
    print('You must install the following modules before using this program: ', end='')
    print(' '.join(required_modules))
    exit(1)


class Recorder(object):

    def __init__(self, channels: int, rate: int, chunk: int, audio_format: int = FORMAT, *args, **kwargs) -> None:
        """The Recorder class.
        """
        super(Recorder, self).__init__()

        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk

        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=self.audio_format, channels=self.channels,
            rate=self.rate, input=True, frames_per_buffer=self.chunk)

        if 'clear' in kwargs and kwargs['clear'] is True:
            os.system('clear')
    
    def record(self, secs: int = RECORD_SECONDS, save: bool = True, name: str = WAVE_OUTPUT_FILENAME):
        """Records the audio and save it inside the file named `name` if `save` is set to True.
        """
        steps = round(self.rate / self.chunk * (secs + 0.5))
        loop = range(0, steps)

        if tqdm_available:
            loop = tqdm(loop, desc='Recording', ncols=60, bar_format='{desc} ({remaining_s:.2f})s: |-{bar}-|')
        else:
            print('Init Recording(..)')
        
        frames = [self.stream.read(self.chunk) for _ in loop]
        self.stream.stop_stream()
        self.pyaudio.terminate()

        if save is True:
            self.save(frames, name)

        return (frames, self.rate, self.chunk, self.channels)
        
    def save(self, frames: list, name: str):
        with wave.open(name, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
        print(f'Saved {str(name)!r}!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('audio')

    parser.add_argument('--nsecs', type=int, required=False, help='Determine how many seconds to record the audio')
    parser.add_argument('--rate', type=int, required=False, help='Determine the rate of the recording')
    parser.add_argument('--channels', type=int, required=False, help='Determine the number of channels of the audio')
    parser.add_argument('--chunks', type=int, required=False, help='Determine the chunks of the audio')
    parser.add_argument('-s', '--save', action='store_true', help='Save the audio file.')
    parser.add_argument('-n', '--name', type=str, help='Name of the file to be stored.')
    parser.add_argument('--no-warns', '--no_warns', action='store_true', required=False, help='If set clear the sys warnings before recording the audio')

    args = parser.parse_args()

    record_seconds = args.nsecs if args.nsecs else RECORD_SECONDS
    rate = args.rate if args.rate else RATE
    channels = args.channels if args.channels else CHANNELS
    chunks = args.chunks if args.chunks else CHUNK
    savename = args.name if args.name else WAVE_OUTPUT_FILENAME

    rec = Recorder(channels, rate, chunks, clear=args.no_warns)
    output = rec.record(record_seconds, args.save, savename)
