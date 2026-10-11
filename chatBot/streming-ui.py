# import streamlit as st 
# from be import chatbot 
# from langchain_core.messages import HumanMessage

# CONFIG = {'configurable': {'thread_id': 'thread-2'}}

# if "history" not in st.session_state : 
#     st.session_state["history"] = []

# for messages in  st.session_state['history'] :
#     with st.chat_message(messages['role']):
#         st.text(messages["content"]) 

# user_input = st.chat_input("type here")

# if user_input :
   
#     st.session_state['history'].append({"role" : "user" , "content" : user_input })

#     with st.chat_message("user"):
#         st.text(user_input) 

#     # final_state = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

#     # ai_message = final_state['messages'][-1].content

#     # with st.chat_message("assistant"):
#     #     st.text(ai_message) 
 
#     # st.session_state['history'].append({'role': 'assistant', 'content': ai_message}) 

#     with st.chat_message('assistant'):

#         ai_message = st.write_stream(
#             message_chunk.content.text for message_chunk, metadata in chatbot.stream(
#                 {'messages': [HumanMessage(content=user_input)]},
#                 config=CONFIG,
#                 stream_mode= 'messages'
#             )
#         )

#     st.session_state['history'].append({'role': 'assistant', 'content': ai_message})


import streamlit as st
from be import chatbot
from langchain_core.messages import HumanMessage
import uuid
import os 
os.environ["LANGCHAIN_PROJECT"] = "streaming-ui-chatbot"
# st.session_state -> dict -> 
# CONFIG = {'configurable': {'thread_id': 'thread-1'}}



def generate_thread() :
    thread_id = uuid.uuid4()
    return str(thread_id) 

def load_converstaion(thread_id):
    return chatbot.get_state(config = {"configurable" : {"thread_id" : thread_id}}).values["messages"]

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state['chat_threads'].append(thread_id)


def reset_thread () :
    thread_id = generate_thread() 
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"]=[]


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state :
    st.session_state['thread_id'] = generate_thread()
if 'chat_threads'  not in st.session_state :
    st.session_state["chat_threads"] = []

add_thread(st.session_state['thread_id'])
# sidebar 
st.sidebar.title("Chat with BILLU")
if st.sidebar.button("New Chat"):
    reset_thread() ; 

st.sidebar.header("Purani batee")

for thread_id in st.session_state["chat_threads"]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"]=thread_id
        history = load_converstaion(thread_id)

        temp_messages = []
            # because from be we had format as role , content but here we have humanMessage.........
        for msg in history :
            if isinstance(msg , HumanMessage):
                role='user'
            else :
                role = 'assistant'    
            temp_messages.append({"role" : role , 'content' : msg.content})    
            st.session_state["message_history"] = temp_messages

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')
def get_text(chunk):

    if isinstance(chunk.content, str):
        return chunk.content

    if isinstance(chunk.content, list):
        return "".join(
            block.get("text", "")
            for block in chunk.content
            if block.get("type") == "text"
        )

    return ""


if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            
            get_text(message_chunk) for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': st.session_state['thread_id'] }},
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})