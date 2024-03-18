import pickle
import random
from dictionary import negativeWordsInRoman, apologiseComments, happyComments, greetingsList, highRating, lowRating, helpline
from dictionary import helplineFeedback, negativeSuggestionFeedback, positiveSuggestionFeedback
import requests


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
  
  
  

  if(predictedRating == 1.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = random.choice(apologiseComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = random.choice(highRating)
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
      response = random.choice(highRating)
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
      response = random.choice(highRating)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

  elif(predictedRating == 4.0):
    if(rating == 1 or rating == 2 or rating == 3):
      response = random.choice(lowRating)
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
      response = random.choice(lowRating)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse
    elif(rating == 4 or rating == 5):
      response = random.choice(happyComments)
      greetings = random.choice(greetingsList)
      finalResponse = greetings + " " + name + " , " +  response
      return finalResponse

def preprocessComment(comment):
    #print("PREPROCESS", comment)
    comment = comment.lower()

    for word in helpline:
      #print(word)
      if word in comment:
          #comment = comment.replace(word, "bakwas")
          comment = "helpline number"
          return comment
    #print("PREPROCESS 2", comment)
    for word in negativeWordsInRoman:
      #print(word)
      if word in comment:
          #comment = comment.replace(word, "bakwas")
          comment = "bakwas"
          return comment
    #print("PREPROCESS 3", comment)

    return comment


def getResponse(name, rating, comment):
    model, vectorizer = getModelandVector()
    processedComment = preprocessComment(comment)

    print(processedComment)

    if(len(comment) > 90):
        if(rating == 1 or rating == 2 or rating ==3):
            response = negativeSuggestionFeedback
            greetings = random.choice(greetingsList)
            finalResponse = greetings + " " + name + " , " +  response
            return finalResponse, "Complaints"
        
        elif(rating == 4 or rating == 5):
            response = positiveSuggestionFeedback
            greetings = random.choice(greetingsList)
            finalResponse = greetings + " " + name + " , " +  response
            return finalResponse, "Suggestion"

    elif(processedComment == "helpline number"):
        response = helplineFeedback
        greetings = random.choice(greetingsList)
        finalResponse = greetings + " " + name + " , " +  response
        return finalResponse, "Help"
    
    
    else:
        category = ""
        if(processedComment == "bakwas"):
           category="Negative Comment"
        else:
           category="Positive Comment"
        new_query = [processedComment]
        new_query_tfidf = vectorizer.transform(new_query)
        predicted_star_rating = model.predict(new_query_tfidf)
        predictedRating = float(predicted_star_rating[0])
        finalResponse = generateResponse(name, rating, processedComment, predictedRating)
        return finalResponse, category
      


#print(preprocessComment("app is not good"))
