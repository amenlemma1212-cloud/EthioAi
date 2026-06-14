import streamlit as st
import requests
from gtts import gTTS
import os

# የ CSS ዲዛይኑ በሙሉ ጠፍቷል - አፑ አሁን ቀላል ነው!
st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ እዚህ ጥቅስ ውስጥ ያንተን እውነተኛ የ gsk ኮድ ብቻ በጥንቃቄ አስገባ!
GROQ_API_KEY = "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"

# 🎙️ የድምፅ መቀበያ
audio_value = st.audio_input("🎙️ በድምፅ ለመጠየቅ ይጫኑ")

# 💬 የጽሕፈት ሳጥን
chat_input = st.chat_input("እዚህ ጋር ይጻፉ...")

user_input = ""
if audio_value:
    user_input = "በድምፅ የተላከ መልእክት አለ"
elif chat_input:
    user_input = chat_input

if user_input:
    # ጥያቄውን ማሳየት
    st.write(f"✍️ **እርስዎ፦** {user_input}")

    if "YOUR_REAL_KEY" in GROQ_API_KEY or GROQ_API_KEY == "":
        st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮድህን አስገባ!")
    else:
        with st.spinner("EthioAi እያሰበ ነው..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": "You are EthioAi. Respond in short, clear, and fluent Amharic language."},
                        {"role": "user", "content": user_input}
                    ]
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    
                    # መልሱን ማሳየት
                    st.write(f"🤖 **EthioAi፦** {ai_response}")
                    
                    # ድምፅ ማጫወት
                    tts = gTTS(text=ai_response, lang='am', slow=False)
                    audio_file = "response_voice.mp3"
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                    tts.save(audio_file)
                    st.audio(audio_file, format="audio/mp3")
                else:
                    st.error(f"የ Groq ኤረር ኮድ፦ {response.status_code}። ኮድህን አረጋግጥ።")
            except Exception as e:
                st.error("ከGroq ሰርቨር ጋር መገናኘት አልተቻለም።")
