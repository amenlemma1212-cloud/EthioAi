import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# አቤል ወንድሜ፣ ያንተን የ Gemini API Key እዚህ ውስጥ ብቻ አስገባው
API_KEY = "AQ.Ab8RN6Ixqrlk4d7e3MgdPXJE9yWZhSbLHPXXsBgCyO8xwprg7w"

# AIውን በቀጥታ ማገናኛ
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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
        try:
            response = model.generate_content(prompt)
            ai_reply = response.text
        except Exception as e:
            ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {e}"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
