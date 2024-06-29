"""
Transcribes according to a fixed length interval
"""

from collections import deque
import pyaudio
import numpy as np
from faster_whisper import WhisperModel
from loguru import logger
from scipy.io.wavfile import write
import threading
import time


class AudioQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def enqueue(self, data: np.ndarray):
        with self.lock:
            self.queue.appendleft(data)

    def pop(self) -> np.ndarray:
        with self.lock:
            return self.queue.pop()

    def __len__(self):
        return len(self.queue)


class FasterWhisperASR:
    def __init__(self, audio_queue: AudioQueue, rate: int, chunk: int):
        self.model = WhisperModel("small")
        self.queue = audio_queue
        self.rate = rate
        self.text = ''
        self.chunk = chunk

    def transcribe(self):
        # Transcribes audio from the task queue
        while True:
            if len(self.queue) == 0:
                time.sleep(0.5)
                continue

            audio_data = self.queue.pop()

            segments, info = self.model.transcribe(
                audio=audio_data,
                initial_prompt=self.text,
                language="en",
                vad_filter=True,
            )

            text = ''
            for segment in segments:
                text += segment.text

            print(text)
            self.text = text

            write(f'{time.time()}.wav', self.rate,
                  (audio_data * 32768).astype(np.int16))


class Microphone:
    def __init__(self, audio_queue: AudioQueue, rate: int, chunk: int):
        self.audio = pyaudio.PyAudio()
        self.queue = audio_queue
        self.rate = rate
        self.chunk = chunk

        logger.info("Microphone initialized")

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        audio_data = (np.frombuffer(
            in_data, dtype=np.int16) / 32768).astype(np.float32)
        self.queue.enqueue(audio_data)
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
    def __init__(self, rate=16000, chunk=32000):
        self.audio_buffer = AudioQueue()
        self.mic_listener = Microphone(
            self.audio_buffer, rate=rate, chunk=chunk)
        self.asr_inference = FasterWhisperASR(
            self.audio_buffer, rate=rate, chunk=chunk)

    def start(self):
        mic_thread = threading.Thread(
            target=self.mic_listener.start_recording)
        infer_thread = threading.Thread(
            target=self.asr_inference.transcribe)

        mic_thread.start()
        infer_thread.start()

        mic_thread.join()
        infer_thread.join()


if __name__ == "__main__":
    asr_system = ASRSystem()
    asr_system.start()
