import streamlit as st
user_input=st.chat_input("Type here:")

messages=[]

if user_input:
    with st.chat_message("user"):
        st.text(user_input)
    with st.chat_message("ai"):
        st.text(user_input)