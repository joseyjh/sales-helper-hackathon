import time
from transcribe_interval import ASRSystem
from pre_rag_prompt import is_relevant

if __name__ == "__main__":
    rate = 16000
    chunk = 32000
    max_non_relevance = 3
    max_repeated = 1
    interval = chunk / rate

    asr_system = ASRSystem(rate=rate, chunk=chunk)
    asr_system.start()

    previous = ''
    non_relevance_count = 0
    repeated_count = 0
    while True:
        transcription = asr_system.get_transcriptions()

        if is_relevant(transcription):
            non_relevance_count = 0

            # TODO: do something with transcription
            print(f'{transcription} (Y)')

            # If nothing was said in the last interval
            if transcription == previous:
                repeated_count += 1

                # Discard transcriptions after `max_repeated` number of repeated transcriptions
                if repeated_count >= max_repeated:
                    repeated_count = 0
                    asr_system.trim_transcriptions(len(transcription))
            else:
                repeated_count = 0
        else:
            print(f'{transcription} (N)')
            non_relevance_count += 1

            # Discard transcriptions after `max_non_relevance` number of non-relevant transcriptions
            if non_relevance_count >= max_non_relevance:
                asr_system.trim_transcriptions(len(transcription))
                non_relevance_count = 0
        previous = transcription
        time.sleep(interval)
