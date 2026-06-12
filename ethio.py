import streamlit as st
import requests

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# ⚠️ አቤል ወንድሜ፣ እዚህ ጥቅስ ምልክቱ ውስጥ ያንተን የ gsk_ ኮድ ብቻ በጥንቃቄ አስገባ
RAW_KEY = "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"

# ማንኛውንም ክፍት ቦታ ወይም ስህተት የሚያጸዳ
GROQ_API_KEY = RAW_KEY.replace('"', '').replace("'", "").strip()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("EthioAi ን አነጋግረው..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are EthioAi, a smart and professional AI assistant created by Abel."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=25)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
            else:
                # ሰርቨሩ በትክክል ያልሠራበትን እውነተኛ ምክንያት ለማወቅ (ለማስተካከል ይጠቅማል)
                ai_reply = f"የሰርቨር ስህተት ቁጥር፦ {response.status_code}"
        except Exception as e:
            ai_reply = "ከኢንተርኔት ጋር መገናኘት አልተቻለም። እባክህ ገጹን Refresh አድርገው።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
