from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, world!'

if __name__ == '__main__':
    print('Hello, world!')
    app.run(host='0.0.0.0', debug=True)
    