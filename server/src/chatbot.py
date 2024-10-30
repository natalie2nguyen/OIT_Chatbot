import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
from pathlib import Path


from .model import predict_intent, model

# This is the access point for the app to interact with the chatbot
def chatbot(user_message):
    preprocessed_message = preprocess_input(user_message)
    rf_model, tfidf_vect = model()
    intent = predict_intent(rf_model, tfidf_vect,preprocessed_message)
    itent_dictionary = read_data()
    output = match_intent_to_response(intent, itent_dictionary)
    return output    

def preprocess_input(user_message):
    # Convert the user message to lowercase
    user_message = user_message.lower()
    # Remove punctuation
    user_message = re.sub(r'[^\w\s]', '', user_message)
    # Tokenize the text
    tokens = word_tokenize(user_message)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize the text
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Rejoin tokens into a string
    processed_message = ' '.join(tokens)
    return processed_message

def read_data():
    file_path = Path(__file__).parent / 'dataset/OIT Responses.xlsx'
    df = pd.read_excel(file_path, sheet_name="Sheet1")    
    intent_response = {}
    intents = df.iloc[:, 0]
    responses = df.iloc[:, 1]
    for intent_key, response in zip(intents, responses): 
        intent_response[intent_key] = response 
    return intent_response

def match_intent_to_response(intent, intent_response):
    if intent in intent_response:
        return intent_response[intent]
    else: 
        return "I'm sorry, I'm not sure if I understand. Could you provide me with more details please?"



