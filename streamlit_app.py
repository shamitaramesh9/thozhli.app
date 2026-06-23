import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Thozhi - Your AI Sister", page_icon="👩", layout="centered")

st.title("Thozhi (தோழி) 👩")
st.markdown("### *Your AI Sister — Here to support, listen, and guide.*")
st.write("---")

# 2. Securely pull the API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 3. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Thozhi (தோழி), an affectionate, highly empathetic, and supportive elder sister for Indian homemakers and mothers. Speak warmly, validate their feelings, use comforting language, and offer clear guidance on household, lifestyle, or emotional well-being questions."}
    ]

# 4. Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. User Input
if user_prompt := st.chat_input("Talk to your sister here..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # 6. Call Groq API via Cloud Requests (Zero laptop RAM used!)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192", 
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 200:
                    assistant_response = response.json()["choices"][0]["message"]["content"]
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    st.error(f"Error: Unable to fetch response from API. (Status Code: {response.status_code})")
            except Exception as e:
                st.error("Connection error. Please try again.")