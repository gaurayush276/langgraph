import streamlit  as st 
import uuid
from be import chatbot , retrieve_all_threads
from langchain_core.messages import HumanMessage

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def generate_thread():
    thread = uuid.uuid4()
    return thread

def reset_chat() :
    thread = generate_thread()
    st.session_state["curr_thread"] = thread 
    add_thread(thread)
    st.session_state["chat_history"] = []

def load_conversation(thread) :
    state = chatbot.get_state(config = {"configurable" : { "thread_id" : thread}})
    return state.values.get("messages" , [])

if "chat_history" not in st.session_state :
    st.session_state["chat_history"] = []

if "curr_thread" not in st.session_state :
    st.session_state["curr_thread"] = generate_thread()

if "chat_threads" not in st.session_state :
    st.session_state["chat_threads"] = retrieve_all_threads()


add_thread(st.session_state["curr_thread"])

st.sidebar.title("ChatBot Test")
if st.sidebar.button("New chat") :
    reset_chat()
st.sidebar.header("Conversation")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['curr_thread'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['chat_history'] = temp_messages




for messages in st.session_state["chat_history"]:
    with st.chat_message(messages["role"]) :
        st.text(messages["content"])


query = st.chat_input("type here")
CONFIG = {"configurable" : { "thread_id" : st.session_state["curr_thread"]}}

if query : 
    if st.chat_message("user"):
        st.text(query) 
    st.session_state["chat_history"].append({"role" : "user" , "content" :query})

    response = chatbot.invoke({"messages":HumanMessage(content=query)}, config = CONFIG )
    final_res = response["messages"][-1].content

    if st.chat_message("ai"):
        st.text(final_res)

    st.session_state["chat_history"].append({"role" : "ai" , "content" :final_res})
    
    






