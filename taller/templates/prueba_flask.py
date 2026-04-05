from flask import Flask
app = Flask(__name__)

@app.route('/')
def hola():
    return '¡Flask funciona!'

if __name__ == '__main__':
    app.run(port=5000)