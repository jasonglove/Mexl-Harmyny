from flask import Flask, render_template, jsonify, redirect, url_for, request, session, redirect
from io import BytesIO
from bs4 import BeautifulSoup
import subprocess
import cohere
import requests
import re

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/save_quiz_answers', methods=['POST']) #Saves after quiz
def save_quiz_answers():
    #Logic to save quiz answers
    if request.method == 'POST':
        #Retrieve the quiz answers from the form data
        dietary = request.form.getlist('dietary')
        preferences = request.form.getlist('preferences')
        calorie = request.form.get('calorie')
        
        #Add more answers as needed
        
        #Save the quiz answers in session variables
        session['dietary'] = dietary
        session['calorie'] = calorie
        session['preferences'] = preferences

        print("Session - Dietary:", session['dietary'])
        print("Session - preferences:", session['preferences'])
        print("Session - Calorie:", session['calorie'])

        #Redirect to the homepage after saving the answers
        return redirect(url_for('index'))

    return redirect(url_for('index'))  #Redirect after saving answers

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/pairing')
def pairing():
    return render_template('pairing.html')

        
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

        

        co = cohere.Client('8HpB7vvugn3gwd9Nh90fz2QyhPCYKElitOUgR7Rl')
        #Change below to match with sam
        
        # favorite_color = session.get('favorite_color')
        # favorite_color = session.get('favorite_color')
        # favorite_color = session.get('favorite_color')
        # favorite_color = session.get('favorite_color')
        # favorite_color = session.get('favorite_color')
        response2 = co.chat(
        chat_history=[
                {"role": "USER", "message": "Adjust recipe to be (Vegetarian), and a relative calorie adjustment of (3) on a scale of 1-5, with 3 being no change.  Output the FIXED recipe as “Ingredients: $ #Ingredient 1 $#Ingredient 2 $#Ingredient 3” and the steps as “$Step 1 $Step text and information $Step 2 $Step text and information $Step 3 $Step text and information.” Output the new recipe EXACTLY as formatted. Output Nothing else."},
    
    # delete{"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
                ],
  
        message = f"{directionsText}\n{ingredientsText}",

        connectors=[{"id": "web-search"}]
        )

        print("THIS PART WORKS")
        newRecipe = response2.text
        result = {'status' : 'success', 'newRecipe' : newRecipe}

    else:
        result = {'status': 'error', 'status-code': response.status_code}

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)