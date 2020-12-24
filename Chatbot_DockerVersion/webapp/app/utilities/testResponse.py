# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components import QuestionAnswerer
from loadClassifier import loadClassif

from fuzzywuzzy import process
import pandas as pd

# import logging
from mindmeld import configure_logs; configure_logs()

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

# loading all previously trained classifiers
loadClassif(nlp,app_path)

input = 'Seit wann gibt es das ZKM?'

print(nlp.process(input))
#id = nlp.process(input)['entities'][0]['value'][0]['id']

#data = pd.read_csv(app_path + '/data/all_possible_questions.txt',header=None, sep='\n')

#print(process.extractOne(input, data[0]))

# setting up knowledge base for query
qa = QuestionAnswerer(app_path)
#qa.load_kb('app','general_information',app_path+'/data/general_information.json')

#information = qa.get(index='general_information',id = id)

#print(exhibtion)

#title = exhibtion[0]['titel_de']
#start = exhibtion[0]['start_tag']
#end = exhibtion[0]['ende_tag']

#verknuepfungEvents = exhibtion[0]['verknuepfung_events']

#day = openinghours[0]['tag']
#start = openinghours[0]['start']
#end = openinghours[0]['ende']

#print('Am ' + day + ' öffnet das ZKM um' + start + ' und schließt um ' + end + '.')

beschreibung = 'Das ZKM wurde 1989 von der Stadt Karlsruhe und dem Land Baden-Würtemberg gegründet. Gründungsdirektor Heinrich Klotz formte die Mission des ZKMs, die klassischen Künste ins digitale Zeitalter fortzuschreiben. Die einzigartige Kulturinstitution ist seit 1997 in einem ehemaligen, denkmalgeschützten Industriebau, dem sogenannten Hallenbau A untergebracht, der zu seiner Entstehungszeit einer der architektonisch fortschrittlichsten in Deutschland war. Hier findest du weitere Infos dazu: https://zkm.de/de/das-zkm '

print(beschreibung)




