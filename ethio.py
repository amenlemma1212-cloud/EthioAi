import streamlit as st
import requests
import json

# 🎨 CSS ማስተካከያ - የብርጭቆ ማውጫ፣ የኩርባ ቅርጾች እና የጽሑፍ አቅጣጫ
st.markdown(
    """
    <style>
    /* 🇪🇹 የኢትዮጵያ ሰንደቅ ዓላማ Gradient ጀርባ */
    .stApp {
        background: linear-gradient(135deg, #009c3a 0%, #fed100 50%, #ef1c24 100%) !important;
    }
    
    /* 🔮 የቻት ታሪክ ማውጫውን (Sidebar) የብርጭቆ/የመስታወት (Glass) ማድረጊያ */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
