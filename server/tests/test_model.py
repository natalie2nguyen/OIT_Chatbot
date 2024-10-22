import pandas as pd
from unittest.mock import patch
import sys
import os
from sklearn.metrics import accuracy_score

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from model import model 
from model import predict_intent

def test_question():
    with patch('model.pd.read_excel') as mock_read_excel:

        mocked_data = pd.DataFrame({
            'Question': ['i forgot my password', 'what is my username', 'how do i login', 'email issues', "i need to reactivate my DUO", 
                         "i got a new phone number and my DUO is not working", 'i need my DUO unlocked', 'i cant connect to the wifi',
                         'i need to connect to the VPN', 'my account is locked', 'is there onsite support'],
            'Intent': ['Password_reset', 'Username', 'Forgot_credentials', 'Email', 
                       'DUO_Reactivation', 'DUO_Change', 'DUO_Lock', 'Network_issues', 
                       'VPN_Access','Locked_account', 'On_site_support']
        })
        # Mocking the dataset loading
        mock_read_excel.return_value = mocked_data

        # Build the model (uses the mocked read_excel)
        trained_model, trained_vectorizer = model()

        predicted_intents = []
        actual_intents = mocked_data['Intent'].tolist()

        # Test the predict_intent function with a sample question
        for input_question in mocked_data['Question']: 
            predicted_intent = predict_intent(trained_model, trained_vectorizer, input_question)
            predicted_intents.append(predicted_intent)

        accuracy = accuracy_score(predicted_intents, actual_intents ) * 100
        assert accuracy >= 70, f"Test failed. Accuracy is {accuracy}."



           
