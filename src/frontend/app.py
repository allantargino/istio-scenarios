from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Calculator service!'

@app.route('/add/<int:x>/<int:y>')
def add(x,y):
    response = requests.get('http://calculator:5000/add/%d/%d' % (x,y)).json()
    return render_template('operation.v2.html', operation='add', result=response['result'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)