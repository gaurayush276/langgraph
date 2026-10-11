from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import operator
from typing import Annotated , List ,TypedDict
from pydantic import BaseModel , Field
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langsmith import traceable
from langgraph.graph import StateGraph, START, END
import os 

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)

search = DuckDuckGoSearchRun()

 