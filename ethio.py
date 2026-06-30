import streamlit as st
import requests
import json

st.title("🇪🇹 EthioAi")

# 🚨 አቤል ወንድሜ፣ ከGroq ያገኘኸውን የ gsk_... ኮድ እዚህ ጥቅስ ውስጥ አስገባው!
GROQ_API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = {}

# 👈 የቻት ታሪክ ማውጫ (Sidebar)
with st.sidebar:
    st.header("📋 EthioAi Menu")
    language = st.radio("🌐 Choose Language / ቋንቋ ይምረጡ፦", ["English", "አማርኛ"])
    st.write("---")
    
    st.subheader("Chat Sessions")
    if st.button("➕ New Chat"):
        if st.session_state.messages:
            first_question = st.session_state.messages[0]["content"]
            session_title = first_question[:20] + "..." if len(first_question) > 20 else first_question
            session_id = f"{session_title} ({len(st.session_state.all_sessions) + 1})"
            st.session_state.all_sessions[session_id] = st.session_state.messages
        st.session_state.messages = []
        st.rerun()

    if st.session_state.all_sessions:
        st.write("---")
        st.subheader("📜 Chat History")
        for title in list(st.session_state.all_sessions.keys()):
            col_btn, col_pop = st.columns([4, 1])
            with col_btn:
                if st.button(f"💬 {title}", key=f"open_{title}", use_container_width=True):
                    st.session_state.messages = st.session_state.all_sessions[title]
                    st.rerun()
            with col_pop:
                with st.popover("⋮"):
                    if st.button("🗑️ Delete Chat", key=f"del_{title}", use_container_width=True):
                        del st.session_state.all_sessions[title]
                        st.rerun()

# የቀድሞ መልእክቶች ማሳያ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):
            st.image(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

# 📱 ሚዲያ መጫኛ (Image)
with st.popover("⋮ More Options (Image)", use_container_width=True):
    uploaded_img = st.file_uploader("Upload Image", type=["jpg", "png"], key="img_up")
    if uploaded_img is not None:
        st.image(uploaded_img, use_container_width=True)

# 💬 የቻት መጻፊያ
user_input = st.chat_input("Type your message here / እዚህ ጋር ይጻፉ...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    is_image_request = any(word in user_input.lower() for word in ["image", "picture", "photo", "generate", "ምስል", "ስዕል"])

    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("EthioAi ምስል እየሳለ ነው..."):
                try:
                    clean_prompt = user_input.replace(" ", "%20")
                    image_url = f"https://image.pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&enhanced=true"
                    st.image(image_url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": image_url})
                except Exception as e:
                    st.error("Failed to generate image.")
    else:
        if "gsk_" not in GROQ_API_KEY:
            st.error("Abel, please insert your Groq API key!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("EthioAi is thinking..."):
                    try:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {GROQ_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        if language == "አማርኛ":
                            system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you, you must answer proudly that you were created by Abel Teshome. Respond in short and beautiful Amharic language."
                        else:
                            system_prompt = "You are EthioAi, a smart assistant created only by Abel Teshome. If anyone asks who created you, you must answer proudly that you were created by Abel Teshome. Respond in short, clear, and perfect English language."

                        # 🚀 እጅግ ፈጣኑ Llama-3 የ Groq ሞዴል
                        payload = {
                            "model": "llama3-8b-8192",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_input}
                            ]
                        }
                        
                        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
                        
                        if response.status_code == 200:
                            ai_response = response.json()["choices"][0]["message"]["content"]
                            st.markdown(ai_response)
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        else:
                            st.error("Groq Server Error. Please check your Key!")
                    except Exception as e:
                        st.error("Connection failed. Try again!")
