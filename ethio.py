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
        border
