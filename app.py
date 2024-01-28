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
        return redirect(url_for('recipe'))

    return redirect(url_for('recipe'))  #Redirect after saving answers

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

        image_tag = soup.find('img', {'class': ['universal-image__image', 'img-placeholder']})
        if image_tag:
            image_url = image_tag['data-src']
            print(image_url)
        else:
            print("NO IMAGE URL FOUND")

        co = cohere.Client('8HpB7vvugn3gwd9Nh90fz2QyhPCYKElitOUgR7Rl')
        
        dietary_r = session.get('dietary')
        preferences_r = session.get('preferences')

        Premessage = "The user will request an alternative recipe for a meal. You will be given the INGREDIENTS and the DIRECTIONS. ALL CHANGES MADE TO THE INGREDIENTS MUST BE REFLECTED IN THE DIRECTIONS.\n"

        if('vegan' in dietary_r):
            Premessage += "THIS USER IS VEGAN, IT CANNOT INCLUDE ANY ANIMAL PRODUCTS AT ALL. IF AN INGREDIENT IS MADE FROM ANY ANIMAL PRODUCTS, SUBSTITUTE IT FOR A VEGAN FRIENDLY OPTION.\n"
        elif('vegetarian' in dietary_r):
            Premessage += "THIS USER IS VEGETERIAN, IT CANNOT INCLUDE ANY MEAT.  IF AN INGREDIENT CONTAINS MEAT, SUBSTITUTE IT FOR A VEGETARIAN FRIENDLY OPTION.\n"

        if('gluten free' in dietary_r):
            Premessage += "THIS USER IS GLUTEN FREE. INGREDIENTS MUST ALL BE ALTERNATIVES THAT DO NOT INCLUDE GLUTEN WHERE APPLICABLE. IF AN IGREDIENT CONTAINS GLUTEN IT IS REQUIRED TO BE SUBSTITUTED FOR A GLUTEN FREE ALTERNATIVE.\n"
        if('dairy free' in dietary_r):
            Premessage += "THIS USER IS DAIRY FREE. INGREDIENTS MUST ALL BE ALTERNATIVES THAT DO NOT INCLUDE DAIRY WHERE APPLICABLE. IF AN IGREDIENT CONTAINS DAIRY IT IS REQUIRED TO BE SUBSTITUTED FOR A DAIRY FREE ALTERNATIVE.\n"

        Premessage += "THE FORMAT OF YOUR RESPONSE MUST BE AS FOLLOWS:\nThe output should be Ingredients: followed by every ingredient that follows any dietary restrictions with measurements seperated from each other by a -. IT IS ABSOLUTLY IMPARITIVE THAT THE FORMAT IS CORRECT AND ALL USER DIETARY RESTRICIONS ARE FOLLOWED. The next output should be Steps: followed by all of the valid steps are listed seperated from each other by -. An example of this is: Ingredients: -1 cup rice -2 pounds tomato -Steps: -Step 1: cook rice -Step 2: Cook tomato -Step 3: Enjoy!.\n\nREMEMBER TO USE -STEP formatting.\n THINK ABOUT HOW THE INGREDIENTS NEED TO BE ADJUSTED FOR THE USER'S PREFERENCES AND MAKE ALL CHANGES. IT IS OF UTMOST IMPORTANCE THAT THE INGREDIENTS ARE TO THE USERS REQUEST AND THAT ALL FORMATTING IS AS EXACTLY AS STATED WITH ALL STEPS LISTED"
        
        response2 = co.chat(


        chat_history=[
                {"role": "USER", "message": Premessage},
    
    # delete{"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
        ],
  
        message = f"{ingredientsText}\n{directionsText}",

            connectors=[{"id": "web-search"}]
        )

        #THis is a string with the entire response
        newRecipe = response2.text

        pattern_I = r'(Ingredients:)'

        newRecipe = re.sub(pattern_I, r'<h2>\1</h2>', newRecipe)

        pattern_S = r'(Steps:)'

        #pattern_SS = r'(Step )'

        #newRecipe=re.sub(pattern_SS, r'(<br>\1)', newRecipe)

        newRecipe = re.sub(pattern_S, r'<br><h2>\1</h2>', newRecipe)

        pattern = r'(-|\b\d{1,2}\.)'

    # Substitute the matched pattern with the pattern followed by a new line
        newRecipe = re.sub(pattern, r'<br>\1', newRecipe)

        
        result = {'status' : 'success', 'newRecipe' : newRecipe, 'imageurl' : image_url}

    else:
        result = {'status': 'error', 'status-code': response.status_code}

    return jsonify(result)

@app.route('/reset_session')
def reset_session():
    session.clear()  # Clear all variables stored in the session
    return redirect(url_for('index'))  # Redirect to the homepage

@app.route('/get_session_data')
def get_session_data():
    dietary_r = session.get('dietary')
    preferences_r = session.get('preferences')
    return jsonify({'dietary': dietary_r, 'preferences' : preferences_r})


if __name__ == '__main__':
    app.run(debug=True)