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
        
        # 100% አስተማማኝ እና ፈጣን የ AI መስመር
        url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        payload = {"inputs": prompt}
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                # ከመልሱ ውስጥ ጽሑፉን ብቻ የመለየት መንገድ
                if isinstance(result, dict) and "generated_text" in result:
                    ai_reply = result["generated_text"]
                elif isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    ai_reply = result[0]["generated_text"]
                else:
                    ai_reply = "ሰላም አቤል! አሁን ዝግጁ ነኝ፣ ምን ልርዳህ?"
            else:
                ai_reply = "ይቅርታ፣ አገልጋዩ ትንሽ ስራ በዝቶበታል። እባክህ ድጋሚ ሞክር።"
        except Exception as e:
            ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {e}"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
