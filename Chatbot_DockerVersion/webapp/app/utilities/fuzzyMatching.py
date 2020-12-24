# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor

# basic python library
import pandas as pd
import re

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))

# defining helper functions
def getEntities(data_all):

    data_replaced = [re.search('\|.*}', s) for s in data_all[0]]

    entities = list()

    for match in data_replaced:
        if match is not None:

            entities.append(match.group(0))
            entities = list(set(entities))

    # remove first and last character
    entities = [string[1:-1] for string in entities]

    return (entities)

def replacePlaceholder(sentence,placeholder,subsitute):
    return sentence.replace(placeholder,subsitute)

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

data_all = pd.DataFrame()

# loading entity recognizer
for domain in nlp.domains:

    for intent in nlp.domains[domain].intents:

        if intent == 'unsupported':
            continue

        if domain == 'basic':
            continue

        # retrieving train and test data for each intent
        root = app_path + "/domains/" + domain + "/" + intent + "/"
        data_train = pd.read_csv(root + "train.txt", header=None, sep='\n')
        data_test = pd.read_csv(root + "train.txt", header=None, sep='\n')

        # combine data
        data_combined = pd.concat([data_train, data_test], axis=0)

        # get entities from data
        entities = getEntities(data_combined)

        if entities:
            for entity in entities:

                placeholder = entity.upper()

                # replace entity pattern with placeholder
                data_combined = [re.sub('{.*\|' + entity +'}', placeholder, s) for s in data_combined[0]]

                data_entities = pd.read_csv(app_path + '/entities/' + entity + '/gazetteer.txt',header=None, sep='\n')

                # replace entity placeholder with data_entity
                data_combined = [replacePlaceholder(question,placeholder,data_entity)
                        for question in data_combined
                        for data_entity in data_entities[0]]
        else:
            data_combined = data_combined[0].unique().tolist()

        # get unique instances
        data_combined = pd.DataFrame(set(data_combined))

        data_all = pd.concat([data_all,data_combined], axis=0)
        data_all.drop(0,axis=0, inplace=True)

with open(app_path + '/data/all_possible_questions.txt', 'w') as f:
    for sentence in data_all[0].tolist():
        f.write('%s\n' % sentence)