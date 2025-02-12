from flask import Flask, render_template, request, jsonify
from response import getResponse
import requests
from db import ReturnDatabaseObject
from data import getDataFromUserComplain, updateDataToUserComplain
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import logging
from urllib.parse import quote

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#from app import app


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

def bot_api_calling(name, rating, feedback, response, category, count):
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

    feedback = feedback.replace("&", "and")
    response = response.replace("&", "and")

    # Encode the text properly
    text = f"{starsOnRating} {category} [UserName: {name} Comment:{feedback} Response: {response}]"
    encoded_text = quote(text)

    # Construct API URL
    api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={encoded_text}&remaining={count}"

    # Send GET request (ignore SSL errors)
    response = requests.get(api_url, verify=False)

    #api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={starsOnRating} {category} [UserName: {name} Comment:{feedback} Response: {response}]&remaining={count}"

    #print(api_url)
    #api_url = f"https://epbot.blinkitech.com/api/file/saveusertext?bot=14&text={starsOnRating}"
    #response = requests.get(api_url)

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
        count = data['count']

        # Call your Python script function
        response,category = getResponse(name, rating, feedback)

        bot_api_calling(name, rating, feedback, response, category, count)
 
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/email') 
def email():
    guid = request.args.get('guid')
    mydb = ReturnDatabaseObject()
    # Retrieve data from the database based on the GUID
    print("*****************************************************")
    print(guid)
    df = getDataFromUserComplain(mydb, guid)
    print(df)

    # Check if the DataFrame is empty
    if not df.empty:
        # Extract the first row of the DataFrame
        print("*****************************************************")
        record = df.iloc[0]
        print("*****************************************************")
        print(record)

        # Extract values from the DataFrame
        id = record['id']
        userguid = record['userguid']
        emailmessage = record['emailmessage']
        messageresponse = record['messageresponse']
        identifiedNumber = record['identifiedNumber']
        identifiedIssue = record['identifiedIssue']
        identifiedAmount = record['identifiedAmount']
        identifiedTransactionId = record['identifiedTransactionId']
        identifiedTransactionTime = record['identifiedTransactionTime']
        commentBox = "Your Comment Here"

        # Render the template with the extracted values
        return render_template('email.html', 
                               id=id,
                               userguid=userguid,
                               emailmessage=emailmessage,
                               messageresponse=messageresponse,
                               identifiedNumber=identifiedNumber,
                               identifiedIssue=identifiedIssue,
                               identifiedAmount=identifiedAmount,
                               identifiedTransactionId=identifiedTransactionId,
                               identifiedTransactionTime=identifiedTransactionTime,
                               commentBox = commentBox
                               )
    else:
        # If no data is found for the given GUID, render the template without any data
        return render_template('email.html')

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    guid = data.get('guid')
    identifiedNumber = data.get('identifiedNumber')
    identifiedAmount = data.get('identifiedAmount')
    identifiedTransactionId = data.get('identifiedTransactionId')
    identifiedTransactionTime = data.get('identifiedTransactionTime')
    comment = data.get('commentBox')

    print("********************************************CHECK******************************")
    comment = str(comment)
    print(type(comment))
    print(comment)
    # Call the updateDataToUserComplain function
    updateDataToUserComplain(guid, identifiedNumber, identifiedAmount, identifiedTransactionId, identifiedTransactionTime,comment)

    # Return a response (you can customize the response as needed)
    return jsonify({"message": "Data updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
        
    

    
