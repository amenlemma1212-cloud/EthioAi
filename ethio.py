import streamlit as st
import requests
from gtts import gTTS
import os

# 🎨 የገጹን ውበት፣ ዘመናዊ የቻት ባር እና የጽሑፍ አኒሜሽን ማስተካከል
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e293b 100%);
    }
    
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animated-box {
        animation: fadeInUp 0.4s ease-out forwards;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    
    .user-box { 
        background-color: #0ea5e9; 
        color: white;
    }
    
    .ai-box { 
        background-color: #1e293b; 
        color: #f8fafc;
        border: 1px solid #334155;
    }
    
    /* 🎨 ያንተን ፎቶ የመሰለ ዘመናዊ የቻት ባር ዲዛይን */
    div[data-testid="stChatInput"] {
        border: 3px solid #38bdf8 !important;
        border-radius: 35px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 25px rgba(56, 189, 248, 0.3) !important;
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

st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ እዚህ ጥቅስ ውስጥ ያንተን እውነተኛ የ gsk ኮድ ብቻ አስገባ!
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
    box_class = "user-box" if message["role"] == "user" else "ai-box"
    st.markdown(f'<div class="animated-box {box_class}">{message["content"]}</div>', unsafe_allow_html=True)

# 🎙️ የማይክሮፎን ሲስተም
audio_value = st.audio_input("🎙️ በድምፅ ለመጠየቅ ማይኩን ይጫኑ")

# 💬 የጽሕፈት ቻት ባር
chat_input = st.chat_input("እዚህ ጋር ይጻፉ...")

user_input = ""
if audio_value:
    user_input = "በድምፅ የተላከ መልእክት አለ (እባክህ እጅግ በጣም ጥራት ባለው በአማርኛ ቋንቋ ምላሽ ስጥ)"
elif chat_input:
    user_input = chat_input

if user_input:
    st.markdown(f'<div class="animated-box user-box">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if "YOUR_REAL_KEY" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
        st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮድህን በኮዱ ውስጥ በትክክል አስገባው!")
        st.stop()

    current_key = GROQ_API_KEYS[st.session_state.key_index]

    with st.spinner("EthioAi እያሰበ ነው..."):
        # 🚀 ይፋዊውን የ Groq HTTP API አጠቃቀም በጣም ቀላል በሆነ መንገድ አስተካክለነዋል
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {current_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are EthioAi, a smart assistant created by Abel. You must respond in beautiful, natural, and fluent Amharic language."},
                {"role": "user", "content": user_input}
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"]
            
            st.markdown(f'<div class="animated-box ai-box">{ai_response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # 🔊 የ AIው ድምፅ መልስ
            tts = gTTS(text=ai_response, lang='am', slow=False)
            audio_file = "response.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")
        else:
            # ኮዱ ካልሰራ ወዲያውኑ ወደ ቀጣዩ ኮድ ያዞረዋል
            st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
            st.error("እባክህ የ gsk API ኮድህ ትክክል መሆኑን አረጋግጥና ድጋሚ ጥያቄህን ላከው ወንድሜ።")
