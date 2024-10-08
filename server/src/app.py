from flask import Flask, request, jsonify
from flask_cors import CORS
from .chatbot import chatbot # Relative import for unit testing

app = Flask(__name__)
CORS(app)  # Need to enable cors for the frontend to be able to make requests

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_response = chatbot(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
