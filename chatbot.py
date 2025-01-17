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
        {"role": "assistant", "content": "Hey! Looking for something to watch? Click on a genre below and I'll recommend three movies with details like actors, language, director, and IMDb rating."}
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

st.write("### Select a Genre:")

# Define genres
genres = ["Thriller", "Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Adventure"]

# Create even-sized blocks
rows = len(genres) // 4 + (1 if len(genres) % 4 != 0 else 0)  # Calculate the number of rows needed
selected_genre = None

for row in range(rows):
    cols = st.columns(4)  # Create 4 columns in each row
    for col, genre in zip(cols, genres[row * 4:(row + 1) * 4]):  # Distribute genres evenly across columns
        if col.button(genre):
            selected_genre = genre

# Process the selected genre
if selected_genre:
    prompt = f"Recommend three {selected_genre} movies with details like actors, language, director, and IMDb rating."
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input=prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
