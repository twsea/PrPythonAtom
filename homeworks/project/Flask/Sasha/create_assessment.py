import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import nltk
#nltk.download('wordnet')
#nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from Sasha import parse

def assessment(title):
    data = pd.read_csv('D:\mail-python\PrPythonAtom\homeworks\project\Flask\Sasha\i8250_changed.csv',  sep='\t')
    lemmatizer = WordNetLemmatizer()
    import string
    exclude = set(string.punctuation)
    data['review'] = data['review'].apply(lambda x: " ".join(lemmatizer.lemmatize(i) for i in x.split()))

    vectorizer = CountVectorizer().fit(data['review'])
    features = vectorizer.transform(data['review'])
    clf = LogisticRegression()
    clf.fit(features[:data.shape[0]], data.quality[:data.shape[0]])


    res = parse.parsing_reviews(title)
    if res == 0:
        return 3
    film_name = res[0][0]
    review = res[0][1]

    review =  "".join(i for i in review if i not in exclude) 
    review_ = " ".join(lemmatizer.lemmatize(i) for i in review.split()) #???? let it be

    vector_review = vectorizer.transform([review_])
    return str(clf.predict(vector_review)[0]) #????



    


