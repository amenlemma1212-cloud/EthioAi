import streamlit as st
import requests

# 🎨 የገጹን ውበት፣ የብርጭቆ ማውጫ፣ የኩርባ ቅርጽ እና አቅጣጫን ያቀፈው የመጨረሻው CSS
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
        font-weight: bold !important;
    }
    
    /* 🤖 🔄 ሮቦት (AI) text -> ወደ ቀኝ (Right) እና በጣም ክብ የኩርባ ጠርዝ */
    div[data-testid="stChatMessageAssistant"] {
        border-right: 5px solid #fed100 !important;
        border-left: none !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        margin-left: 20% !important;
        margin-right: 0% !important;
        border-radius: 25px 25px 0px 25px !important;
    }
    
    /* 👤 🔄 ሰው (Human/User) text -> ወደ ግራ (Left) እና በጣም ክብ የኩርባ ጠርዝ */
    div[data-testid="stChatMessageUser"] {
        border-left: 5px solid #009c3a !important;
        border-right: none !important;
        background-color: rgba(240, 248, 255, 0.95) !important;
        margin-right: 20% !important;
        margin-left: 0% !important;
        text-align: left !important;
        border-radius: 25px 25px 25px 0px !important;
    }
    
    /* 🎬 አጠቃላይ የሳጥን ውበት */
    .stChatMessage {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        margin-bottom: 12px !important;
        padding: 15px !important;
    }
    
    /* ➕ "New Chat" ማራኪ ሰማያዊ ቁልፍ */
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
        width: 100% !important;
        transition: transform 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.05) !important;
    }
    
    /* 🎨 ነጭ የቻት ባር ማስተካከያ */
    div[data-testid="stChatInput"] {
        border: 3px solid #009c3a !important;
        border-radius: 35px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border: 3px solid #ef1c24 !important;
        box-shadow: 0 0 20px rgba(254, 209, 0, 0.8) !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        background-color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🇪🇹 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱንም የ gsk ኮዶችህን እዚህ ጥቅስ ውስጥ በትክክል አስገባቸው!
GROQ_API_KEYS = [
    "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",     "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",     "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"
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
            st.session_state.all_sessions[session_id] = st.session_state.messages
            
        st.session_state.messages = []
        st.rerun()

    if st.session_state.all_sessions:
        st.write("---")
        st.subheader("📜 Chat History")
        
        sorted_sessions = sorted(
            st.session_state.all_sessions.keys(),
            key=lambda k: k in st.session_state.pinned_sessions,
            reverse=True
        )
        
        for title in sorted_sessions:
            display_title = title
            if title in st.session_state.pinned_sessions:
                display_title = "📌 " + display_title
            if title in st.session_state.favorite_sessions:
                display_title = display_title + " ⭐"
                
            if st.button(f"💬 {display_title}", key=f"open_{title}"):
                st.session_state.messages = st.session_state.all_sessions[title]
                st.rerun()
                
            col_pin, col_fav, col_del = st.columns(3)
            
            with col_pin:
                pin_label = "📍 Unpin" if title in st.session_state.pinned_sessions else "📌 Pin"
                if st.button(pin_label, key=f"pin_{title}"):
                    if title in st.session_state.pinned_sessions:
                        st.session_state.pinned_sessions.remove(title)
                    else:
                        st.session_state.pinned_sessions.append(title)
                    st.rerun()
                    
            with col_fav:
                fav_label = "💛 Unfav" if title in st.session_state.favorite_sessions else "⭐ Fav"
                if st.button(fav_label, key=f"fav_{title}"):
                    if title in st.session_state.favorite_sessions:
                        st.session_state.favorite_sessions.remove(title)
                    else:
                        st.session_state.favorite_sessions.append(title)
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️ Delete", key=f"del_{title}"):
                    del st.session_state.all_sessions[title]
                    if title in st.session_state.pinned_sessions:
                        st.session_state.pinned_sessions.remove(title)
                    if title in st.session_state.favorite_sessions:
                        st.session_state.favorite_sessions.remove(title)
                    st.rerun()
            st.write("---")

# የቀድሞ መልእክቶች ማሳያ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):
            st.image(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

# 💬 የታችኛው ዘመናዊ የጽሕፈት ቻት ባር
user_input = st.chat_input("Type your message here / እዚህ ጋር ይጻፉ...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    is_image_request = any(word in user_input.lower() for word in ["image", "picture", "photo", "generate", "ምስል", "ስዕል", "ፎቶ"])

    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("EthioAi ምስል እየሳለ ነው..."):
                try:
                    current_key = GROQ_API_KEYS[st.session_state.key_index]
                    translate_payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "Translate the user prompt into a short English image generation prompt. Only return the English translation, nothing else."},
                            {"role": "user", "content": user_input}
                        ]
                    }
                    headers = {"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}
                    trans_res = requests.post("https://api.groq
