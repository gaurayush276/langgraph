from langgraph.graph import StateGraph  ,START , END 
from typing import TypedDict, Literal

class QuadEq(TypedDict):
    a : int 
    b : int
    c : int 
    D : int 
    roots : list[int] | str 
    equation : str

def find_descriminant (state :QuadEq) :
    a = state["a"]
    b = state["b"]
    c = state["c"]
    D = (b**2) - (4 * a * c )
    
    return { "D" : D }

def check_discriminant ( state :QuadEq )  -> Literal[
    "real_roots",
    "same_roots",
    "imaginary_roots"
]: 
    if state["D"] == 0 :
        return  "same_roots"
    if state["D"] < 0 :
        return  "imaginary_roots"
    else :
        return  "real_roots"

def same_roots (state :QuadEq) :
    b = state['b']
    a = state['a']
    roots = -b / ( 2* a) 
    return { "roots" :  [roots  ,roots] }

def  real_roots ( state : QuadEq ) :
    b = state['b']
    a = state['a']
    c = state['c']
    D = state['D']
    first = (-b + D ** 0.5 ) / (2*a)
    second = (-b - D ** 0.5 ) / (2*a)

    return { "roots" :  [first  ,second] } 

def imaginary_roots (state : QuadEq) :
    return { "roots" : "not possible" } 

def show_equation(state: QuadEq):

    equation = f'{state["a"]}x2 {state["b"]}x {state["c"]}'

    return {'equation':equation}

graph = StateGraph(QuadEq)

graph.add_node("show_equation" , show_equation)
graph.add_node("find_descriminant" , find_descriminant)
graph.add_node("same_roots" , same_roots)
graph.add_node("real_roots" , real_roots)
graph.add_node("imaginary_roots" , imaginary_roots)


graph.add_edge(START , "show_equation")
graph.add_edge("show_equation" , "find_descriminant")
graph.add_conditional_edges("find_descriminant" , check_discriminant)
graph.add_edge("same_roots" , END)
graph.add_edge("real_roots" , END)
graph.add_edge("imaginary_roots" , END)

workflow = graph.compile() 

initial_State = { "a" :1 , "b" : 8 , "c" : 15} 
final_state  = workflow.invoke(initial_State)
print(final_state)





