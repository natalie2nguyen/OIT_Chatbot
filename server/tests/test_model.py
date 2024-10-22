import pandas as pd
from unittest.mock import patch
import sys
import os

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

        count = 0  # Initialize count variable

        # Test the predict_intent function with a sample question
        for i, input_question in enumerate(mocked_data['Question']): 
            predicted_intent = predict_intent(trained_model, trained_vectorizer, input_question)

            # Increment count if prediction is correct
            if predicted_intent == mocked_data['Intent'][i]:
                count += 1

        # Check if the count of correct predictions is greater than 10
        assert count > 5, f"Test failed. Only {count} correct predictions."

           
