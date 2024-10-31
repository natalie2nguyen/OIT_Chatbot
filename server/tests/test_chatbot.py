import nltk
nltk.download('punkt_tab')
from unittest.mock import patch
import pandas as pd



# test_preprocess_input.py

import sys
import os

# Adjust the Python path to include the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the preprocess_input function from src.chatbot
from src.chatbot import preprocess_input

from src.chatbot import match_intent_to_response

def test_preprocess_normal_input():
    input_text = "This is a sample message with punctuation! Very nice."
    expected_output = "sample message punctuation nice"
    assert preprocess_input(input_text) == expected_output

def test_preprocess_empty_input():
    input_text = ""
    expected_output = ""
    assert preprocess_input(input_text) == expected_output

def test_preprocess_only_stopwords():
    input_text = "is the in and"
    expected_output = ""
    assert preprocess_input(input_text) == expected_output

def test_preprocess_only_punctuation():
    input_text = "!@#$%^&*()"
    expected_output = ""
    assert preprocess_input(input_text) == expected_output

def test_preprocess_lemmatization():
    input_text = "running runners ran"
    expected_output = "running runner ran"
    assert preprocess_input(input_text) == expected_output

def test_match_intent_to_response():
    intent = "Password_reset"
    expected_output = "Please click on the following link to reset your password: https://myaccount.ucdenver.edu/change-password"
    dictionary = {'Forgot_credentials':"Please specify which credential you need: Password, Username, or Email",
                      "Password_reset":"Please click on the following link to reset your password: https://myaccount.ucdenver.edu/change-password", 
                      "Username": "To obtain your username, you can go to the following website and click on 'Forgot my username?' under the 'Next Step' button. Your username will be sent to the email you registered your account with: https://myaccount.ucdenver.edu/change-password"
                      } 
    assert match_intent_to_response(intent, dictionary) == expected_output

