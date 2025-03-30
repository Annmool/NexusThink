# NexusThink AI Assistant 🧠

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **Ultra-fast AI assistant powered by Groq's LPUs**  
> Chat with Llama 3, Mixtral, or Gemma models in real-time with customizable parameters

## 🌟 Features
- **Multiple LLMs**: llama3-8b/70b, mixtral-8x7b, gemma-7b
- **Customizable**: Adjust temperature (0-1) and max tokens (50-4000)
- **Persistent Chat**: Maintains conversation history during session
- **Secure**: API keys encrypted in session state
- **Responsive**: Works on desktop and mobile

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/yourusername/nexusthink-ai.git
cd nexusthink-ai
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Required
GROQ_API_KEY=your_key_here_from_groq.com

# Optional (for LangSmith)
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true

#Launch
streamlit run app.py
