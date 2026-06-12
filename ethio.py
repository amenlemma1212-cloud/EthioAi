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
        
        # ሰርቨር 1 (ዋናው ሰርቨር)
        url1 = "https://open-api.koyeb.app/v1/chat/completions"
        payload1 = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are EthioAi, a smart and helpful AI assistant created by Abel."},
                {"role": "user", "content": prompt}
            ]
        }
        
        # ሰርቨር 2 (የመጠባበቂያ ሰርቨር - ሰርቨር 1 ስራ ቢበዛበት ይህ ይሠራል)
        url2 = "https://chateverywhere.v7x.workers.dev/api/chat"
        payload2 = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        ai_reply = ""
        
        # መጀመሪያ ዋናውን ሰርቨር መሞከር
        try:
            response = requests.post(url1, json=payload1, timeout=20)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
        except:
            pass
            
        # ዋናው ሰርቨር ከሸሸገ መጠባበቂያውን ሰርቨር መሞከር
        if not ai_reply:
            try:
                response = requests.post(url2, json=payload2, timeout=20)
                if response.status_code == 200:
                    ai_reply = response.text
            except:
                pass
                
        # ሁለቱም እምቢ ካሉ የሚመጣ መልዕክት
        if not ai_reply:
            ai_reply = "ይቅርታ፣ የአገልጋይ ስራ መብዛት አጋጥሟል። እባክህ ጥቂት ቆይተህ ድጋሚ ሞክር።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
