from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import minmaxheap

app = Flask(__name__)

class PrefixTree:
    def __init__(self):
        self.root = [{}]
        self.amount = 0
        
    def add(self, string):
        string = string.lower() #делаю все буквы маленькими
        wrk_dict = self.root #wrk_dict теперь равно дереву
        for i in string: #перебирает буквы в строке. по-любому проходит все слово до конца
            if i in wrk_dict[0]: #смотрит, есть ли текущая буква в ключе словаря
                wrk_dict = wrk_dict[0][i] #обращаемся к словарю по ключу "i"
            else:
                if len(wrk_dict) == 1: #если list состоит только из словаря, т.e. слово ранее не записывалось
                    wrk_dict.append(0)
                wrk_dict[0][i] = [{}] #записываем по ключу "i"  снова список с пустым словарем внутри
                wrk_dict = wrk_dict[0][i] #переходим в свежезаписанный list
        if len(wrk_dict) == 1: #если list состоит только из словаря, т.e. слово ранее не записывалось
            wrk_dict.append(1) 
        else:
            wrk_dict[1] = wrk_dict[1] + 1 
        self.amount += 1
        #TODO добавить строку
        
        
    def check(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i] #если буква-ключ есть, то углубляемся
            else:
                return False
        if wrk_dict[1] == True:
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

    def show_tree(self):
        w = self.root
        s = ''
        p = [[]] #выводит массив со словами
        for key in w[0]:
            self.recur(p, w,s,key)
        del  p[len(p)-1]
        #print(p)
        return p

    def recur (self, array, w,string, key): #обход дерева
        string = string + key
        if len(list(w[0][key][0].keys())) == 0: #если внутренний словарь пуст, значит это последняя буква слова
            array[len(array)-1].append(string)
            array[len(array)-1].append(w[0][key][1])
            array.append([])
        else:
            w = w[0][key] #иначе переходим по текущему ключу в его внутренний словарь
            for m in list(w[0].keys()): #перебираем все ключи во внутреннем словаре
                self.recur(array, w,string,m)

    def return_part_of_tree(self, string): #показать часть дерева после введенной строки
        string = string.lower()
        if self.check_part(string): #если слово присутствует в дереве
            wrk_dict = self.root
            for i in string: #добираемся до нужного list
                wrk_dict = wrk_dict[0][i]
            s = string
            p = [[]] #выводит массив со словами
            for key in wrk_dict[0]:
                self.recur(p, wrk_dict,s,key)
            del p[len(p)-1]
            if len(p) == 0: #если вернулся пустой массив, т.е. если строка равно макс. слову в дереве
                p = [[string,1]]
            return p
        else:
            print("Ничего не найдено")
        

    def top_10 (self,string):
        if not self.check_part(string):
            return "Ничего не найдено"
        p = self.return_part_of_tree(string)
        p = p[:len(p)] #обрезаю по 10-й, это же топ_10
        p = minmaxheap.MaxHeap(p).array
        top_10_str = ''
        for i in range(len(p)):
            top_10_str =  top_10_str + p[i][0]
            if i != len(p)-1:
                top_10_str =  top_10_str + ', '
        return top_10_str

                    

def init_prefix_tree(filename):
    f = open(filename)
    l = [line.strip() for line in f] #массив из строк, записанных в файле
    f.close()
    if l[len(l)-1] == '': #обработка последнего элемента
        del l[len(l)-1]
    pr_tree = PrefixTree()
    for i in range(len(l)):
        pr_tree.add(l[i])
    return pr_tree

    #TODO в данном методе загружаем данные из файла. Предположим формат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости


@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    result = init_prefix_tree('info.txt').top_10(string)
    return str(result)
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод

@app.route("/")
def hello():
    return 'Добавьте в конец ссылки /get_sudgest/string, где string - слово, продолжение которого вы хотите получить.\nПрограмма работает корректно только для латинского алфавита.'

if __name__ == "__main__":
    app.run()