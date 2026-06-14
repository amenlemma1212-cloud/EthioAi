import streamlit as st
import requests
from gtts import gTTS
import os

st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱንም የ gsk ኮዶችህን እዚህ ጥቅስ ውስጥ በትክክል አስገባቸው!
GROQ_API_KEYS = [
    "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",
    "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",
    "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"
]

# የትኛው ኮድ ላይ እንዳለን ማስታወሻ
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

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
    st.write(f"✍️ **እርስዎ፦** {user_input}")

    if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
        st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮዶችህን አስገባ!")
    else:
        with st.spinner("EthioAi እያሰበ ነው..."):
            try:
                # በአሁኑ ሰዓት የሚሠራውን ኮድ መምረጥ
                current_key = GROQ_API_KEYS[st.session_state.key_index]
                
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {current_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are EthioAi. Respond in short, clear, and fluent Amharic language."},
                        {"role": "user", "content": user_input}
                    ]
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    
                    st.write(f"🤖 **EthioAi፦** {ai_response}")
                    
                    # ድምፅ ማጫወት
                    tts = gTTS(text=ai_response, lang='am', slow=False)
                    audio_file = "response_voice.mp3"
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                    tts.save(audio_file)
                    st.audio(audio_file, format="audio/mp3")
                    
                # ኮዱ ጥያቄ ካበዛ ወይም ኤረር ካለው ወደ ቀጣዩ ኮድ ይቀይራል
                elif response.status_code in [429, 401, 400]:
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                    st.warning("EthioAi መስመሩን እየቀየረ ነው፣ እባክህ ድጋሚ ላከው ወንድሜ...")
                else:
                    st.error(f"የ Groq ኤረር ኮድ፦ {response.status_code}")
                    
            except Exception as e:
                # በሰርቨር ችግር ጊዜም ቢሆን ኮዱን ይቀይራል
                st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                st.error("መስመር ላይ ትንሽ መጨናነቅ አለ፣ እባክህ ድጋሚ ጥያቄህን ላከው።")
