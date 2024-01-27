from flask import Flask, render_template, jsonify, redirect, url_for, request, session, redirect
from io import BytesIO
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe')
def quiz():
    return render_template('recipe.html')

@app.route('/pairing')
def pairing():
    return render_template('pairing.html')

if __name__ == '__main__':
    app.run(debug=True)