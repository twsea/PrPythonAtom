from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

class PrefixTree:
    def __init__(self):
        self.root = [{}]
        
    def add(self, string):
        if self.check(string): #проверяет полностью, если слово входит в дерево, то ничего не делает
            return
        wrk_dict = self.root #wrk_dict теперь равно дереву
        for i in string: #перебирает буквы в строке. по-любому проходит все слово до конца
            if i in wrk_dict[0]: #смотрит, есть ли текущая буква в ключе словаря
                wrk_dict = wrk_dict[0][i] #обращаемся к словарю по ключу "i"
            else:
                wrk_dict[0][i] = [{}] #записываем по ключу "i"  снова список с пустым словарем внутри
                wrk_dict = wrk_dict[0][i] #переходим в свежезаписанный list
        wrk_dict.append(True) #записываем в последний list (конец текущего слова) "True"
        #TODO добавить строку
        
    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i] #если буква-ключ есть, то углубляемся
            else:
                return False
        if len(wrk_dict) != 1: #если содержит еще и True в массиве => слово входит полностью
            return True
        return False
        #TODO проверить наличие строки
    
    def check_part(self, string): #всегда проверят от начала
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True
    def top_10 (self, string):
        pass
    #TODO реализация класса prefix tree, методы как на лекции + метод дать топ 10 продолжений. 
    
    # Скажем на строку кросс выдаем кроссовки, кроссовочки итп. Как хранить топ? 
    #Решать вам. Можно, конечно, обходить все ноды, но это долго. Дешевле чуток поиграть по памяти, зато отдавать быстро (скажем можно взять кучу)
    # В терминальных (конечных) нодах может лежать json с топ актерами.

def init_prefix_tree(filename):
    pass
    #TODO в данном методе загружаем данные из файла. Предположим формат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости


@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    pass
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод

@app.route("/")
def hello():
    #TODO должна возвращаться инструкция по работе с сервером
    return 0

if __name__ == "__main__":
    app.run()
