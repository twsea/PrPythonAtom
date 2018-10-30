from flask import Flask, request, jsonify,json

app = Flask(__name__)

@app.route("/get_classifier_result/<version>", methods=['GET', 'POST'])
def return_classifier_result(version):
    #TODO прочитать из полученного запроса json-контент
    if request.method == 'POST':
        r = request.get_json()
        if int(version) == 1:
            return jsonify(version = 1, predict = r['predict'])
        else:
            return jsonify(version = 0, predict = r['old_predict'])
    #В случае, если version==1, то должен вернуться json с версией и полем predict из входящего jsonа {"version":1, "predict":<predict_value>}
    #В случае, если version==0, то должен вернуться json с версией и полем old_predict из входящего jsonа {"version":0, "predict":<old_predict_value>}
@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
    return 'Перейдите по ссылке http://127.0.0.1:5000/get_classifier_result/0 и вам выведется версия и значение predict. То же самое для версии 1 - перейдите по ссылке http://127.0.0.1:5000/get_classifier_result/1 и выведется значение old_predict' 


if __name__ == "__main__":
    app.run()
    
    