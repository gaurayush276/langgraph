from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Simple one-line prompt
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from langgraph.graph.message import add_messages

load_dotenv()
prompt = PromptTemplate.from_template("{question}")

GEMINI_KEY = os.getenv("GEMINI_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the capital of Peru?"})
print(result)