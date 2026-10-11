from langgraph.graph import StateGraph , START , END 
from typing import TypedDict , Annotated
from langchain_core.messages import HumanMessage , BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 
from langgraph.graph.message import add_messages
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GEMINI_KEY,
    temperature=0.7
)

checkpointer = MemorySaver()

class ChatState(TypedDict) :
    messages : Annotated[list[BaseMessage] , add_messages]


graph = StateGraph(ChatState)

def chat_node(state:ChatState) :
    message = state["messages"]
    response = llm.invoke(message)
    # we are returning [response] not response because both must be list to be added
    return { "messages" : [response ]}

graph.add_node("chat_node" , chat_node )

graph.add_edge(START , "chat_node")
graph.add_edge("chat_node" , END) 

workflow = graph.compile(checkpointer = checkpointer) 

# initial_State ={ "messages" : HumanMessage(content="hi")}
# final_State = workflow.invoke(initial_State) 

# for res in final_State["messages"] :
#     print(res.content)

thread = '1' 
while True :
    query = input("enter the input") 
    config = {'configurable' : { "thread_id" : thread}}
    initial_state = {
        "messages" : HumanMessage(content = query )
    }
    if query.strip().lower() in ["exit" , "quit" , 'bye'] :
        break
    final_state = workflow.invoke(initial_state, config = config)
    print(final_state["messages"][-1].content)

