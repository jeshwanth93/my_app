import streamlit as st
import requests

st.set_page_config(page_title="PyGuide", page_icon="🧠")
st.title("🧠 PyGuide – Ask Your AI Mentor")

# ✅ Set the model URL here (LLaMA 3.3)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"

# Input from user
user_input = st.text_input("What would you like to ask PyGuide?")

# Only run if input is provided
if user_input:
    headers = {
        "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
        "Content-Type": "application/json"
    }

    # Construct prompt with system instruction for PyGuide
    prompt = f"[INST] <<SYS>>You are PyGuide, a helpful AI mentor who explains coding, AI, and projects clearly and patiently.<</SYS>> {user_input} [/INST]"

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }

    with st.spinner("PyGuide is thinking..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text')
            st.markdown(reply or "No response generated.")
        else:
            st.error(f"Error: {response.status_code}\n{response.text}")


