import streamlit as st
from langgraph_backend import Chatbot
from langchain_core.messages import HumanMessage
user_input=st.chat_input("Type here:")

# message_history=[] # this list will always get reset when we press enter so we need st.session_state (history that persists 
#st.session_state
config={'configurable':{'thread_id':'thread_1'}}
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

# loadint the covnersation history

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


if user_input:
    #adding the message to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
   
    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk for message_chunk,metadata in Chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config={'configurable':{'thread_id':'thread-1'}},
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})