from flask import Flask, request, jsonify
from flask_cors import CORS
from .chatbot import chatbot # Relative import for unit testing
from pathlib import Path
import pandas as pd


app = Flask(__name__)
CORS(app)  # Need to enable cors for the frontend to be able to make requests

intent_response = None

def read_data():
    global intent_response
    if intent_response is None: 
        file_path = Path(__file__).parent / 'dataset/OIT Responses.xlsx'
        df = pd.read_excel(file_path, sheet_name="Sheet1")    
        intent_response = {}
        intents = df.iloc[:, 0]
        responses = df.iloc[:, 1]
        for intent_key, response in zip(intents, responses): 
            intent_response[intent_key] = response 
    return intent_response

@app.route('/chat', methods=['POST'])    

def chat():
    user_message = request.json.get('message')
    if intent_response is None:
        read_data()
    
    bot_response = chatbot(user_message, intent_response)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
