from flask import Flask, render_template, url_for, redirect, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about-us')
def about():
    return render_template('about-us.html')


@app.route('/services')
def services():
    return render_template('services/services.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')


if __name__ == '__main__':
    app.run(debug=True)