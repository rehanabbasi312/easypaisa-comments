from flask import Flask, render_template, request
from response import getResponse


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/api', methods=['POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        rating = int(request.form['rating'])
        feedback = request.form['feedback']

        response = getResponse(name, rating, feedback)

        return render_template('index.html', name=name, rating=rating, feedback=feedback, response=response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

