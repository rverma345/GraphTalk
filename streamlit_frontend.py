import streamlit as st
message_history=[]

user_input=st.chat_input('Type here:')

if user_input:
    message_history.append({'role':'human','content':user_input})
    with st.chat_message('human'):
        st.text(user_input)
    message_history.append({'role':'assistant','content':user_input})
    with st.chat_message('ai'):
        st.text(user_input)


