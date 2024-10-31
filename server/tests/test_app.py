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
            'Password_reset': 'Please click on the following link to reset your password. https://myaccount.ucdenver.edu/change-password', 'Username': "To obtain your username, you can go to the following website and click on 'Forgot my username?' under the 'Next Step button. Your username will be sent to the email you registered your account with. https://myaccount.ucdenver.edu/change-password", 'Email': 'Please click on the following link to claim your account. After step 1, you will receive your email address (if your account has already been claimed). https://myaccount.ucdenver.edu/step6.php', 'DUO_Reactivation': 'To reactivate your DUO account, please click on the following website > scroll down to frequently asked questions > Click on “I upgraded to a new phone and now DUO is not working. How do I reactivate Duo?” and follows these steps https://www.cuanschutz.edu/offices/office-of-information-technology/tools-services/detail-page/multi-factor-authentication--mfa--with-duo. If you continue to have issues, please give us a call at 303-724-4357.', 'DUO_Change': 'To change the phone number in your DUO account, please give us a call at 303-724-4357.', 'DUO_Lock': 'To unlock or re-enable your DUO account, please give us a call at 303-724-4357.', 'Network_issues': 'To connect to CU Denver’s network “AurariaNet,” you will need to login with your university credentials. This includes your username and password.', 'VPN_Access': 'Please refer to our page on VPN access. https://www.ucdenver.edu/offices/office-of-information-technology/tools-services/remote-access-vpn. If you continue to have issues, please give us a call at 303-724-4357.', 'Locked_account': 'To unlock your account, please give us a call at 303-724-4357.', 'On_site_support': 'For classroom or conference room IT help, please call 303-315-2055. For other IT help issues please give us a call at 303-724-4357.'
        }

        result = read_data()
        assert result == dictionary, f"Test failed. result is {result}."