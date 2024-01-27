from flask import Flask, render_template, jsonify, redirect, url_for, request, session, redirect
from io import BytesIO
from bs4 import BeautifulSoup
import subprocess
import requests
import re

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/pairing')
def pairing():
    return render_template('pairing.html')

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

@app.route('/find-recipe', methods=['GET', 'POST'])
def find_recipe():

    # Define the URL of the webpage you want to scrape
    url = request.form.get('url-input')

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with a certain class (e.g., 'your_class_name')
        ingredientsQuantity = soup.find_all('span', {'data-ingredient-quantity': 'true'})
        ingredientsUnit = soup.find_all('span', {'data-ingredient-unit': 'true'})
        ingredientsName = soup.find_all('span', {'data-ingredient-name': 'true'})

        # Extract the text content from each element
        ingredientsText = ""
        for quantity, unit, name in zip(ingredientsQuantity, ingredientsUnit, ingredientsName):
            # Extract the text content of the element
            ingredientsText += f"{quantity} {unit} {name}\n"


        directions = soup.find_all('p', {'class': 'comp mntl-sc-block mntl-sc-block-html', 'id': re.compile(r'mntl-sc-block_2-0-\d+')})

        i = 1
        directionsText = ""
        for direction in directions:
            directionsText += f"Step {i}:\n{direction}\n"
            i+=1

        result = {'status': 'success', 'ingredients': ingredientsText, 'directions' : directionsText}

    else:
        result = {'status': 'error', 'status-code': response.status_code}

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)