import streamlit as st
import requests
import json

# 🎨 CSS ማስተካከያ - የኢትዮጵያ ሰንደቅ ዓላማ ጀርባ እና የብርጭቆ ውበት
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #009c3a 0%, #fed100 50%, #ef1c24 100%) !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    div[data-testid="stChatMessageAssistant"] {
        border-right: 5px solid #fed100 !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 25px 25px 0px 25px !important;
    }
    div[data-testid="stChatMessageUser"] {
        border-left: 5px solid #009c3a !important;
        background-color: rgba(240, 248, 255, 0.95) !important;
        border-radius: 25px 25px 25px 0px !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%) !important;
        color: white !important;
        border-radius: 25px !important;
    }
    div[data-testid="stChatInput"] {
        border: 3px solid #009c3a !important;
        border-radius: 35px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🇪🇹 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱን የ OpenRouter (sk-or-...) ኮዶችህን እዚህ ጥቅስ ውስጥ በቅደም ተከተል አስገባቸው!
OPENROUTER_API_KEYS = [
    "የመጀመሪያው_sk-or-_ኮድ_እዚህ_ይግባ",
    "ሁለተኛው_sk-or-_ኮድ_እዚህ_ይግባ",
    "ሦስተኛው_sk-or-_ኮድ_እዚህ_ይግባ"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = {}

if "pinned_sessions" not in st.session_state:
    st.session_state.pinned_sessions = []

if "favorite_sessions" not in st.session_state:
    st.session_state.favorite_sessions = []

# 👈 የቻት ታሪክ ማውጫ (Sidebar)
with st.sidebar:
    st.header("📋 EthioAi Menu")
    language = st.radio("🌐 Choose Language / ቋንቋ ይምረጡ፦", ["English", "አማርኛ"])
    st.write("---")
    
    st.subheader("Chat Sessions")
    if st.button("➕ New Chat"):
        if st.session_state.messages:
            first_question = st.session_state.messages[0]["content"]
            session_title = first_question[:20] + "..." if len(first_question) > 20 else first_question
            session_id = f"{session_title} ({len(st.session_state.all_sessions) + 1})"
            st.session_state.all_sessions[session_id] = st.
