from flask import Flask, render_template, request, jsonify
from response import getResponse
import requests
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

def bot_api_calling(name, rating, feedback, response, category):
    # Make API call here
    '''
    Onestars ="★"
    Twostars ="★★"
    Threestars ="★★★"
    Fourstars ="★★★★"
    Fivestars ="★★★★★"
    '''
    starsOnRating = ""
    if (rating == 1):
        starsOnRating = "*"
    elif(rating == 2):
        starsOnRating = "**"
    elif(rating == 3):
        starsOnRating = "***"
    elif(rating == 4):
        starsOnRating = "****"
    elif(rating == 5):
        starsOnRating = "*****"
    api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={starsOnRating} {category} [UserName: {name} Comment:{feedback} Response: {response}]"
    #api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={starsOnRating}"
    response = requests.get(api_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    try:
        data = request.get_json()
        name = data['name']
        rating = data['rating']
        feedback = data['comment']

        # Call your Python script function
        response,category = getResponse(name, rating, feedback)
        bot_api_calling(name, rating, feedback, response, category)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
