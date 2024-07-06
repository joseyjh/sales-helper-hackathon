from collections import deque
from .pre_rag_prompt import is_relevant
import socketio
from .rag import RAG

# Store user and response


class TranscriptProcessor():
    def __init__(self):
        self.working_memory = deque()
        self.query_snippet = ''
        self.memory = []
        self.previous_transcript = None
        self.repeat_count = 0
        self.sio = socketio.SimpleClient()
        self.sio.connect('http://localhost:8765')
        self.rag = RAG()
        self.silence_processed = False

    def process_query(self):
        rag_output = self.rag.process_query(
            self.query_snippet, self.working_memory)

        # Append RAG output to working memory
        self.working_memory.append(
            f"User: {self.query_snippet}\n"
            f"Our response: {rag_output}"
        )

        # If working memory exceeds 3 entries, clear oldest entry
        if len(self.working_memory) > 3:
            self.working_memory.pop()

        # Emit RAG output to client
        self.sio.emit("message event", {"message": rag_output})
        self.query_snippet = ''

    def process_transcripts(self, transcript):
        max_char = 120

        # If transcript is repeated more than 5 times, process query (silence from user)
        # Else do nothing
        if self.previous_transcript and transcript[-1]['text'] == self.previous_transcript:
            self.repeat_count += 1

            if self.repeat_count > 5 and is_relevant(self.previous_transcript) and not self.silence_processed:
                print("PROCESSING QUERY")
                self.process_query()
                self.repeat_count = 0
                self.silence_processed = True
            return
        self.previous_transcript = transcript[-1]['text']
        self.repeat_count = 0
        self.silence_processed = False

        texts = [entry['text'] for entry in transcript]

        # Extract new text from the transcript
        for text in texts:
            if text in self.memory:
                continue
            self.memory.append(text)
            self.query_snippet += text

        # If not relevant, discard working memory
        if not is_relevant(self.query_snippet):
            print(f'{self.query_snippet} (N)')
            self.query_snippet = ''
            return

        # If working memory exceeds max_char, perform action
        # Otherwise new text will be appended to working memory
        print(f'{self.query_snippet} (Y)')
        if len(self.query_snippet) > max_char:
            print("PROCESSING QUERY")
            self.process_query()
