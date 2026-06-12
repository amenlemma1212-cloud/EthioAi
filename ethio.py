import streamlit as st
import google.generativeai as genai

# የ EthioAi ገጽ ማስተካከያ
st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# የ Google Gemini AI ነፃ ቁልፍ (API Key) ማገናኛ
# አቤል ወንድሜ፣ እዚህ ሳጥን ውስጥ ያንተን የ Gemini API Key ታስገባለህ
API_KEY = "AQ.Ab8RN6Ixqrlk4d7e3MgdPXJE9yWZhSbLHPXXsBgCyO8xwprg7w"

if API_KEY != "AQ.Ab8RN6Ixqrlk4d7e3MgdPXJE9yWZhSbLHPXXsBgCyO8xwprg7w":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.warning("እባክህ መጀመሪያ የ Gemini API Key አስገባ!")

# የቻት ታሪክ (Chat History) ማስቀመጫ
if "messages" not in st.session_state:
    st.session_state.messages = []

# የድሮ መልእክቶችን በስክሪኑ ላይ ማሳያ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ተጠቃሚው ጥያቄ ሲጠይቅ
if prompt := st.chat_input("EthioAi ን አነጋግረው..."):
    # ያንተን ጥያቄ ማሳያ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # ከእውነተኛው AI መልስ መቀበያ
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            try:
                response = model.generate_content(prompt)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"ይቅርታ ስህተት ተፈጥሯል፦ {e}"
        else:
            ai_reply = "እባክህ የ API Key ኮድህን አስገባ።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
