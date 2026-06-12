import streamlit as st
import requests

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# አቤል ወንድሜ፣ ያንተን የ Gemini API Key እዚህ ውስጥ ብቻ በጥንቃቄ ለጥፈው
MY_KEY = "እዚህ ጋር ያንተን ረጅሙን የAPI_KEY ኮድ አስገባ"

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
        
        # ቁልፉን በቀጥታ ወደ ሊንኩ አስገብተነዋል
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MY_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            else:
                ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {response.status_code} - {response.text}"
        except Exception as e:
            ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {e}"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
