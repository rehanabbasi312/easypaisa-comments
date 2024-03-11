from flask import Flask, render_template, request, jsonify
from response import getResponse

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

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
        response = getResponse(name, rating, feedback)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
