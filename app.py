from flask import Flask, render_template
from emails_response import check_email
import threading
import time

app = Flask(__name__)

loading_messages = []

def email_checker():
    global loading_messages
    
    loading_messages.append(f" Loading...")
    check_email()  # Perform email checking here
    time.sleep(10)  # Check email every 2 minutes
        

@app.route('/')
def index():
    loading_messages.append(f"Loading...")
    print("Loading ... ")
    check_email()
    return render_template('index.html', loading_messages=loading_messages)

if __name__ == "__main__":
    # Start a separate thread for email checking
    #email_thread = threading.Thread(target=email_checker)
    #email_thread.daemon = True
    #email_thread.start()
    app.run(debug=True)
