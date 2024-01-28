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
        
        dietary_r = session.get('dietary')
        calorie_r = session.get('calorie')
        preferences_r = session.get('preferences')
       
       # if(len(dietary_r) == 0):
       #     dietary_r[0]="No Dietary restrictions"

        #print("Dietary ", dietary_r[0], " ", len(dietary_r))
        
        response2 = co.chat(


        chat_history=[
                {"role": "USER", "message": "I am interested in making more nutritious meals. Here are my dietary requirements. These have to be followed  {dietary_r}. This is my calorie range. 1 is the lowest and 5 is the highest let 3 represent no change. {calorie_r}   These are my preferences: {preferences_r}. The output should be every ingredient with measurements seperated from each other by a -. The next output should be all of the steps are listed seperated from each other by -. An example is: Ingredients: -1 cup rice -2 pounds chicken -Steps: -Step 1: cook rice -Step 2: Cook chicken -Step 3: Enjoy!. INCLUDE ALL STEPS THIS IS NECCESSARY AND WILL RUIN EVERYTHING IF NOT ALL ARE USED. REMEMBER TO USE -STEP formatting. INCLUDE NO OTHER WORDS."},
    
    # delete{"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
        ],
  
        message = f"{directionsText}\n{ingredientsText}",

        connectors=[{"id": "web-search"}]
        )
        #THis is a string with the entire response
        newRecipe = response2.text

        pattern_I = r'(Ingredients:)'

        newRecipe = re.sub(pattern_I, r'<h2>\1</h2>', newRecipe)

        pattern_S = r'(Steps:)'

        newRecipe = re.sub(pattern_S, r'<br><h2>\1</h2>', newRecipe)

        pattern = r'(-|\b\d{1,2}\.)'

    # Substitute the matched pattern with the pattern followed by a new line
        newRecipe = re.sub(pattern, r'<br>\1', newRecipe)

        
        result = {'status' : 'success', 'newRecipe' : newRecipe}

    else:
        result = {'status': 'error', 'status-code': response.status_code}

    return jsonify(result)

@app.route('/reset_session')
def reset_session():
    session.clear()  # Clear all variables stored in the session
    return redirect(url_for('index'))  # Redirect to the homepage


if __name__ == '__main__':
    app.run(debug=True)