import streamlit as st
import requests

# 🎨 የገጹን ውበት፣ ያንተን ፎቶ ዲዛይን እና ሁሉንም አዲሱን አኒሜሽኖች በ CSS ማስተካከል
st.markdown(
    """
    <style>
    /* 🇪🇹 የኢትዮጵያ ሰንደቅ ዓላማ Gradient ጀርባ */
    .stApp {
        background: linear-gradient(135deg, #009c3a 0%, #fed100 50%, #ef1c24 100%) !important;
    }
    
    /* 🎬 ጽሑፎች እና መልእክቶች በቀስታ ከታች ወደ ላይ ብቅ እንዲሉ (Fade In & Up) */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .stChatMessage {
        animation: fadeInUp 0.4s ease-out forwards;
        border-radius: 15px !important;
    }
    
    /* 📋 በግራ በኩል ያለው ማውጫ (Sidebar) በቀስታ ብቅ እንዲል ማድረጊያ አኒሜሽን */
    @keyframes sidebarFade {
        0% { opacity: 0; transform: translateX(-20px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    section[data-testid="stSidebar"] {
        animation: sidebarFade 0.5s ease-out forwards;
    }
    
    /* 🎨 ነጭ የቻት ባር ማስተካከያ */
    div[data-testid="stChatInput"] {
        border: 2px solid #009c3a !important;
        border-radius: 35px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* ⌨️ ቻት ባሩ ላይ ክሊክ ሲደረግ ደምቆ እንዲያበራ ማድረጊያ አኒሜሽን (Focus Glow Animation) */
    div[data-testid="stChatInput"]:focus-within {
        border: 3px solid #ef1c24 !important;
        box-shadow: 0 0 25px rgba(254, 209, 0, 0.8) !important;
        transform: scale(1.01);
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
    "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",
    "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",
    "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"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# 👈 በግራ በኩል የቻት ታሪክ እና የቋንቋ መምረጫ (Sidebar) በአኒሜሽን
with st.sidebar:
    st.header("📋 EthioAi Menu")
    
    language = st.radio("🌐 Choose Language / ቋንቋ ይምረጡ፦", ["English", "አማርኛ"])
    
    st.write("---")
    st.subheader("💬 Chat History")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# የቀድሞ የቻት ታሪኮችን በገጹ ላይ ማሳያ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):
            st.image(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

# 💬 የታችኛው ዘመናዊ የጽሕፈት ቻት ባር (በአኒሜሽን የተገነባ)
user_input = st.chat_input("Type your message here / እዚህ ጋር ይጻፉ...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # የምስል ጥያቄ መሆኑን ማረጋገጫ
    is_image_request = any(word in user_input.lower() for word in ["image", "picture", "photo", "generate", "ምስል", "ስዕል", "ፎቶ"])

    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("EthioAi is painting... / EthioAi ምስል እየሳለ ነው..."):
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
                    trans_res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=translate_payload, headers=headers)
                    
                    image_prompt = trans_res.json()["choices"][0]["message"]["content"] if trans_res.status_code == 200 else user_input
                    clean_prompt = image_prompt.replace(" ", "%20")
                    
                    image_url = f"https://image.pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&enhanced=true"
                    
                    st.image(image_url, caption=f"🎬 Generated Image: {user_input}", use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": image_url})
                except Exception as e:
                    st.error("Failed to generate image. / ምስሉን መፍጠር አልተቻለም።")

    # 💬 የጽሑፍ ጨዋታ (ስምህን Abel Teshome ብሎ እንዲጠራ የተደረገበት ክፍል)
    else:
        if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
            st.error("Abel, please insert your Groq gsk API keys!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("EthioAi is thinking... / እያሰበ ነው..."):
                    try:
                        current_key = GROQ_API_KEYS[st.session_state.key_index]
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {current_key}",
                            "Content-Type": "application/json"
                        }
                        
                        # 🚨 እዚህ ጋር ለ AIው ፈጣሪው አንተ (Abel Teshome) መሆንህን በግልጽ አስተምረነዋል!
                        if language == "አማርኛ":
                            system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you or who made you, you must answer proudly that you were created by Abel Teshome. Respond in short and beautiful Amharic language."
                        else:
                            system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you or who made you, you must answer proudly that you were created by Abel Teshome. Do not say Meta AI. Respond in short, clear, and perfect English language."

                        payload = {
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_input}
                            ]
                        }
                        
                        response = requests.post(url, json=payload, headers=headers, timeout=15)
                        
                        if response.status_code == 200:
                            data = response.json()
                            ai_response = data["choices"][0]["message"]["content"]
                            
                            st.markdown(ai_response)
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                            
                        elif response.status_code in [429, 401, 400]:
                            st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                            st.warning("Server line switching, please try again...")
                        else:
                            st.error(f"Error Code: {response.status_code}")
                            
                    except Exception as e:
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                        st.error("Connection error, please resend.")
