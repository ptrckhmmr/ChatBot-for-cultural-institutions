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
nlp.build()

# train domain classifier
dc = nlp.domain_classifier
dc.fit()

# nehme den besten nach Accuracy

# saving model for later use
path_classif = app_path+"/models/domain_model.pkl"
dc.dump(path_classif)

# evaluate classifier
logErrorsInCSV(dc,"error_domainClassif.csv")