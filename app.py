from flask import Flask, render_template, request, jsonify
from response import getResponse
import requests
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

def bot_api_calling(response):
    # Make API call here
    api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={response}"
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
        bot_api_calling(category)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
