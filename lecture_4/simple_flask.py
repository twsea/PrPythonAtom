
from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/members/<string:name>/")
def getMember(name):
    return name

if __name__ == "__main__":
    app.run()
#Теперь нужно запустить, через python simple_flask.py