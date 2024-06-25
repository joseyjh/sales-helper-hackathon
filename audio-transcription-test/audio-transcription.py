import time
import pyaudio
import librosa
import numpy as np
from faster_whisper import WhisperModel
from loguru import logger

class Microphone:

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.sampling_rate = 16000
        self.record_duration = 10
        self.model = WhisperModel("small")
        logger.info("Microphone initialized")

    def start_recording(self):

        logger.info("Recording started")

        def callback_function(in_data, frame_count, time_info, status):

            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_data = (audio_data / 32768).astype(np.float32) 
            print(f"{audio_data.shape} {audio_data.dtype}")
            segments, info = self.model.transcribe(audio_data,language="en")
            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

            return (None, pyaudio.paContinue)
        
        self.microphone = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sampling_rate,
            input=True,
            input_device_index=0,
            frames_per_buffer=int(self.record_duration * self.sampling_rate),
            stream_callback=callback_function

        )




if __name__ == "__main__":
    mic = Microphone()
    mic.start_recording()
    while True:
        time.sleep(1)