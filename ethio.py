import streamlit as st
import requests

st.title("🤖 EthioAi")

# 🚨 Abel, remember to put your 3 real gsk keys in these quotes!
GROQ_API_KEYS = [
    "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",
    "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",
    "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"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# 🔄 1. Chat History System
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🖼️ 2. Image Mode Toggle System (Fixes the image generation bug)
if "image_mode" not in st.session_state:
    st.session_state.image_mode = False

# Display older chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):
            st.image(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

# 🎨 3. Layout for buttons and chat bar
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("💬 Chat Mode"):
        st.session_state.image_mode = False
        st.rerun()
with col2:
    if st.button("🖼️ Image Mode"):
        st.session_state.image_mode = True
        st.rerun()

# Show the user which mode is currently active
if st.session_state.image_mode:
    st.info("🎨 Current Mode: Image Generator (Write what you want to see)")
else:
    st.info("💬 Current Mode: English AI Chat")

# 💬 Chat Input Bar
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message and save to history
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🖼️ FIX: If Image Mode is ON, generate image directly using Pollinations AI
    if st.session_state.image_mode:
        with st.chat_message("assistant"):
            with st.spinner("EthioAi is painting your image..."):
                try:
                    # Clean the text for URL link
                    clean_prompt = user_input.replace(" ", "%20")
                    image_url = f"https://image.pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&enhanced=true"
                    
                    # Show image and save the URL to history
                    st.image(image_url, caption=f"🎬 Generated Image: {user_input}", use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": image_url})
                except Exception as e:
                    st.error("Sorry, failed to generate the image. Please try again.")

    # 💬 If Image Mode is OFF, reply in English text using Groq
    else:
        if "YOUR_REAL_KEY" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
            st.error("Abel, please insert your Groq gsk API keys in the code!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("EthioAi is thinking..."):
                    try:
                        current_key = GROQ_API_KEYS[st.session_state.key_index]
                        
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {current_key}",
                            "Content-Type": "application/json"
                        }
                        
                        # System prompt changed to English language only
                        payload = {
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {"role": "system", "content": "You are EthioAi, a smart assistant created by Abel. You must respond in professional, short, clear, and perfect English language."},
                                {"role": "user", "content": user_input}
                            ]
                        }
                        
                        response = requests.post(url, json=payload, headers=headers, timeout=15)
                        
                        if response.status_code == 200:
                            data = response.json()
                            ai_response = data["choices"][0]["message"]["content"]
                            
                            st.markdown(ai_response)
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                            
                        elif response.status_code in [429, 401, 400]:
                            st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                            st.warning("EthioAi switching server lines, please send your message again...")
                        else:
                            st.error(f"Groq Error Code: {response.status_code}")
                            
                    except Exception as e:
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                        st.error("Connection error, please resend your message.")
