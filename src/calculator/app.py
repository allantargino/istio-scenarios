from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Calculator service!'

@app.route('/add/<int:x>/<int:y>')
def add(x,y):
    return jsonify(result=x+y)

@app.route('/times/<int:x>/<int:y>')
def times(x,y):
    return jsonify(result=x+y)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
