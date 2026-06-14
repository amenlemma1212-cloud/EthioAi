import streamlit as st
import requests
from gtts import gTTS
import os

# 🎨 የገጹን ውበት፣ የማይክሮፎን አቀማመጥ እና የጽሑፍ አኒሜሽን በ CSS ማስተካከል
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e293b 100%);
    }
    
    /* ✨ 🎬 ጽሑፎች በቀስታ ከታች ወደ ላይ ብቅ እንዲሉ ማድረጊያ (Fade In and Up Animation) */
    @keyframes fade-in-up {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* አኒሜሽኑን በቻት መልእክቶች ላይ መጫን */
    .stChatMessage {
        animation: fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
    
    /* 🎨 የቻት ባር እና የማይክሮፎን ውህደት ዲዛይን */
    div[data-testid="stChatInput"] {
        border: 3px solid #38bdf8 !important;
        border-radius: 25px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4) !important;
        padding: 5px !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        background-color: #ffffff !important;
    }
    
    /* 🎙️ የማይክሮፎን ሳጥኑ ከቻት ባሩ ጋር በጣም ተቀራራቢ ሆኖ እንዲያምር */
    .audio-container {
        margin-bottom: -15px;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱንም የ gsk ኮዶችህን እዚህ ጥቅስ ውስጥ በትክክል ማስገባትህን እንዳትረሳ!
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

user_input = ""

# 🎙️ የድምፅ ሲስተም (አቀማመጡን ልክ ከቻት ባሩ ጎን/በላይ እንዲሆን አድርገነዋል)
st.markdown('<div class="audio-container">', unsafe_allow_html=True)
audio_value = st.audio_input("🎙️ በድምፅ ለመጠየቅ ማይኩን ይጫኑ")
st.markdown('</div>', unsafe_allow_html=True)

if audio_value:
    user_input = "በድምፅ የተላከ መልእክት አለ (እባክህ እጅግ በጣም ጥራት ባለው አማርኛ ምላሽ ስጥ)"

# 💬 የጽሕፈት ቻት ባር
chat_input = st.chat_input("እዚህ ጋር በግልጽ ይጻፉ...")
if chat_input:
    user_input = chat_input

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
        with st.chat_message("assistant"):
            st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮድህን በGitHub ላይ ባለው ኮድ ውስጥ አስገባው!")
            st.stop()

    current_key = GROQ_API_KEYS[st.session_state.key_index]

    headers = {
        "Authorization": f"Bearer {current_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "You are EthioAi, a smart assistant created by Abel. You must respond in fluent, beautiful, and natural Amharic language. Speak clearly and like a real Ethiopian."
            },
            {"role": "user", "content": user_input}
        ]
    }

    with st.chat_message("assistant"):
        with st.spinner("EthioAi እያሰበ ነው..."):
            try:
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=15)
                
                if response.status_code == 429 or response.status_code == 401:
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                    st.warning("EthioAi መስመሩን እየቀየረ ነው፣ እባክህ ድጋሚ ጥያቄህን ላከው...")
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
                st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                st.error("ከGroq ሰርቨር ጋር መገናኘት አልተቻለም። እባክህ የ gsk ኮድህን በትክክል መጻፍህን አረጋግጥና ድጋሚ ሞክር።")
