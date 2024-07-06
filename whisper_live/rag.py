from openai import OpenAI
import os
import numpy as np
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv(override=True)


class RAG:
    def __init__(self):
        self.qc = QdrantClient(
            url="https://dafd8b74-38ea-418d-88ca-adf6dcfd77a0.us-east4-0.gcp.cloud.qdrant.io",
            port=6333,
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "techjam"
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def process_query(self, query):
        question = self.query_to_question(query)
        most_relevant = self.get_most_relevant(question)
        return most_relevant

    def query_to_question(self, query):
        prompt = f"""
      This is a portion of an audio transcript query from a client asking about Tiktok Business, and how to use their ads effectively: {query}.

      Complete the query in a short sentence and keep the main key words in this question. Make the query SIMPLE.

      """

        query_completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        query_result = query_completion.choices[0].message.content
        return query_result

    def get_most_relevant(self, text):
        query_vector = np.array(self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small",
            encoding_format="float"
        ).data[0].embedding)

        nearest_result = self.qc.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=1
        )[0]

        prompt = f"""
      This is a portion of an audio transcript query from a client: {query_vector}.

      Summarize the information below to around 50-100 words that can help the client understand this better:

      {nearest_result.payload['doc']}

      """

        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content
