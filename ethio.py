import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 🎨 የገጹን ውበት፣ ዘመናዊ ቻት ባር እና የጽሑፍ አኒሜሽን በ CSS ማስተካከል
st.markdown(
    """
    <style>
    /* ሙሉ ገጹ በጥቁር እና ሰማያዊ እንዲያምር */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e293b 100%);
    }
    
    /* 🎬 ጽሑፎች በቀስታ ከታች ወደ ላይ ብቅ እንዲሉ ማድረጊያ አኒሜሽን */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animated-box {
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 12px;
        font-size: 16px;
        line-height: 1.5;
    }
    
    .user-box { 
        background-color: #0ea5e9; 
        color: white;
        margin-left: 20%;
        border-radius: 15px 15px 0px 15px;
    }
    
    .ai-box { 
        background-color: #1e293b; 
        color: #f8fafc;
        border: 1px solid #334155;
        margin-right: 20%;
        border-radius: 15px 15px 15px 0px;
    }
    
    /* 🎨 ያንተን ፎቶ የመሰለ ዘመናዊ ክብ የቻት ባር ዲዛይን */
    div[data-testid="stChatInput"] {
        border: 3px solid #38bdf8 !important;
        border-radius: 35px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 25px rgba(56, 189, 248, 0.3) !important;
        padding: 6px !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        background-color: #ffffff !important;
    }
    
    /* የማይክሮፎን ሪከርደር ዲዛይን */
    .mic-container {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #38bdf8;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ እዚህ ጥቅስ ውስጥ ያንተን 3 የ gsk ኮዶች ማስገባትህን ፍጹም እንዳትረሳ!
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

# 🎙️ የማይክሮፎን ሲስተም (ከላይ በኩል በጣም ተስማሚ በሆነ ቦታ)
with st.container():
    st.markdown('<div class="mic-container">', unsafe_allow_html=True)
    audio_value = st.audio_input("🎙️ በድምፅ ለመጠየቅ ማይኩን ይጫኑ")
    st.markdown('</div>', unsafe_allow_html=True)

# 💬 ያንተን ፎቶ የመሰለ ዘመናዊ ክብ የጽሕፈት ቻት ባር
chat_input = st.chat_input("እዚህ ጋር ልክ እንደ ፎቶው ይጻፉ...")

# የትኛው መረጃ እንደመጣ ማረጋገጫ
if audio_value:
    user_input = "በድምፅ የተላከ መልእክት አለ (እባክህ እጅግ በጣም ጥራት ባለው አማርኛ ምላሽ ስጥ)"
elif chat_input:
    user_input = chat_input

if user_input:
    # ጥያቄን በአኒሜሽን ማሳየት
    st.markdown(f'<div class="animated-box user-box">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # የ gsk ኮድ መኖሩን ማረጋገጫ
    if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
        st.markdown('<div class="animated-box ai-box" style="color:red;">⚠️ አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮድህን በኮዱ ውስጥ አስገባው!</div>', unsafe_allow_html=True)
        st.stop()

    with st.spinner("EthioAi እያሰበ ነው..."):
        try:
            client = Groq(api_key=GROQ_API_KEYS[st.session_state.key_index])
            
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are EthioAi, a smart assistant created by Abel. You must respond in fluent, beautiful, and natural Amharic language. Speak like a real Ethiopian human."},
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
            st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
            st.markdown('<div class="animated-box ai-box" style="color:orange;">መስመር ላይ ትንሽ መጨናነቅ አለ፣ እባክህ ድጋሚ ጥያቄህን ላከው ወንድሜ።</div>', unsafe_allow_html=True)
