
from langgraph.graph import StateGraph , START ,END
from typing import TypedDict

class BMIState (TypedDict):
    weight : float 
    height:  float 
    bmi  : float

def calculate (state : BMIState) -> BMIState :
     
    weight = state["weight"]
    height = state["height"]
    answer = weight / ( height ** 2)
    state["bmi"] = round(answer , 2 )
    return state

graph = StateGraph(BMIState)

graph.add_node("calculate" , calculate )
graph.add_edge(START , "calculate" )
graph.add_edge( "calculate" , END  ) 

workflow = graph.compile()

initia_state =  { "weight" : 62 , "height" : 1.776}

final_state = workflow.invoke(initia_state) 
print(final_state)

# works only in notebook  not  in py 
from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())
 