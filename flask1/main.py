from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Добро пожаловать на мой сайт!</h1><p>Это главная страница.</p>"

@app.route('/about')
def about():
    return "<h1>О нас</h1><p>Этот сайт создан с использованием Flask.</p>"

if __name__ == '__main__':
    app.run(debug=True)
