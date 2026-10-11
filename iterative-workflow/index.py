from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import operator
import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

evaluator_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)
generateor_llm =  ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(..., description="Final evaluation result.")
    feedback: str = Field(..., description="feedback for the tweet.")


structured_output = evaluator_llm.with_structured_output(TweetEvaluation)

class TweetState(BaseModel) : 
    topic : str 
    tweet : str 
    evaluation : Literal["approved" , "need_imporovement"]
    feedback : str 
    iteration : int 
    max_iteration : int 

    tweet_history : Annotated[list[str], operator.add]
    feedback_history : Annotated[list[str], operator.add]

def generate_tweet (state:TweetState)  :
