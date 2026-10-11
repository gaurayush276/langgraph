import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

load_dotenv()

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_TOKEN")
)

text = "What is artificial intelligence?"

vector = embeddings.embed_query(text)

print(vector)
print(len(vector))