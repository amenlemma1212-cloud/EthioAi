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

# 🚨 አቤል ወንድሜ፣ 3ቱን የ OpenRouter (sk-or-...) ኮዶችህን እዚህ ጥቅስ ውስጥ በቅደም ተከተል አስገባቸው!
OPENROUTER_API_KEYS = [
    "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",
    "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",
    "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"
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
            
            col_btn, col_pop = st.columns([4, 1])
            
            with col_btn:
                if st.button(f"💬 {display_title}", key=f"open_{title}", use_container_width=True):
                    st.session_state.messages = st.session_state.all_sessions[title]
                    st.rerun()
            
            with col_pop:
                with st.popover("⋮", help="Options"):
                    pin_label = "📍 Unpin Chat" if title in st.session_state.pinned_sessions else "📌 Pin Chat"
                    if st.button(pin_label, key=f"pin_{title}", use_container_width=True):
                        if title in st.session_state.pinned_sessions:
                            st.session_state.pinned_sessions.remove(title)
                        else:
                            st.session_state.pinned_sessions.append(title)
                        st.rerun()
                        
                    fav_label = "💛 Unfavorite" if title in st.session_state.favorite_sessions else "⭐ Favorite"
                    if st.button(fav_label, key=f"fav_{title}", use_container_width=True):
                        if title in st.session_state.favorite_sessions:
                            st.session_state.favorite_sessions.remove(title)
                        else:
                            st.session_state.favorite_sessions.append(title)
                        st.rerun()
                        
                    if st.button("🗑️ Delete Chat", key=f"del_{title}", use_container_width=True):
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
        elif message["content"].startswith("[Image Uploaded]"):
            st.info("🖼️ Image received by EthioAi!")
        elif message["content"].startswith("[Audio Uploaded]"):
            st.success("🎤 Audio file is in memory.")
        else:
            st.markdown(message["content"])

# 📱 👈 ባለ 3 ነጥብ (⋮) ፖፖቨር - Video, Image, Audio
with st.popover("⋮ More Options (Video, Image, Audio)", use_container_width=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎬 Video Option", use_container_width=True):
            st.toast("Video making assistant initialized! 🎬")
    with col2:
        uploaded_img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="img_up")
        if uploaded_img is not None:
            st.image(uploaded_img, caption="Selected Image", use_container_width=True)
            if st.button("Send Image", use_container_width=True, key="send_img"):
                st.session_state.messages.append({"role": "user", "content": "[Image Uploaded]"})
                st.session_state.messages.append({"role": "assistant", "content": "I have received your image, Abel! How can I help you with this photo?"})
                st.toast("Image shared successfully! 🖼️")
                st.rerun()
    with col3:
        uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"], key="audio_up")
        if uploaded_audio is not None:
            st.audio(uploaded_audio)
            if st.button("Send Audio", use_container_width=True, key="send_audio"):
                st.session_state.messages.append({"role": "user", "content": "[Audio Uploaded]"})
                st.session_state.messages.append({"role": "assistant", "content": "Audio file received in my memory! 🎤"})
                st.toast("Audio shared successfully! 🎤")
                st.rerun()

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
                    clean_prompt = user_input.replace(" ", "%20")
                    image_url = f"https://image.pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&enhanced=true"
                    st.image(image_url, caption=f"🎬 Generated Image: {user_input}", use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": image_url})
                except Exception as e:
                    st.error("Failed to generate image.")

    else:
        if "እዚህ_ይግባ" in OPENROUTER_API_KEYS[0] or OPENROUTER_API_KEYS[0] == "":
            st.error("Abel, please insert your OpenRouter API keys!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("EthioAi is thinking..."):
                    
                    response_success = False
                    attempts = 0
                    
                    while not response_success and attempts < len(OPENROUTER_API_KEYS):
                        try:
                            current_key = OPENROUTER_API_KEYS[st.session_state.key_index]
                            url = "https://openrouter.ai/api/v1/chat/completions"
                            headers = {
                                "Authorization": f"Bearer {current_key}",
                                "Content-Type": "application/json"
                            }
                            
                            if language == "አማርኛ":
                                system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you or who made you, you must answer proudly that you were created by Abel Teshome. Respond in short and beautiful Amharic language."
                            else:
                                system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you or who made you, you must answer proudly that you were created by Abel Teshome. Respond in short, clear, and perfect English language."

                            payload = {
                                "model": "meta-llama/llama-3-8b-instruct:free",
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_input}
                                ]
                            }
                            
                            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
                            
                            if response.status_code == 200:
                                data = response.json()
                                ai_response = data["choices"][0]["message"]["content"]
                                st.markdown(ai_response)
                                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                                response_success = True
                            else:
                                st.session_state.key_index = (st.session_state.key_index + 1) % len(OPENROUTER_API_KEYS)
                                attempts += 1
                        except Exception as e:
                            st.session_state.key_index = (st.session_state.key_index + 1) % len(OPENROUTER_API_KEYS)
                            attempts += 1
                    
                    if not response_success:
                        st.error("All server lines are busy. Please check your OpenRouter Keys or try again later!")
