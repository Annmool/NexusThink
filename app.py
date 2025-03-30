import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from datetime import datetime

# Load environment variables
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "NexusThink"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "new_input" not in st.session_state:
    st.session_state.new_input = False

## Page styling and configuration
st.set_page_config(
    page_title="NexusThink AI Assistant",
    page_icon="🧠",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #e6f3ff;
        border-left: 5px solid #2b6cb0;
        color: #1a202c;
    }
    .chat-message.assistant {
        background-color: #f0f4f8;
        border-left: 5px solid #4c1d95;
        color: #1a202c;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
     /* Clear Chat button styling */
    .stButton>button {
        background-color: #4C1D95;  /* Purple background (matches your theme) */
        color: white !important;    /* White text */
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
    }

    /* Hover effect */
    .stButton>button:hover {
        background-color: #5F2DAB;  /* Slightly lighter purple on hover */
        color: white !important;    /* Keep text white on hover */
    }
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        padding: 0.75rem;
        border: 1px solid #e2e8f0;
    }
    .title-container {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    .title-text {
        font-weight: 800;
        color: #4c1d95;
        font-size: 2.5rem;
        margin-left: 1rem;
    }
    .sidebar-header {
        margin-top: 0;
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        text-align: center;
        background-color: #4c1d95;
        color: white;
        border-radius: 0 0 1rem 1rem;
    }
   .model-info {
        padding: 1rem;
        background-color: #f8fafc;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #e2e8f0;
        color: #1a202c !important;  /* Dark gray text for better contrast */
    }

    .model-info h4 {
        color: #4c1d95 !important;  /* Purple header to match your theme */
        margin-top: 0;
    }

    .model-info p {
        margin-bottom: 0.5rem;
    }
    .error-message {
        color: #e53e3e;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant called NexusThink. Please respond to user queries with well-structured, informative answers."),
    ("user", "Question:{question}")
])

# Function to generate responses
def generate_response(question, model, temperature, max_tokens):
    groq_api_key = os.getenv("GROQ_API_KEY") or st.session_state.get("groq_api_key", "")
    
    if not groq_api_key:
        return "❌ Please enter your Groq API key in the sidebar to continue."
    
    try:
        llm = ChatGroq(
            model=model,
            groq_api_key=groq_api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        return chain.invoke({'question': question})
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h2>⚙️ Configuration</h2></div>', unsafe_allow_html=True)
    
    groq_api_key = st.text_input(
        "Enter your Groq API key:",
        type="password",
        value=st.session_state.get("groq_api_key", ""),
        key="api_key_input"
    )
    
    if groq_api_key:
        st.session_state["groq_api_key"] = groq_api_key
        st.success("API key saved successfully!")
    else:
        st.warning("Please enter your Groq API key to use the assistant")

    st.markdown("### Model Settings")
    model = st.selectbox(
        "Select Groq model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
        key="model_select"
    )
    temperature = st.slider(
        "Temperature",
        0.0, 1.0, 0.7, 0.1,
        key="temp_slider"
    )
    max_tokens = st.slider(
        "Max Tokens",
        50, 4000, 1000, 50,
        key="tokens_slider"
    )

    st.markdown(f"""
    <div class="model-info">
        <h4>Currently using:</h4>
        <p><strong>Model:</strong> {model}</p>
        <p><strong>Temperature:</strong> {temperature}</p>
        <p><strong>Max tokens:</strong> {max_tokens}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.markdown('<div class="title-container"><div class="title-text">NexusThink</div></div>', unsafe_allow_html=True)
st.markdown("##### Your AI-powered assistant for instant knowledge and insights")

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    avatar = "👤" if role == "user" else "🧠"
    
    with st.container():
        st.markdown(f"""
        <div class="chat-message {role}">
            <div>{avatar}</div>
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# User input area - Only show if API key is set
if st.session_state.get("groq_api_key"):
    user_input = st.text_input(
        "Ask NexusThink a question:",
        value="",
        key="user_input",
        label_visibility="collapsed",
        on_change=lambda: st.session_state.update({"new_input": True})
    )
else:
    st.markdown('<div class="error-message">Please enter your Groq API key in the sidebar to enable chat</div>', unsafe_allow_html=True)
    user_input = ""

if st.session_state.get("new_input", False) and user_input:
    # Reset the flag immediately
    st.session_state.new_input = False
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        response = generate_response(
            user_input,
            st.session_state.model_select,
            st.session_state.temp_slider,
            st.session_state.tokens_slider
        )
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear the input by rerunning
    st.rerun()

# Footer
st.markdown(f"""
<div style="text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; color: #718096; font-size: 0.8rem;">
    NexusThink AI Assistant • {datetime.now().strftime("%B %d, %Y")}
</div>
""", unsafe_allow_html=True)
