import streamlit as st
from langgraph_backend import Chatbot
from langchain_core.messages import HumanMessage,AIMessage
import uuid


st.sidebar.title('graphtalk')
if st.sidebar.button('new chat'):
    #logic to implement new chat where new thread id will generate and the window will restore that will be done using utility functions
    pass

st.sidebar.text('thread-1')
