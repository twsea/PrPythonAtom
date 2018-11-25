from flask import Flask, request, jsonify,json, Response, render_template
import os.path
import create_assessment

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('start.html')

@app.route('/input-film-assessment')
def asess():
    return render_template('signUp.html')


@app.route('/film-assessment', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        my_result = request.form
        title = my_result['Name']
        res = {}
        assesment = create_assessment.assessment(title)
        print(assesment)
        if int(assesment) == 1:
                res['Name'] = 'Наша система говорит, что фильм "'+title+ '" будет интересным'
        elif int(assesment) == 0:
                res['Name'] = 'Наша система определила, что фильм "'+title+  '" будет не самым увлекательным'  
        else:
                res['Name'] = 'К сожалению, данные о фильме не были найдены.'

        return render_template('signUpUser.html', result = res)


@app.route('/suggest')
def res():
        return render_template('suggest.html')

if __name__=="__main__":
    app.run(debug = True)