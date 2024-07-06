from .pre_rag_prompt import is_relevant
import socketio
from .rag import RAG


class TranscriptProcessor():
    def __init__(self):
        self.working_memory = ''
        self.memory = []
        self.previous_transcript = None
        # self.sio = socketio.SimpleClient()
        # self.sio.connect('http://localhost:8765')
        self.rag = RAG()

    def process_transcripts(self, transcript):
        max_char = 120

        # print(transcript)

        # If transcript has not been updated since last time, do nothing
        if self.previous_transcript and transcript[-1]['text'] == self.previous_transcript:
            return
        self.previous_transcript = transcript[-1]['text']

        texts = [entry['text'] for entry in transcript]

        # Extract new text from the transcript
        for text in texts:
            if text in self.memory:
                continue
            self.memory.append(text)
            self.working_memory += text

        # if self.working_memory == '':
        #     return

        # If not relevant, discard working memory
        if not is_relevant(self.working_memory):
            print(f'{self.working_memory} (N)')
            self.working_memory = ''
            return

        # If working memory exceeds max_char, perform action
        # Otherwise new text will be appended to working memory
        print(f'{self.working_memory} (Y)')
        if len(self.working_memory) > max_char:
            print("PROCESSING QUERY")
            print(self.rag.process_query(self.working_memory))
            # self.sio.emit("message event", {"message": "this is a message"})
            self.working_memory = ''
