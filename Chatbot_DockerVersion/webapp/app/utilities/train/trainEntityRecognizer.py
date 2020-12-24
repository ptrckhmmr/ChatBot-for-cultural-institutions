# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor

# error tracking
from logErrors import logErrorsInCSV

# setting the correct path of the chat bot app
import os
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))
app_path = os.path.abspath((os.path.join(app_path, '..')))

# configuring logging
import logging
import mindmeld as mm
logging.getLogger('mindmeld').setLevel(logging.INFO)
mm.configure_logs()

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

for domain in nlp.domains:
    for intent in nlp.domains[domain].intents:

        nlp.domains[domain].intents[intent].build()

        if nlp.domains[domain].intents[intent].entities != {}:
            er = nlp.domains[domain].intents[intent].entity_recognizer
            er.fit()

            # save model for later use
            er.dump(model_path=app_path + '/models/domain_' + domain + '_intent_' + intent + '_entity_recognizer.pkl')

            # evaluate classifier
            try:
                logErrorsInCSV(er, "error_domain_" + domain + "_intent_" + intent + "_entity_recognizer.csv")
            except:
                pass