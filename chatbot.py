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
        {"role": "assistant", "content": "Hey! Looking for something to watch? I can help you discover movies in these genres:\n\n"
         "🎭 Drama\n"
         "🔫 Action\n"
         "💕 Romance\n"
         "🔍 Thriller\n"
         "👻 Horror\n"
         "🤣 Comedy\n"
         "🚀 Sci-Fi\n\n"
         "Which genre interests you today?"}
    ]

if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None

# Initialize ChatOpenAI and ConversationChain
llm = ChatOpenAI(
    model="llama-2-70b-chat",
    openai_api_key=st.secrets["TOGETHER_API_KEY"],
    openai_api_base="https://api.together.xyz/v1"
)

conversation = ConversationChain(
    memory=st.session_state.buffer_memory, 
    llm=llm
)

# Create user interface
st.title("🎬 IMDb Chatbot")
st.subheader("🍿 Your Personal Movie Advisor")

# Add genre selection sidebar
with st.sidebar:
    st.header("Quick Genre Selection")
    if st.button("🎭 Drama"):
        st.session_state.selected_genre = "Drama"
    if st.button("🔫 Action"):
        st.session_state.selected_genre = "Action"
    if st.button("💕 Romance"):
        st.session_state.selected_genre = "Romance"
    if st.button("🔍 Thriller"):
        st.session_state.selected_genre = "Thriller"
    if st.button("👻 Horror"):
        st.session_state.selected_genre = "Horror"
    if st.button("🤣 Comedy"):
        st.session_state.selected_genre = "Comedy"
    if st.button("🚀 Sci-Fi"):
        st.session_state.selected_genre = "Science Fiction"  # Fixed syntax error here

# Handle genre selection
if st.session_state.selected_genre and st.session_state.messages[-1]["role"] == "assistant":
    prompt = f"I'm interested in {st.session_state.selected_genre} movies"
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.selected_genre = None

# Handle chat input
if prompt := st.chat_input("Ask me about movies or select a genre!"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Finding the perfect movies for you..."):
            # Enhanced prompt to guide the conversation
            enhanced_prompt = f"""
            As a movie expert, help with this request: {prompt}
            If the user hasn't specified a genre, suggest some genres.
            If they have, recommend 2-3 highly-rated movies in that genre, including:
            - Movie title and year
            - Brief plot summary
            - Star rating (out of 5)
            - Key actors
            - Why they might enjoy it
            
            End with a question about their preferences to help refine recommendations.
            """
            response = conversation.predict(input=enhanced_prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)

# Add helpful footer
st.markdown("---")
st.markdown("💡 **Tip**: Try asking about specific genres, actors, or decades!")
