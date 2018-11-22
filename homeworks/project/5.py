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
    url = 'https://www.kinopoisk.ru/index.php?kp_query=' + film_name +'&what='
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    if (soup.findAll("p", attrs={"class": ["name"]})): #если фильм существует
        href = soup.findAll("p", attrs={"class": ["name"]})[0].find('a')['href'] #ссылка на искомый фильм
        title = soup.findAll("p", attrs={"class": ["name"]})[0].find('a').text #название фильма
        href = href[:len(href)-5] #обрезаю ссылку
        new_url = 'https://www.kinopoisk.ru' + href + 'ord/rating/#list' #ссылка на отсортированные комменты (кнопка "Все")
        r = requests.get(new_url)
        soup = BeautifulSoup(r.text, "html.parser")
        comments = []
        #беру только 2 отзыва о фильме
        length = 2 if len(soup.findAll("div", attrs={"itemprop": ["reviews"]})) else len(soup.findAll("div", attrs={"itemprop": ["reviews"]}))
        for i in range(length-1):
            comments.append(soup.findAll("div", attrs={"itemprop": ["reviews"]})[i].findAll("span", attrs={"class": ["_reachbanner_"]})[0].text)
            comments[i] = comments[i].replace('\n', ' ').replace('\r', '').replace('\t', '').replace(u'\xa0', u' ').replace('\x97', '—').replace('\x85', '...').replace('\x88', '^')
        res = ''
        print(new_url)
        for i in comments: #запихиваю 2 отзыва в 1 строку
            res = res + i
        assessment = 0 if assessment < 6 else 1
        return [film_name, res, assessment]
    else:
        print('Введеное название фильма не найдено.') 

#print(parsing_reviews('Елки'))
#спарсить массив названий фильмов
films = ["Пираты ХХ века", "Гарри Поттер и Дары Смерти: Часть II", "Любить по-русски 2", "Опасный Бангкок", "Пила 8", "Уродцы", "Призрачный рейс", "Атлантида: Затерянный мир", "Преступник", "Новый Человек-паук", "Подмена", "Эдди Мерфи без купюр", "Вишенка на новогоднем торте", "Человек-улыбка", "Тринадцать друзей Оушена", "Нежная Ирма", "THX 1138", "Снег на голову", "Девушка, которая взрывала воздушные замки", "Рудо и Курси", "Цоци", "Осенью 41-го", "Не говори никому", "Любовники", "Суини Тодд, демон-парикмахер с Флит-стрит", "Маленькая мисс Счастье", "Ключ", "Бок о бок", "Горы", "Слезы капали", "Пассажиры", "Сало, или 120 дней Содома", "Команда из штата Индиана", "Срочно выйду замуж", "Ледяной ветер", "Гравитация", "Невероятная правда", "Пипец", "Чунгкингский экспресс", "Генетическая опера", "Приключения кота Фрица", "Оседлавший кита", "Извините, ошиблись номером", "Всё путём", "Убить пересмешника", "Элитный отряд: Враг внутри", "Голубой ангел", "Мобильник", "Три богатыря и Морской царь", "Играй, как Бекхэм", "Букашки. Приключение в Долине муравьев", "Зеленый театр в Земфире", "Великан", "Последний охотник на ведьм", "Принц Щелкунчик", "Молчание ягнят", "Четвертак", "Тарзан-размазня", "«Дюна» Ходоровского", "Форсаж 4", "После работы", "Боксер", "На цепи", "Честное крокодильское", "Схватка", "Алиса в Стране чудес", "Шайтан", "История игрушек 2", "Шайбу! Шайбу!", "Настоящая любовь", "Иван Царевич и Серый Волк", "Мамма MIA!", "Ловушка для одинокого мужчины", "Тесты для настоящих мужчин", "Мой самый страшный кошмар", "Любовник", "Максимка", "Беовульф", "Дикая вишня", "Сундук предков", "Бивень", "Глухие стены", "Призрак в доспехах", "Письма с Иводзимы", "Как украсть миллион", "СуперМакГрубер", "Убийство священного оленя", "Переводчик", "Аферисты Дик и Джейн", "Чёрная Пантера", "Мой путь", "Предсказание", "Рокко и его братья", "- Ишь ты, Масленица!", "Любящие сердца", "Золушка", "Пойга и Лиса", "Телохранитель", "Новая эра Z", "Эльза и Фред"]
sample = np.array([])
for i in films:
    print(i)
    np.append(sample, parsing_reviews(i))

print(sample)
data = pd.DataFrame(sample, columns = ['name', 'review', 'quality'])
#print(parsing_reviews('Любить по-русски 2'))



""" film_name = 'Опасный Бангкок'
url = 'https://www.kinopoisk.ru/index.php?kp_query=' + film_name +'&what='
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
if (soup.findAll("p", attrs={"class": ["name"]})): #если фильм существует
    href = soup.findAll("p", attrs={"class": ["name"]})[0].find('a')['href'] #ссылка на искомый фильм
    title = soup.findAll("p", attrs={"class": ["name"]})[0].find('a').text #название фильма
    href = href[:len(href)-5] #обрезаю ссылку
    new_url = 'https://www.kinopoisk.ru' + href + 'ord/rating/#list' #ссылка на отсортированные комменты (кнопка "Все")
    r = requests.get(new_url)
    soup = BeautifulSoup(r.text, "html.parser")
    comments = []
    #print(soup.findAll("div", attrs={"itemprop": ["reviews"]})[1].findAll("span", attrs={"class": ["_reachbanner_"]})[0])
    print(soup.findAll("span", attrs={"class": ["rating_ball"]})) """