import streamlit as st
import requests
import random
import time

# ገጹን በሙሉ ስክሪን እና በታዋቂው EthioAi ስም መክፈቻ
st.set_page_config(page_title="EthioAi", page_icon="🤖", layout="centered")

# ⚠️ አቤል ወንድሜ፣ የ gsk_ ቁልፎችህን እዚህ ዝርዝር ውስጥ በጥንቃቄ አስገባቸው
KEYS_LIST = [
    "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",
    "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",
    "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"
]

GROQ_KEYS = [k.replace('"', '').replace("'", "").strip() for k in KEYS_LIST if k]

# --- የኢትዮጵያ ሰንደቅ ዓላማ Background እና የዲዛይን ስታይል (CSS) ---
st.markdown("""
<style>
    /* አፑ መጀመሪያ ሲከፈትና በጀርባው ላይ የኢትዮጵያ ባንዲራ ቀለማት በፈዘዘ (Soft Linear Gradient) ዲዛይን */
    .stApp {
        background: linear-gradient(180deg, rgba(0,154,68,0.15) 0%, rgba(254,203,0,0.15) 50%, rgba(239,43,45,0.15) 100%);
        background-attachment: fixed;
    }
    
    /* የቻት መልእክቶች አኒሜሽን (Fade-in effect) */
    .stChatMessage {
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* የኢትዮጵያ ባንዲራ አርማ ከላይ ለማሳየት */
    .flag-bar {
        height: 6px;
        width: 100%;
        display: flex;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .green { background-color: #009A44; flex: 1; }
    .yellow { background-color: #FECB00; flex: 1; }
    .red { background-color: #EF2B2D; flex: 1; }
</style>
""", unsafe_allow_html=True)

# --- 1. STARTUP BANNER ---
# የኢትዮጵያ ባንዲራ መስመር ከላይ ያሳያል
st.markdown('<div class="flag-bar"><div class="green"></div><div class="yellow"></div><div class="red"></div></div>', unsafe_allow_html=True)
st.title("🤖 EthioAi")

# --- 2. CHAT HISTORY (የቆየ ወሬ ማስታወሻ) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# የቆዩትን መልእክቶች በሙሉ ከነ አኒሜሽናቸው በስክሪኑ ላይ ያሳያል
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CHAT INPUT & ANIMATION ---
if prompt := st.chat_input("EthioAi ን አነጋግረው..."):
    # የተጠቃሚውን መልእክት በታሪክ ውስጥ ማስቀመጥ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # የ AI አስተዋጽኦ በሚጽፍበት ጊዜ የሚታይ ውብ የጽሕፈት አኒሜሽን (Typing Thinking Animation)
        with st.spinner("EthioAi እያሰበ ነው..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            # ለ AIው የቆየውን ታሪክ (History) አብሮ በመላክ እንዲያስታውስ ማድረግ
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
                    elif response.status_code == 429:
                        continue
                except:
                    continue
                    
            if not ai_reply:
                ai_reply = "ይቅርታ፣ አሁን ሁሉም አገልጋዮች ስራ በዝቶባቸዋል። እባክህ ጥቂት ደቂቃዎች ቆይተህ ድጋሚ ሞክር።"
        
        # እውነተኛ የጽሕፈት አኒሜሽን (Word-by-word typing effect)
        full_response = ""
        for word in ai_reply.split(" "):
            full_response += word + " "
            time.sleep(0.04)  # የጽሕፈት ፍጥነት ማስተካከያ
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    # የ AIውን መልስ በታሪክ (History) ውስጥ ማስቀመጥ
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
