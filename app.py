from flask import Flask, render_template, jsonify, redirect, url_for, request, session, redirect
from io import BytesIO
import subprocess

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_quiz_answers', methods=['POST']) #Saves after quiz
def save_quiz_answers():
    #Logic to save quiz answers
    if request.method == 'POST':
        #Retrieve the quiz answers from the form data
        fat = request.form.get('fat')
        #Add more answers as needed
        
        #Save the quiz answers in session variables
        session['fat_amount'] = fat
        
        #Redirect to the homepage after saving the answers
        return redirect(url_for('index'))

    return redirect(url_for('index'))  #Redirect after saving answers

@app.route('/recipe')
def quiz():
    return render_template('recipe.html')

@app.route('/pairing')
def pairing():
    return render_template('pairing.html')

if __name__ == '__main__':
    app.run(debug=True)