import streamlit as st
import requests

st.set_page_config(page_title="PyGuide AI", page_icon="🧠")
st.title("🧠 PyGuide – Your Personal AI Mentor")

# Input
user_input = st.text_input("What would you like to ask PyGuide?")

if user_input:
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3-70b-chat-hf"
    headers = {
        "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
        "Content-Type": "application/json"
    }

    # PyGuide's behavior (system prompt embedded in prompt)
    prompt = f"[INST] <<SYS>>You are PyGuide, an expert and friendly AI mentor that helps students understand code, concepts, and projects clearly. Be concise, supportive, and educational.<</SYS>> {user_input} [/INST]"

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }

    with st.spinner("PyGuide is thinking..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            answer = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text')
            st.markdown(answer or "No reply generated.")
        else:
            st.error(f"Error: {response.status_code}\n{response.text}")

