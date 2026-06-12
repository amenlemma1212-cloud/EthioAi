import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="EthioAi", page_icon="🤖")

# ⚠️ አቤል ወንድሜ፣ የ gsk_ ቁልፎችህን እዚህ ጥቅስ ውስጥ ማስገባትህን እንዳትረሳ!
KEYS_LIST = [
    "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",
    "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",
    "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"
]

GROQ_KEYS = [k.replace('"', '').replace("'", "").strip() for k in KEYS_LIST if k]

# --- ለአፕሊኬሽን የሚሆን አዲስና ቀላል የባንዲራ ፍሬም ዲዛይን (CSS) ---
st.markdown("""
<style>
    /* አፑን ውብ የሚያደርግ የጀርባ ቀለም */
    .stApp {
        background-color: #f4f6f7;
    }
    
    /* በግራ እና በቀኝ በኩል የኢትዮጵያን ባንዲራ የሚያሳዩ ቀጫጭን መስመሮች */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(to bottom, #009A44 0%, #FECB00 50%, #EF2B2D 100%);
        z-index: 9999;
    }
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        right: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(to bottom, #009A44 0%, #FECB00 50%, #EF2B2D 100%);
        z-index: 9999;
    }
    
    /* ከላይ ያለችው ዋና የባንዲራ መስመር */
    .flag-top {
        height: 5px;
        width: 100%;
        display: flex;
        margin-bottom: 20px;
    }
    .green { background-color: #009A44; flex: 1; }
    .yellow { background-color: #FECB00; flex: 1; }
    .red { background-color: #EF2B2D; flex: 1; }
</style>
""", unsafe_allow_html=True)

# ከላይ የባንዲራ መስመር ያሳያል
st.markdown('<div class="flag-top"><div class="green"></div><div class="yellow"></div><div class="red"></div></div>', unsafe_allow_html=True)
st.title("🤖 EthioAi")

# የቆየ ወሬ ማስታወሻ (Chat History)
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
        
        with st.spinner("EthioAi..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            api_messages = [{"role": "system", "content": "You are EthioAi, a smart and professional AI assistant created by Abel."}]
            for msg in st.session_state.messages:
                api_messages.append({"role": msg["role"], "content": msg["content"]})
                
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": api_messages
            }
            
            ai_reply = ""
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
                        break
                except:
                    continue
                    
            if not ai_reply:
                ai_reply = "ይቅርታ፣ አሁን ሰርቨር ስራ በዝቶበታል። እባክህ ድጋሚ ሞክር።"
        
        # ለአሮጌ ስልኮች የሚሆን ፈጣን አኒሜሽን
        full_response = ""
        for word in ai_reply.split(" "):
            full_response += word + " "
            time.sleep(0.01)
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
