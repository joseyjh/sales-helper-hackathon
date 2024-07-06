from openai import OpenAI
import os
import numpy as np
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from .pre_rag_prompt import template

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
        Here is the query that is provided by the customer "{text}"

        With the context provided by the RAG here: "{nearest_result.payload['doc']}",

        Come up with ONLY 1 question that follow this based on what feels the most suitable at the moment to address the customer query in alignment with the context provided.

        The question should use the framework ({template}) when deciding how to respond.
        
        Do not indicate which part of the framework you are using after selection, just the question itself.
        """

        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            top_p=0.5,
            frequency_penalty=0.4,
            messages=[
                {"role": "system", "content": "You are a sales person that is well-versed with handling customer queries with regards to tiktok ads and is currently assisting a newcomer with sales\n\n The information provided to you are a part of the conversation from you interacting with the customers, who are looking to potentially engage with your service or product.\n\n Your role is to provide the right questions to help this newcomer ask the right question to lead the customer to clarify their doubts or to a closing of a product"},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content
