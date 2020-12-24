"""
This module contains a sample query from the knowledge base to play around with the outputs
"""

from mindmeld.components import QuestionAnswerer

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))

qa = QuestionAnswerer(app_path)

qa.load_kb('app','exhibition',app_path+'/data/exhibition.json')

exhibtion = qa.get(index='exhibition',titel_de = "mapping")

print(exhibtion)

for i in exhibtion:
    print(i["titel_de"])