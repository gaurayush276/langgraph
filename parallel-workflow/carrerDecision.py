from langgraph.graph import StateGraph , START ,END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 
from typing import TypedDict

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)


class Decision (TypedDict):
    topic : str
    technical_aspect : str 
    industry_trend : str 
    advantage: str
    limitation : str 
    real_world_expamles : list[str]
    notes : list[str]

def find_technical_aspect (state :Decision) :
    # technical_aspect = state["technical_aspect"]
    topic = state["topic"]

    query = f"find the technical_aspect of {topic} "
    result = model.invoke(query)
    return {

    "technical_aspect" : result.content 
    }

def find_industry_trend (state :Decision) :
    # industry_trend = state["industry_trend"]
    topic = state["topic"]

    query = f"find the industry_trend of {topic} "
    result = model.invoke(query)
    return {

    "industry_trend" : result.content 
    }

def find_advantages (state :Decision) :
    # advantage = state["advantage"]
    topic = state["topic"]

    query = f"find the advantage of {topic} "
    result = model.invoke(query)
    return {

    "advantage" : result.content 
    }

def find_limitations (state :Decision) :
    # limitations = state["limitation"]
    topic = state["topic"]

    query = f"find the limitations of {topic} "
    result = model.invoke(query)
    return {

    "limitation" : result.content 
    }

def find_examples (state :Decision) :
    # ex = state["real_world_expamles"]
    topic = state["topic"]

    query = f"find the ex of {topic} "
    result = model.invoke(query)
    return {

    "real_world_expamles" : result.content 
    }

def find_notes(state: Decision):

    topic = state["topic"]
    limitation = state["limitation"]
    advantages = state["advantage"]
    trend = state["industry_trend"]
    aspects = state["technical_aspect"]
    examples = state["real_world_expamles"]

    query = f"""
    On the basis of:

    Topic: {topic}
    Technical aspects: {aspects}
    Industry trends: {trend}
    Advantages: {advantages}
    Limitations: {limitation}
    Real-world examples: {examples}

    Prepare short notes on the topic {topic}.
    """

    result = model.invoke(query)

    return {
        "notes": result.content
    }


graph  = StateGraph(Decision)

graph.add_node("find_technical_aspect" ,find_technical_aspect )
graph.add_node("find_industry_trend" ,find_industry_trend )
graph.add_node("find_advantages" ,find_advantages )
graph.add_node("find_limitations" ,find_limitations )
graph.add_node("find_examples" ,find_examples )
graph.add_node("find_notes" ,find_notes )


graph.add_edge(START ,"find_technical_aspect" )
graph.add_edge(START ,"find_industry_trend" )
graph.add_edge(START ,"find_advantages" )
graph.add_edge(START ,"find_limitations" )
graph.add_edge(START ,"find_examples" )

 
graph.add_edge("find_technical_aspect" , "find_notes" )
graph.add_edge("find_industry_trend" , "find_notes" )
graph.add_edge("find_advantages" , "find_notes" )
graph.add_edge("find_limitations" , "find_notes" )
graph.add_edge("find_examples" , "find_notes" )

graph.add_edge("find_notes" , END) 

workflow = graph.compile() 

initial_State = {"topic" : "AI"}
final_state = workflow.invoke(initial_State)
result = final_state  

print(result)

 