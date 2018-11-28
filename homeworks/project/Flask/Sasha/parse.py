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

def parsing_reviews (film_name): #возвращает массив типа [название, отзывы, оценка]
    film_name_new = film_name.replace('&','')
    film_name_new = film_name_new.replace(' ','+')
    print(film_name_new)
    url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q='+ film_name_new + '&s=all'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    flag = 0
    print(url)
    if (not soup.findAll("div", attrs={"class": ["findNoResults"]})): #если фильм существует
        if(soup.findAll("h3", attrs={"class": ["findSectionHeader"]})):
            if (soup.findAll("h3", attrs={"class": ["findSectionHeader"]})[0].text == 'Titles'):
                flag = 1

    else:
        print('Введеное название фильма не найдено.') 
        return 0 #TODO проработать возврат
    if flag == 1:
        href = soup.findAll("td", attrs={"class": ["result_text"]})[0].find('a')['href'] #ссылка на искомый фильм
        title = soup.findAll("td", attrs={"class": ["result_text"]})[0].find('a').text #название фильма
        #взять рейтинг на главной странице
        url_main = 'https://www.imdb.com' + href
        r = requests.get(url_main)
        print(url_main)
        soup = BeautifulSoup(r.text, "html.parser")
        if not soup.findAll("span", attrs={"itemprop": ["ratingValue"]}):
            print(5)
            return 0
        rating = float(soup.findAll("span", attrs={"itemprop": ["ratingValue"]})[0].text) 
        assessment = 0 if rating < 7.5 else 1
        #получить комментарии
        position_of_question = href.find('?')
        new_href = href[:position_of_question]
        url_reviews = 'https://www.imdb.com' + new_href + 'reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0' #ссылка на reviews
        r = requests.get(url_reviews)
        soup = BeautifulSoup(r.text, "html.parser")      
        reviews = []

        #брать все отзывы, но обрезать. 5 отзывов по 20 слов

        length = 5 if len(soup.findAll("div", attrs={"class": ["content"]})) > 5 else len(soup.findAll("div", attrs={"class": ["content"]}))
        
        for i in range(length):
            review = soup.findAll("div", attrs={"class": ["content"]})[i].find('div').text
            review = review.replace('\n', ' ').replace('\r', '').replace('\t', '').replace(u'\xa0', u' ').replace('\x97', '—').replace('\x85', '...').replace('\x88', '^').replace("\'", "'")
            index = 0
            review = review[::-1]
            if len(review) > 60:             
                for i in range(60):
                    index = review.find(' ', index+1)
                review = review[:index] #обрезаем по 60 слов
            review = review[::-1]
            reviews.append(review)
        
        res = ''
        for i in reviews: #запихиваю все отзывы в 1 строку
            res = res + i + ' '
        return [[film_name, res,rating, assessment]]
    if 1 == 1:
        return 0