import sys
import os
from unittest.mock import patch
import pandas as pd


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.app import app, read_data
from src.chatbot import chatbot

def test_chat_endpoint():
    with app.test_client() as client:
        # Set up the test
        test_message = 'I forgot my password' 
        dictionary = {'Forgot_credentials':"Please specify which credential you need: Password, Username, or Email",
                      "Password_reset":"Please click on the following link to reset your password. https://myaccount.ucdenver.edu/change-password", 
                      "Username": "To obtain your username, you can go to the following website and click on 'Forgot my username?' under the 'Next Step' button. Your username will be sent to the email you registered your account with: https://myaccount.ucdenver.edu/change-password"
                      } 
        expected_response = chatbot(test_message, dictionary)

        # Make a request to the endpoint
        response = client.post('/chat', json={'message': test_message})

        # Check that the response is correct
        assert response.status_code == 200
        assert response.json['response'] == expected_response

def test_read_data():
    with patch('model.pd.read_excel') as mock_read_excel:
        mocked_data = pd.DataFrame([
            ["Forgot_credentials", "Please specify which credential you need: Password, Username, or Email"],
            ["Password_reset", "Please click on the following link to reset your password: https://myaccount.ucdenver.edu/change-password"],
            ["Username", "To obtain your username, you can go to the following website and click on 'Forgot my username?' under the 'Next Step' button. Your username will be sent to the email you registered your account with: https://myaccount.ucdenver.edu/change-password"]
        ])
        mock_read_excel.return_value = mocked_data
        dictionary = {
            "Forgot_credentials": "Please specify which credential you need: Password, Username, or Email",
            "Password_reset": "Please click on the following link to reset your password: https://myaccount.ucdenver.edu/change-password",
            "Username": "To obtain your username, you can go to the following website and click on 'Forgot my username?' under the 'Next Step' button. Your username will be sent to the email you registered your account with: https://myaccount.ucdenver.edu/change-password"
        }

        result = read_data()
        assert result == dictionary, f"Test failed. result is {result}."