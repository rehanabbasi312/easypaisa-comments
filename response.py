import pickle
import random


def getModelandVector():
    model_path = "model.pkl"
    vectorizer_path = "vectorizer.pkl"

    model = ""
    vectorizer = ""

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    with open(vectorizer_path, "rb") as file:
        vectorizer = pickle.load(file)

    return model, vectorizer

def generateResponse(name, rating, comment, predictedRating):
  
  greetingsList = ["Hey", "Dear","Hello"]
  highRating = "Thank you for providing us with a high rating. We apologize for any inconvenience and strive to make your experience smoother. 💚 Please share the details of your issue with us through our inbox, and our team will promptly address and resolve it for you. https://www.facebook.com/easypaisa/ 😊"
  lowRating = "We're delighted that you shared your positive experience. Please consider giving us a higher star rating. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚"
  apologiseComments = ["We are sorry for the inconvenience and would like to make your experience easy. 💚 Kindly share the details of your issue in our inbox and our team will resolve it for you quickly. https://www.facebook.com/easypaisa/ You can also contact us on Whatsapp: https://wa.me/923411103737?text=Hi Thank you for reaching out to us! 😊","We apologise for the inconvenience. Kindly let us know the details of your problem with screenshots in our inbox and our team will resolve it right away. www.facebook.com/easypaisa/ 💚 You can also contact us on Whatsapp: https://wa.me/923411103737?text=Hi", "We apologise for the inconvenience and would like to know about any issue you have faced to improve our services. We'd be grateful if you could kindly share details with us on our Whatsapp: wa.me/923411103737?text=Hi"]
  happyComments = ["We're so glad that you shared your positive experience here. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","We're so happy to have customers like you. Thank you for your appreciation. Keep using easypaisa! For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","We're always here for you. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","Thank you for your valuable feedback. Keep using easypaisa to make your life easy every day! 🤙 For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","Thank you for rating us the best. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","we are grateful for your support. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","Your appreciation means a lot to us. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","We're so glad to know about your positive experience. Keep using easypaisa to make your life easy every day! 🤙 For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","Feedbacks like yours keep us going! Thank you for acknowledging us. Keep using easypaisa. ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚","Your satisfaction is our utmost priority. We are glad to make your life easy. Keep using easypaisa! ✨ For any info & support, feel free to reach out to us on Whatsapp: https://wa.me/923411103737?text=Hi 💚"]

  if(predictedRating == 1.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = random.choice(apologiseComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = highRating
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

  elif(predictedRating == 2.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = random.choice(apologiseComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = highRating
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

  elif(predictedRating == 3.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = random.choice(apologiseComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = highRating
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

  elif(predictedRating == 4.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = lowRating
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = random.choice(happyComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

  elif(predictedRating == 5.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = lowRating
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = random.choice(happyComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse


def getResponse(name, rating, comment):
    model, vectorizer = getModelandVector()

    new_query = [comment]
    new_query_tfidf = vectorizer.transform(new_query)
    predicted_star_rating = model.predict(new_query_tfidf)

    predictedRating = float(predicted_star_rating[0])
    finalResponse = generateResponse(name, rating, comment, predictedRating)
    return finalResponse
