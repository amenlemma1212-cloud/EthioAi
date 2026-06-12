import streamlit as st
import requests
import random

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# ⚠️ አቤል ወንድሜ፣ ያወጣሃቸውን 3 የተለያዩ የ gsk_ ቁልፎች እዚህ ጥቅስ ውስጥ በኮማ ለይተህ አስገባቸው
KEYS_LIST = [
    "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",
    "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",
    "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"
]

# ከዝርዝሩ ውስጥ ንጹሕ የሆኑትን ቁልፎች ብቻ አጽድቶ የሚይዝ
GROQ_KEYS = [k.replace('"', '').replace("'", "").strip() for k in KEYS_LIST if k]

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
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are EthioAi, a smart and professional AI assistant created by Abel."},
                {"role": "user", "content": prompt}
            ]
        }
        
        ai_reply = ""
        
        # 🚀 ቁልፎቹን አንድ በአንድ እየቀያየረ ይሞክራል (አንዱ ሊሚት ቢሞላ ሌላው ይተካል)
        # በየቀኑ በዘፈቀደ ቅደም ተከተል እንዲሞክራቸው ያደርጋል
        shuffled_keys = GROQ_KEYS.copy()
        random.shuffle(shuffled_keys)
        
        for key in shuffled_keys:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=20)
                if response.status_code == 200:
                    result = response.json()
                    ai_reply = result["choices"][0]["message"]["content"]
                    break  # በትክክል ከተረጋገጠ ከሉፑ ይወጣል
                elif response.status_code == 429:
                    continue  # ይህ ቁልፍ ሊሚት ከሞላበት ወደ ቀጣዩ ቁልፍ ይሸጋገራል
            except:
                continue
                
        if not ai_reply:
            ai_reply = "ይቅርታ፣ አሁን ሁሉም አገልጋዮች ስራ በዝቶባቸዋል። እባክህ ጥቂት ደቂቃዎች ቆይተህ ድጋሚ ሞክር።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
