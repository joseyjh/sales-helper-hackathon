from openai import OpenAI
import os
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, Distance, VectorParams
from dotenv import load_dotenv

load_dotenv(override=True)


class RAG:
    def __init__(self):
        self.qc = QdrantClient(
            url="https://dafd8b74-38ea-418d-88ca-adf6dcfd77a0.us-east4-0.gcp.cloud.qdrant.io",
            port=6333,
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = ""
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization="org-5wZe424Sz9nIIZ1Nxgf7n2cv"
        )

    def get_top_k(self, text, k=3):
        query_vector = np.array(self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small",
            encoding_format="float"
        ).data[0].embedding)

        hits = self.qc.search(
            collection_name="testtest2",
            query_vector=query_vector,
            limit=1
        )

        return hits[:k]
