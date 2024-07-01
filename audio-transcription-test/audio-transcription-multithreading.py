"""
Transcribes according to word level

ref:https://www.youtube.com/watch?v=_spinzpEeFM
"""
import pyaudio
import numpy as np
from faster_whisper import WhisperModel
from loguru import logger
from scipy.io.wavfile import write
import threading
import time
from nltk import word_tokenize


class AudioBuffer:
    def __init__(self, rate):
        self.audio_buffer = np.array([], dtype=np.float32)
        self.lock = threading.Lock()
        self.rate = rate

    def write(self, data):
        with self.lock:
            self.audio_buffer = np.append(self.audio_buffer, data)

    def clear(self):
        with self.lock:
            self.audio_buffer = np.array([], dtype=np.float32)

    def read(self):
        return self.audio_buffer

    def trim_from_start(self, end):
        with self.lock:
            self.audio_buffer = self.audio_buffer[int(end * self.rate):]

    def __len__(self):
        return len(self.audio_buffer)


class FasterWhisperASR:
    def __init__(self, audio_buffer: AudioBuffer, rate: int, chunk: int):
        self.model = WhisperModel("small")
        self.audio_buffer = audio_buffer
        self.rate = rate
        self.next_text = ''
        self.transcriptions = []
        self.chunk = chunk

    def transcribe(self):
        while True:
            segments, info = self.model.transcribe(
                audio=self.audio_buffer.read(),
                initial_prompt=self.next_text,
                language="en",
                vad_filter=True,
            )

            text = ''

            segments = list(segments)

            if len(segments) == 0:
                time.sleep(self.chunk / self.rate)
                continue

            for segment in segments:
                text += segment.text

            # print(text)
            self.transcriptions.append(text)

            tokens = word_tokenize(text)
            if len(tokens) > 6:
                self.next_text = ' '.join(tokens[6:])
                self.audio_buffer.trim_from_start(segments[-1].end)

            # write(f'{time.time()}.wav', self.rate,
            #       (self.audio_buffer.read() * 32768).astype(np.int16))

    def get_transcription(self):
        return self.transcriptions


class Microphone:
    def __init__(self, audio_buffer: AudioBuffer, rate: int, chunk: int):
        self.audio = pyaudio.PyAudio()
        self.audio_buffer = audio_buffer
        self.rate = rate
        self.chunk = chunk

        logger.info("Microphone initialized")

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        audio_data = (np.frombuffer(
            in_data, dtype=np.int16) / 32768).astype(np.float32)
        self.audio_buffer.write(audio_data)
        return (None, pyaudio.paContinue)

    def start_recording(self):
        logger.info("Recording started")
        self.microphone = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            input_device_index=0,
            frames_per_buffer=self.chunk,
            stream_callback=self._pyaudio_callback
        )


class ASRSystem():
    def __init__(self, rate=16000, chunk=16000):
        self.audio_buffer = AudioBuffer(rate=rate)
        self.mic_listener = Microphone(
            self.audio_buffer, rate=rate, chunk=chunk)
        self.asr_inference = FasterWhisperASR(
            self.audio_buffer, rate=rate, chunk=chunk)

    def start(self):
        mic_thread = threading.Thread(
            target=self.mic_listener.start_recording)
        transcribe_thread = threading.Thread(
            target=self.asr_inference.transcribe)

        mic_thread.start()
        transcribe_thread.start()

    def get_transcriptions(self):
        return self.asr_inference.get_transcription()


if __name__ == "__main__":
    asr_system = ASRSystem()
    asr_system.start()

    while True:
        time.sleep(1)
        print(asr_system.get_transcriptions())
