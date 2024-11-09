from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
model = genai.GenerativeModel('gemini-pro')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    chat = model.start_chat(history=[])
    response = chat.send_message(user_input)
    response_text = ''.join([chunk.text for chunk in response])
    return jsonify({'response': response_text})

if __name__ == "__main__":
    app.run(debug=True)
