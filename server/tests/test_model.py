import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from model import model  # Now you can import the function after modifying the path

# Mocking the stopwords and dataset
mocked_data = pd.DataFrame({
    'Question': ['how do i reset my password', 'what is my username'],
    'Intent': ['Password_reset', 'Username']
})

class TestIntentModel(unittest.TestCase):

    @patch('model.pd.read_excel')
    @patch('model.TfidfVectorizer')
    @patch('model.RandomForestClassifier')
    def test_question(self, mock_rf, mock_vectorizer, mock_read_excel):
        # Mocking stopwords and dataset
        mock_read_excel.return_value = mocked_data
        
        # Mock the TfidfVectorizer and RandomForestClassifier behavior
        mock_vectorizer_instance = MagicMock()
        mock_vectorizer_instance.transform.return_value = MagicMock()
        mock_vectorizer_instance.fit_transform.return_value = MagicMock()
        mock_vectorizer.return_value = mock_vectorizer_instance

        mock_rf_instance = MagicMock()
        mock_rf_instance.predict.return_value = ['Password_reset']  # Mock the prediction
        mock_rf.return_value = mock_rf_instance

        # Test the function with a sample question
        input_question = "How do I reset my password?"
        predicted_intent = model(input_question)

        # Assert that the predicted intent is correct
        self.assertEqual(predicted_intent, 'Password_reset')
