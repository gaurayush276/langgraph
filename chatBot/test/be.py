from langgraph.graph import StateGraph , START , END
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 
from typing import TypedDict , Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()

# GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     api_key=GEMINI_KEY,
#     temperature=0.7
# )

from langchain_groq import ChatGroq
 
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
)

class ChatState (TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

def chat_node(state :ChatState):
    messages = state["messages"]
    res = llm.invoke(messages)
    return {"messages" : [res]}

conn = sqlite3.connect(database="chatbot.db" , check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)    

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_thread = set()
    for threads in checkpointer.list(None):
        all_thread.add(threads.config["configurable"]["thread_id"])

    return list(all_thread)    
 