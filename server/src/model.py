import string
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier


# approach:
# clean and preprocess the questions (remove punctuation, lowercase the text, etc.).
# remove stop words like "is", "my", "the"
# use TF-IDF (Term Frequency-Inverse Document Frequency) to convert the questions into numerical vectors
# in comparison to CountVectorizer, CV just counts the frequency of a word in a given sentence/input
# TF_IDF counts the frequency AND the Inverse Document Frequency
# use Random Forest Classifier 
# predict the intent of the user's question/input

import re
def model(question: string): 
    df = pd.read_excel('server/src/OIT_Dataset.xlsx', sheet_name="Sheet1")
    df = df.sample(frac=1)

    df['Question'] = df['Question'].str.lower().str.replace('[^\w\s]', '', regex=True)
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    df['Question'] = df['Question'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

    X = df['Question']
    y = df['Intent']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Convert questions into numerical features using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train_tfidf, y_train)
    # y_pred = rf.predict(X_test_tfidf)

    # #print(pd.DataFrame({'Predicted': y_pred, 'Actual': y_test.values}))
    # print(f'Random Forest Accuracy: {accuracy_score(y_test, y_pred)}')

    # strip the user's question of punctuation and stop words
    question = question.lower()
    question = re.sub(r'[^\w\s]', '', question)
    stop_words = set(stopwords.words('english'))
    question = ' '.join([word for word in question.split() if word not in stop_words])
    question_tfidf = vectorizer.transform([question])

    # Predict the intent
    predicted_intent = rf.predict(question_tfidf)
    
    return predicted_intent[0]


if __name__ == '__main__':
    question = input("Hi I am the OIT Chatbot, how can I assist you today?\n")
    print(model(question))
    




