import time
from transcribe_interval import ASRSystem
from pre_rag_prompt import is_relevant

if __name__ == "__main__":
    rate = 16000
    chunk = 32000
    max_non_relevance = 3
    interval = chunk / rate

    asr_system = ASRSystem(rate=rate, chunk=chunk)
    asr_system.start()

    previous = ''
    non_relevance_count = 0
    while True:
        transcription = asr_system.get_transcriptions()

        if is_relevant(transcription):
            # TODO: something with transcription
            # If nothing was said in the last interval
            if transcription == previous:
                asr_system.clear_transcriptions()
        else:
            non_relevance_count += 1
            # Discard transcriptions after `max_non_relevance` number of non-relevant transcriptions
            if non_relevance_count >= max_non_relevance:
                asr_system.clear_transcriptions()
                non_relevance_count = 0
        previous = transcription
        time.sleep(interval)
