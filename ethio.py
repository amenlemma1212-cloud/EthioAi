import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 🎨 የገጹን ውበት እና የጽሑፍ አኒሜሽን በ CSS ማስተካከል
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e293b 100%);
    }
    
    /* 🎬 ጽሑፎች በቀስታ ከታች ወደ ላይ ብቅ እንዲሉ ማድረጊያ አኒሜሽን */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animated-box {
        animation: fadeInUp 0.5s ease-out forwards;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        color: white;
    }
    
    .user-box { background-color: #0ea5e9; }
    .ai-box { background-color: #1e293b; border: 1px solid #334155; }
    
    /* 🎨 የጽሕፈት ሳጥኑ ደማቅ ጥቁር ጽሑፍ እንዲሆን */
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 EthioAi")

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

# የቀድሞ የቻት ታሪኮችን በአኒሜሽን ማሳያ
for message in st.session_state.messages:
    box_class = "user-box" if message["role"] == "user" else "ai-box"
    st.markdown(f'<div class="animated-box {box_class}">{message["content"]}</div>', unsafe_allow_html=True)

user_input = ""

# 🎙️ 💬 የማይክሮፎን እና የቻት ባር ውህደት (ጎን ለጎን ተደርገዋል)
col1, col2 = st.columns([1, 4])

with col1:
    audio_value = st.audio_input("🎙️") # ማይኩ አጠር ብሎ ከሳጥኑ ጎን ሆነ

with col2:
    chat_input = st.chat_input("እዚህ ጋር ይጻፉ...")

# ጥያቄን መቀበያ
if audio_value:
    user_input = "በድምፅ የተላከ መልእክት አለ (እባክህ እጅግ በጣም ጥራት ባለው አማርኛ ምላሽ ስጥ)"
elif chat_input:
    user_input = chat_input

if user_input:
    # የተጠቃሚውን ጥያቄ በአኒሜሽን ማሳየት
    st.markdown(f'<div class="animated-box user-box">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
        st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮድህን በኮዱ ውስጥ አስገባው!")
        st.stop()

    with st.spinner("EthioAi እያሰበ ነው..."):
        try:
            # 🚀 አዲሱ እና ፍጹሙ የ Groq አገናኝ ሲስተም
            client = Groq(api_key=GROQ_API_KEYS[st.session_state.key_index])
            
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are EthioAi, a smart assistant created by Abel. You must respond in fluent, beautiful, and natural Amharic language."},
                    {"role": "user", "content": user_input}
                ],
                timeout=15
            )
            
            ai_response = completion.choices[0].message.content
            
            # የ AIውን መልስ በአኒሜሽን ማሳየት
            st.markdown(f'<div class="animated-box ai-box">{ai_response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # 🔊 የ AIው ድምፅ መልስ
            tts = gTTS(text=ai_response, lang='am', slow=False)
            audio_file = "response.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")
            
        except Exception as e:
            # ሰርቨሩ እምቢ ካለ ወደ ቀጣዩ የ gsk ኮድ ያዞረዋል
            st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
            st.error("መስመር ላይ ትንሽ መጨናነቅ አለ፣ እባክህ ድጋሚ ጥያቄህን ላከው ወንድሜ።")
