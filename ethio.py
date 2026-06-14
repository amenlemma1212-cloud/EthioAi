import streamlit as st
import requests

st.title("🤖 EthioAi")

# 🚨 አቤል ወንድሜ፣ 3ቱንም የ gsk ኮዶችህን እዚህ ጥቅስ ውስጥ በትክክል አስገባቸው!
GROQ_API_KEYS = [
    "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",
    "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",
    "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"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# 💬 የጽሕፈት ሳጥን ብቻ (የድምፅ ሲስተሙ ጠፍቷል)
user_input = st.chat_input("እዚህ ጋር የፈለጉትን ይጻፉ (ለምሳሌ፦ 'የወደፊት መኪና ምስል ሰብስብ')...")

if user_input:
    st.write(f"✍️ **እርስዎ፦** {user_input}")

    # 1. መጀመሪያ ተጠቃሚው ምስል እንዲፈጠርለት ከጠየቀ በነፃ ምስል የመፍጠሪያ ሲስተም
    if "ምስል" in user_input or "image" in user_input.lower() or "photo" in user_input.lower() or "ስዕል" in user_input:
        with st.spinner("EthioAi ምስል እየሳለ ነው..."):
            try:
                # የእንግሊዘኛ ትርጉም ለምስል መፍጠሪያው እንዲመች ወደ Groq እንልካለን
                current_key = GROQ_API_KEYS[st.session_state.key_index]
                translate_payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Translate the user prompt into a short English image generation prompt. Only return the English translation, nothing else."},
                        {"role": "user", "content": user_input}
                    ]
                }
                headers = {"Authorization": f"Bearer {current_key}", "Content-Type": "application/json"}
                trans_res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=translate_payload, headers=headers)
                
                if trans_res.status_code == 200:
                    image_prompt = trans_res.json()["choices"][0]["message"]["content"]
                else:
                    image_prompt = user_input
                
                # ነፃ የምስል መፍጠሪያ ሊንክ (Pollinations AI)
                image_url = f"https://image.pollinations.ai/p/{image_prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&enhanced=true"
                
                st.image(image_url, caption=f"🎬 በ EthioAi የተፈጠረ ምስል፦ {user_input}", use_container_width=True)
                st.success("ምስሉ በተሳካ ሁኔታ ተፈጥሯል!")
            except Exception as e:
                st.error("ይቅርታ፣ ምስሉን መፍጠር አልተቻለም።")

    # 2. ተራ የጽሑፍ ጥያቄ ከሆነ ቀጥታ በጽሑፍ ይመልሳል
    else:
        if "እዚህ_ይግባ" in GROQ_API_KEYS[0] or GROQ_API_KEYS[0] == "":
            st.error("አቤል ወንድሜ፣ እባክህ የ Groq gsk API ኮዶችህን አስገባ!")
        else:
            with st.spinner("EthioAi እያሰበ ነው..."):
                try:
                    current_key = GROQ_API_KEYS[st.session_state.key_index]
                    
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {current_key}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are EthioAi. Respond in short, clear, and fluent Amharic language."},
                            {"role": "user", "content": user_input}
                        ]
                    }
                    
                    response = requests.post(url, json=payload, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data["choices"][0]["message"]["content"]
                        st.write(f"🤖 **EthioAi፦** {ai_response}")
                    elif response.status_code in [429, 401, 400]:
                        st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                        st.warning("EthioAi መስመሩን እየቀየረ ነው፣ እባክህ ድጋሚ ላከው ወንድሜ...")
                    else:
                        st.error(f"የ Groq ኤረር ኮድ፦ {response.status_code}")
                        
                except Exception as e:
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(GROQ_API_KEYS)
                    st.error("እባክህ ድጋሚ ጥያቄህን ላከው።")
