# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation

# function for loading previously trained classifier
from app.utilities.loadClassifier import loadClassif

# loading predefined logger
from logging_config import Logger

# Define logfile for user input and chatbot output
logger = Logger("chat.log")

# configuring logging
import logging
import mindmeld as mm
logging.getLogger('mindmeld').setLevel(logging.INFO)
mm.configure_logs()

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))
app_path = app_path + "/app"

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)
loadClassif(nlp,app_path)

conv = Conversation(nlp=nlp, app_path=app_path)

#### flask app

from flask import Flask, jsonify, render_template, request

# initializing flask app
app = Flask(__name__)

# endpoint for processing the input values for chatbot
@app.route('/process_form')
def process_form():
    #### Input for chatbot
    input = request.args.get('input')

    #### Process input
    if not (input is None or input == ''):

        # predict output and intent of user input
        output = conv.say(input)[0]
        intent = nlp.process(input)["intent"]

        logger.log("Input: " + input + " Output: " + output)

        chat_protokoll = open("Chat_Protokoll.txt", "a")
        chat_protokoll.write(input + ";" + output + "\n")
        chat_protokoll.close()

    #### Return output and predicted intent
    return jsonify(output_chatbot=output, intent_prediction=intent)

# function for automatically corrected questions in intent unsupported
@app.route('/corrected_question')
def corrected_question():

    # get parameters of front end
    input = request.args.get('input')
    user_message = request.args.get('user_message')

    if not (input is None or input == ''):

        output = conv.say(input)[0]
        #intent = nlp.process(input)["intent"]

        logger.log("Input: " + input + " Output: " + output)

        # write corrected questions to file
        corrected_questions = open("corrected_questions.txt", "a")
        corrected_questions.write(user_message + " (Correct Question: " + input + ")" + "\n")
        corrected_questions.close()

        # Levenshtein report
        log_file = open("Levenshtein_Auswertung.txt", "a")
        log_file.write(user_message + ";" + input + ";true" + "\n")
        log_file.close()

    #### Return console answer and output
    return jsonify(answer="correctly adjusted question received", output_chatbot=output)

# function for false corrected questions in intent unsupported
@app.route('/false_corrected_question')
def false_corrected_question():

    # get parameters of front end
    input = request.args.get('input')
    user_message = request.args.get('user_message')

    if not (input is None or input == ''):

        # write false corrected questions to file
        false_corrected_questions = open("false_corrected_questions.txt", "a")
        false_corrected_questions.write(user_message + " (Incorrect Question: " + input + ")" + "\n")
        false_corrected_questions.close()

        # Levenshtein report
        log_file = open("Levenshtein_Auswertung.txt", "a")
        log_file.write(user_message + ";" + input + ";false" + "\n")
        log_file.close()

    #### Return console answer
    return jsonify(answer="false corrected question received")

# function to report false modelled intents
@app.route('/intent_learning_improve')
def intent_learning_improve():

    # get parameters of front end
    user_input = request.args.get('user_input')
    correct_label = request.args.get('correct_label')
    false_label = request.args.get('false_label')
    output_chatbot = request.args.get('output_chatbot')

    # file name contains intent labels
    fileName = correct_label + "_improve.txt"

    if not (user_input is None or user_input == ''):

        # write false modelled training data to intent file
        change_file = open(fileName, "a")
        change_file.write(user_input + "\n")
        change_file.close()

        # Marie function
        log_file = open("Marie_Auswertung.txt", "a")
        log_file.write(user_input + ";" + output_chatbot + ";" + false_label + ";false;" + correct_label + "\n")
        log_file.close()

    #### Return console answer
    return jsonify(answer="intent modelled false")

# function to report correctly modelled intents
@app.route('/intent_learning_alright')
def intent_learning_alright():

    # get parameters of front end
    user_input = request.args.get('user_input')
    correct_label = request.args.get('correct_label')
    output_chatbot = request.args.get('output_chatbot')

    # file name contains intent labels
    fileName = correct_label + "_alright.txt"

    if not (user_input is None or user_input == ''):

        # write correctly modelled training data to intent file
        change_file = open(fileName, "a")
        change_file.write(user_input + "\n")
        change_file.close()

        # Marie function
        log_file = open("Marie_Auswertung.txt", "a")
        log_file.write(user_input + ";" + output_chatbot + ";" + correct_label + ";true;" + correct_label + "\n")
        log_file.close()

    #### Return console answer
    return jsonify(answer="intent already correctly modelled")

# function to send 10 artists to the frontend
@app.route('/get_artists')
def get_artists():

    # get 10 artists of the database
    artists = conv.say('ZKM gerade Ausstellungen &+*bnbn??')[0]
    # store these in a list which is received from the frontend
    artists_list = []
    # search for the first comma
    index = artists.index(",")
    # add the first artist to the list
    artists_list.append(artists[1:index])
    # remove the artist from the string
    artists = artists[index + 1:]

    # loop to get the artists in the middle of the string
    for i in range(8):
        index = artists.index(",")
        artists_list.append(artists[1:index])
        artists = artists[index + 1:]

    # add the last artist to the list
    artists_list.append(artists[1:-1])

    return jsonify(artists=artists_list)

# function to send 10 current exhibitions to the frontend
@app.route('/get_exhibitions')
def get_exhibitions():

    # get 10 exhibitions of the database
    exhibitions = conv.say('ZKM gerade Ausstellungen &+*bnbn?')[0]
    print(exhibitions)
    # store these in a list which is received from the frontend
    exhibitions_list = []
    # search for the first comma
    index = exhibitions.index(",")
    # add the first exhibition to the list
    exhibitions_list.append(exhibitions[0:index])
    # remove the exhibition from the string
    exhibitions = exhibitions[index + 1:]

    # loop to get the exhibitions in the middle of the string
    while(exhibitions != " "):
        index = exhibitions.index(",")
        exhibitions_list.append(exhibitions[1:index])
        exhibitions = exhibitions[index + 1:]

    return jsonify(exhibitions=exhibitions_list)

# function to transform chatbot output related to artists in exhibitons in table
@app.route('/tabelle_umwandeln')
def tabelle_umwandeln():

    # get the message to be transformed
    nachricht = request.args.get('transformieren')
    # list to store the artists in
    nachricht_list = []

    # get name of the exhibition
    ab_ausstellung = nachricht[20:]
    index = ab_ausstellung.index("haben folgende Künstler mitgewirkt: ")
    ausstellung = ab_ausstellung[0:index - 1]

    # rest of the string containing the artists
    kuenstler = ab_ausstellung[index + 36:]

    # compute the number of commas as separator
    anzahl_komma = 0
    for zeichen in kuenstler:
        if zeichen == ",":
            anzahl_komma = anzahl_komma + 1


    # get index of comma
    komma = kuenstler.index(",")
    # append first artist
    nachricht_list.append(kuenstler[0:komma-1])
    # remove artist from string
    kuenstler = kuenstler[komma+2:]

    # repeat this procedure for all artists in the string
    for i in range(anzahl_komma-1):
        komma = kuenstler.index(",")
        nachricht_list.append(kuenstler[0:komma-1])
        kuenstler = kuenstler[komma+2:]

    # append the last artist
    nachricht_list.append(kuenstler)

    return jsonify(exhibition=ausstellung, liste=nachricht_list)


# Render HTML Datei
@app.route('/')
def render_static():
    return render_template('index.html')

# run web app for chatbot
app.run(debug = True, use_reloader = False, host = '0.0.0.0')