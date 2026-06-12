import streamlit as st
import requests

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

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
        
        # ያለምንም የሀገር ገደብ ለሁሉም ሰው የሚሠራ እውነተኛ AI
        url = "https://open-api.koyeb.app/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are EthioAi, a smart and helpful AI assistant created by Abel."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
            else:
                ai_reply = "ይቅርታ፣ የአገልጋይ ስራ መብዛት አጋጥሟል። እባክህ ጥቂት ቆይተህ ድጋሚ ሞክር።"
        except Exception as e:
            ai_reply = "ይቅርታ፣ ከኔትወርክ ጋር መገናኘት አልተቻለም። እባክህ ገጹን Refresh አድርገው።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
