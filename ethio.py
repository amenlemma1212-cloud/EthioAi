import streamlit as st
import requests

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# አቤል ወንድሜ፣ እዚህ ጋር የጥቅስ ምልክቶቹን እንዳታጠፋቸው!
# ያንተን AIzaSy ብሎ የሚጀምረውን ኮድ ብቻ እዚህ መሃል በጥንቃቄ ለጥፈው።
RAW_KEY = "AQ.Ab8RN6JgfoKtegCAj3EEpXYbtr-BvqhFIrIzvzK5qisDY9O3Kg"

# ክፍት ቦታ ወይም ሌላ አላስፈላጊ ነገር ካለ የሚያጸዳ
API_KEY = RAW_KEY.strip()

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
        
        # ሊንኩን እጅግ በጣም ንጹሕ አድርገን ለይተን እንጽፈዋለን
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        params = {"key": API_KEY}
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            # params=params በመጠቀም ቁልፉን በንጽሕና ይልከዋል
            response = requests.post(url, headers=headers, json=payload, params=params)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            else:
                ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {response.status_code} - {response.text}"
        except Exception as e:
            ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {e}"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
