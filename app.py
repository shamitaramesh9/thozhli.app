import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Pointing to a local running LLM engine (Ollama)
LLM_API_URL = "http://localhost:11434/api/generate"  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").strip()
    
    if not user_message:
        return jsonify({"reply": "I am right here listening, talk to me."})

    system_instructions = (
        "You are Thozhi (தோழி), an affectionate, mature, and deeply understanding AI companion "
        "specially created for Indian homemakers and mothers. Speak like a loving, reliable peer or close sister. "
        "You can answer ANY general knowledge query, household advice, or lifestyle problem, "
        "but your underlying tone must ALWAYS remain supportive, patient, and uplifting. "
        "Keep answers concise, reassuring, and comforting. Respond directly to the user's message now:"
    )

    full_prompt = f"{system_instructions}\nUser: {user_message}\nThozhi:"

    payload = {
        "model": "llama3.2",  
        "prompt": full_prompt,
        "stream": False  # Crucial: this tells Ollama to send the full text at once instead of word-by-word
    }

    try:
        response = requests.post(LLM_API_URL, json=payload, timeout=30)
        response_json = response.json()
        
        # Ollama returns the generated text inside the "response" key
        bot_reply = response_json.get("response", "").strip()
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        print(f"Ollama Error: {e}")
        return jsonify({
            "reply": "Amma, I can hear you, but my system is currently updating its connection lines. Sit back, drink some warm water, and let's talk properly in a quick minute!"
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)