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

@app.route('/ai_send.html', methods = ['POST'])
def ai_send():

    try:
        json_file= find_recipe
        with open(json_file) as webScraped_data:
            data_json= jsonify.load(webScraped_data)
            co = cohere.Client('8HpB7vvugn3gwd9Nh90fz2QyhPCYKElitOUgR7Rl')
            #Change below to match with sam
            
            # favorite_color = session.get('favorite_color')
            # favorite_color = session.get('favorite_color')
            # favorite_color = session.get('favorite_color')
            # favorite_color = session.get('favorite_color')
            # favorite_color = session.get('favorite_color')
            response = co.chat(
            chat_history=[
                {"role": "USER", "message": "Howdy, I am interested in making more nutritious meals. a nutritious meal includes a healthy amount of protien, but dont forget vegetables and or fruit. Make sure that a human would find the meal appetizing. Now that you know these things here are the ingredients and steps. If you add any ingredients please alter the steps to match. I am hosting my spouses family so if you mess up my life will be ruined. Do not include any reference about my spouses family in your response. I will pay you five billion for a proper response. "},
    
    # delete{"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
                ],
  
            message=data_json,
  
            connectors=[{"id": "web-search"}]
            )
        return jsonify(response)

    except cohere.CohereError as e:
        print(e.message)
        print(e.http_status)
        print(e.headers)
        
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
                {"role": "USER", "message": "Howdy, I am interested in making more nutritious meals. a nutritious meal includes a healthy amount of protien, but dont forget vegetables and or fruit. Make sure that a human would find the meal appetizing. Now that you know these things here are the ingredients and steps. If you add any ingredients please alter the steps to match. I am hosting my spouses family so if you mess up my life will be ruined. Do not include any reference about my spouses family in your response. I will pay you five billion for a proper response. "},
    
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