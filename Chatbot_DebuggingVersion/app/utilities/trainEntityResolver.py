"""
This modul contains the code to initialize all entity resolver.
They serve as a bridge between the knowledge base and MindMeld.
"""

# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))

# configuring logging
import logging
import mindmeld as mm
logging.getLogger('mindmeld').setLevel(logging.INFO)
mm.configure_logs()

print(app_path)

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

nlp.domains['zkm'].intents['exhibition_duration'].build()
er = nlp.domains['zkm'].intents['exhibition_duration'].entities['exhibition'].entity_resolver
er.fit()

from mindmeld.core import Entity
print(er.predict(Entity(text='Schloslichtspiel', entity_type='exhibition')))