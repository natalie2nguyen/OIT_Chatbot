import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# This is the access point for the app to interact with the chatbot
def chatbot(user_message):
    # Just a placeholder for now
    return "Hello, I am a chatbot. How can I help you today?"

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


