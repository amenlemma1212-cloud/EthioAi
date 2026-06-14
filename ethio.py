import streamlit as st
import requests
from gtts import gTTS
import os

# 🎨 የገጹን ውበት እና አኒሜሽን በ CSS ማስተካከል
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e293b 100%);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage {
        animation: fadeIn 0.5s ease-out forwards;
        border-radius: 15px !important;
        margin-bottom: 10px;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #0ea5e9 !important;
        color: white !important;
    }
    [data-testid="stChatMessageAssistant"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    div[data-testid="stChatInput"] {
        border: 2px solid #38bdf8 !important;
        border-radius: 30px !important;
        background-color: #111827 !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2) !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 EthioAi")

# ⚠️ አቤል ወንድሜ፣ 3ቱንም የgsk ኮዶችህን እዚህ ጥቅስ ውስጥ አስገባቸው!
GROQ_API_KEYS = [
    "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",
    "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",
    "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"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# የቀድሞ የቻት ታሪኮችን ማሳያ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🎙️ የሰው ድምፅ መቀበያ ሲስተም (Safe Human Audio Input)
st.write("🎙️ በድምፅ ለመጠየቅ ከታች ያለውን ማይክሮፎን ይጫኑ፦")
audio_value = st.audio_input("ድምፅዎን ይቅረጹ")

user_input = ""

# ሰውየው ድምፅ ቀርጾ ካስገባ
if audio_value:
    st.audio(audio_value, format="audio/wav")
    user_input = "በድምፅ የተላከ ጥያቄ አለ (እባክህ በቆንጆ አማርኛ መልስ ስጥ)"

# በጽሑፍም መቀበያ
chat_input = st.chat_input("ወይም እዚህ ጋር በጽሑፍ ይጻፉ...")
if chat_input:
    user_input = chat_input

# ጥያቄው ሲመጣ የሚሠራው ዋናው የ AI ሲስተም
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    current_key = GROQ_API_KEYS[st.session_state.key_index]

    headers = {
        "Authorization": f"Bearer {current_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "You are EthioAi, a smart assistant created by Abel. You must respond in perfect, beautiful, and fluent Amharic language. Speak like a native Ethiopian."
            },
            {"role": "user", "content": user_input}
        ]
    }

    with st.chat_message("assistant"):
        with st.spinner("EthioAi እያሰበ ነው..."):
            try:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                
                if response.status_code == 429:
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                    st.warning("EthioAi መስመሩን እየቀየረ ነው፣ እባክህ ድጋሚ ላከው...")
                    st.stop()

                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                # 🔊 የ AIው ድምፅ መልስ
                tts = gTTS(text=ai_response, lang='am', slow=False)
                audio_file = "response.mp3"
                tts.save(audio_file)
                st.audio(audio_file, format="audio/mp3")
                
            except Exception as e:
                st.error("ይቅርታ፣ ስህተት ተከስቷል።")
