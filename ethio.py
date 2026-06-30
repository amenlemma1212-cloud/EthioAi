import streamlit as st
import requests
import json

st.title("🇪🇹 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱን የ OpenRouter (sk-or-...) ኮዶችህን እዚህ ጥቅስ ውስጥ አስገባቸው!
OPENROUTER_API_KEYS = [
    " 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 ",
    " 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 ",
    " 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 "
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

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
        if "እዚህ_ይግባ" in OPENROUTER_API_KEYS[0] or OPENROUTER_API_KEYS[0] == "":
            st.error("Abel, please insert your OpenRouter API keys!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("EthioAi is thinking..."):
                    response_success = False
                    attempts = 0
                    while not response_success and attempts < len(OPENROUTER_API_KEYS):
                        try:
                            current_key = OPENROUTER_API_KEYS[st.session_state.key_index]
                            url = "https://openrouter.ai/api/v1/chat/completions"
                            headers = {
                                "Authorization": f"Bearer {current_key}",
                                "Content-Type": "application/json"
                            }
                            if language == "አማርኛ":
                                system_prompt = "You are EthioAi, created by Abel Teshome. Respond in short Amharic."
                            else:
                                system_prompt = "You are EthioAi, created by Abel Teshome. Respond in short English."

                            payload = {
                                "model": "google/gemini-2.5-flash:free",
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
                                response_success = True
                            else:
                                st.session_state.key_index = (st.session_state.key_index + 1) % len(OPENROUTER_API_KEYS)
                                attempts += 1
                        except Exception as e:
                            st.session_state.key_index = (st.session_state.key_index + 1) % len(OPENROUTER_API_KEYS)
                            attempts += 1
                    if not response_success:
                        st.error("All server lines are busy. Please check your OpenRouter Keys!")
