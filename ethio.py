import streamlit as st

st.set_page_config(page_title="EthioAi")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("EthioAi")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask EthioAi anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    ai_reply = f"Hello, you said: {prompt}"
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
