import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords

# approach:
# clean and preprocess the questions (remove punctuation, lowercase the text, etc.).
# remove stop words (like "is", "my", "the")
# use TF-IDF (Term Frequency-Inverse Document Frequency) to convert the questions into numerical vectors


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


# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Predict the intent on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
print(f'Logistic Regression Accuracy: {accuracy_score(y_test, y_pred)}')
# print(classification_report(y_test, y_pred))
print()
##############################################
from sklearn.linear_model import SGDClassifier

sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
sgd.fit(X_train, y_train)

y_pred = sgd.predict(X_test)

print('Linear Support Vector machine accuracy %s' % accuracy_score(y_pred, y_test))
# print(classification_report(y_test, y_pred))
print()

###################
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_tfidf, y_train)
y_pred_rf = rf.predict(X_test_tfidf)

print(f'Random Forest Accuracy: {accuracy_score(y_test, y_pred_rf)}')
print()
# # print(classification_report(y_test, y_pred))
# print()

from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(random_state=42)
gb.fit(X_train_tfidf, y_train)
y_pred_gb = gb.predict(X_test_tfidf)

print(f'Gradient Boosting Accuracy: {accuracy_score(y_test, y_pred_gb)}')
print()

from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.1, 1, 10, 100, 1000], 'penalty': ['l2']}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid.fit(X_train_tfidf, y_train)

print(f'Best parameters: {grid.best_params_}')
print(f'Best accuracy: {grid.best_score_}')



