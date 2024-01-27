from flask import Flask, render_template, jsonify, redirect, url_for, request, session, redirect
from io import BytesIO
import subprocess
import cohere

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
        


if __name__ == '__main__':
    app.run(debug=True)