import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# Load environment variables
load_dotenv()


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e1b4b 50%,
        #312e81 100%
    );
    color: white;
}

.main {
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 17px;
    margin-bottom: 30px;
}

.chat-box {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

.user-message {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 10px 0;
    margin-left: 20%;
}

.bot-message {
    background: rgba(255,255,255,0.12);
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 10px 20% 10px 0;
}

[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
}

.stButton > button {
    border-radius: 12px;
    border: none;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="title">🤖 AI Mood Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with AI in your favourite mood</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("🎭 AI Mode")

    mode_choice = st.selectbox(
        "Choose your AI personality",
        [
            "😂 Funny Mode",
            "😢 Sad Mode",
            "😡 Angry Mode",
            "🧠 Intelligent Mode"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# AI Modes
# -----------------------------

modes = {

    "😂 Funny Mode":
        "You are a funny AI agent. Respond in a humorous and entertaining way.",

    "😢 Sad Mode":
        "You are a sad AI agent. Respond in a calm, emotional and slightly sad way.",

    "😡 Angry Mode":
        "You are an angry AI agent. Respond in an angry and frustrated style, but remain respectful.",

    "🧠 Intelligent Mode":
        "You are an intelligent AI agent. Give logical, accurate and well-explained answers."
}


mode = modes[mode_choice]


# -----------------------------
# Initialize Model
# -----------------------------

@st.cache_resource
def load_model():

    return init_chat_model(
        "llama-3.3-70b-versatile",
        model_provider="groq"
    )


model = load_model()


# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# -----------------------------
# Display Chat History
# -----------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        st.markdown(
            f"""
            <div class="user-message">
                <b>YOU</b><br>
                {message.content}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif isinstance(message, AIMessage):

        st.markdown(
            f"""
            <div class="bot-message">
                <b>🤖 BOT</b><br>
                {message.content}
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# User Input
# -----------------------------

prompt = st.chat_input("Type your message...")


if prompt:

    # Add user message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # Create conversation
    messages = [
        SystemMessage(content=mode)
    ]

    messages.extend(st.session_state.messages)

    # Generate response
    with st.spinner("🤖 Thinking..."):

        response = model.invoke(messages)

    # Add AI response
    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    # Refresh UI
    st.rerun()