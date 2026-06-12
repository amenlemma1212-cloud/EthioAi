import streamlit as st
import requests

st.set_page_config(page_title="EthioAi", page_icon="🤖")
st.title("🤖 EthioAi")

# ⚠️ አቤል ወንድሜ፣ ያንን የ Hugging Face hf_ ቁልፍህን እዚህ መሃል ብቻ በትክክል አቆየው
HF_TOKEN = "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"

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
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        ai_reply = ""
        
        # --- ሰርቨር 1: Meta Llama 3 (ዋናው AI) ---
        url1 = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        payload1 = {
            "inputs": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "parameters": {"max_new_tokens": 500, "return_full_text": False}
        }
        
        try:
            response = requests.post(url1, headers=headers, json=payload1, timeout=12)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    ai_reply = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    ai_reply = result.get("generated_text", "")
        except:
            pass  # የመጀመሪያው ካልሠራ ወደ ሁለተኛው ያልፋል
            
        # --- ሰርቨር 2: Microsoft Phi 3 (መጠባበቂያ AI - 1ኛው Full ሲሆን ይህ ይተካል) ---
        if not ai_reply:
            url2 = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
            payload2 = {
                "inputs": f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
                "parameters": {"max_new_tokens": 500, "return_full_text": False}
            }
            try:
                response = requests.post(url2, headers=headers, json=payload2, timeout=12)
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        ai_reply = result[0].get("generated_text", "")
                    elif isinstance(result, dict):
                        ai_reply = result.get("generated_text", "")
            except:
                pass
                
        # --- ሁለቱም ሰርቨሮች በጣም ስራ ከበዛባቸው ብቻ የሚመጣ መልእክት ---
        if not ai_reply:
            ai_reply = "ይቅርታ፣ የአገልጋይ ስራ መብዛት አጋጥሟል። እባክህ ጥቂት ቆይተህ ድጋሚ ሞክር።"
            
        message_placeholder.markdown(ai_reply)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
