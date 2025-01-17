import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import os

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! Looking for something to watch? You can ask about genres like thriller, action, or comedy, and I'll recommend three movies with details like actors, language, director, and IMDb rating. Try it out!"}
    ]

# Initialize ChatOpenAI and ConversationChain
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    openai_api_key=st.secrets["TOGETHER_API_KEY"],
    openai_api_base="https://api.together.xyz/v1"
)

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🗣️ IMDb Chatbot")
st.subheader("🎥 Entertainment with AI")

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if "regenerate" in prompt.lower():
                # Logic to ensure new recommendations
                st.session_state.buffer_memory.clear()
                response = conversation.predict(input="Recommend another set of movies")
            else:
                response = conversation.predict(input=prompt)

            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
