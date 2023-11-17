import streamlit as st
import random
import time

st.title("Simple Chat")

#Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#React to user input
if prompt := st.chat_input("What is up?"):
    #Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    #Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "What's up dude, how can I help?",
                "Hi, Human! Is there anything I can help you with?",
                "What's the haps?"
            ]
        )
        #Simulate stream of response with slight delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            #Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    #Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})