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
<<<<<<< HEAD
    # Just a placeholder for now
<<<<<<< HEAD
    message = "Hello, I am a chatbot. How can I help you today?"

    return message
=======
    return "Hello, I am a chatbot. How can I help you today?"
=======
    preprocessed_message = preprocess_input(user_message)
    intent = match_input_to_intent(preprocessed_message)
    output = match_intent_to_output(intent)
    return output    
>>>>>>> 0d88268e (Preparsed the input)

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

def match_intent_to_output(intent_list):
    # Loop through each word in the processed message
    output = []
    for word in intent_list.split():
        # Match the word to an intent
        # For now, we'll just return a placeholder intent
        if word == 'hello':
            output.append('greetings')
    
    if len(output) == 0:
        output.append('no_intent')
    return output
        
def match_input_to_intent(processed_message):
    # Placeholder
    return processed_message


<<<<<<< HEAD
>>>>>>> e2350a51 (preprocessing input)
=======

    return message
>>>>>>> e17b64ac (task: reowrked based on comments on PR)
