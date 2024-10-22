import string
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
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

def model(): 
    df = pd.read_excel('server/src/dataset/OIT_Dataset.xlsx', sheet_name="Sheet1")
    df = df.sample(frac=1)

    df['Question'] = df['Question'].str.lower().str.replace(r'[^\w\s]', '', regex=True)

    stop_words = set(stopwords.words('english'))

    df['Question'] = df['Question'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

    X = df['Question']
    y = df['Intent']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # convert questions into numerical features using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train_tfidf, y_train)
    
    # return both the model and vectorizer because these need to be used to predict the intent
    return rf, vectorizer


def predict_intent(model: RandomForestClassifier, vect: TfidfVectorizer, question: string):
    
    question_tfidf = vect.transform([question])

    # Predict the intent
    predicted_intent = model.predict(question_tfidf)
    
    return predicted_intent[0]


if __name__ == '__main__':
    # call the model only once
    rf_model, tfidf_vect = model()

    question = input("Hi I am the OIT Chatbot, how can I assist you today?\n")
    
    intent = predict_intent(rf_model, tfidf_vect, question)
    
    print(intent)



    




