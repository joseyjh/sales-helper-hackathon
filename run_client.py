from whisper_live.client import TranscriptionClient

client = TranscriptionClient(
    'localhost',
    9090,
    model='base.en',
    save_output_recording=True
)
client()
