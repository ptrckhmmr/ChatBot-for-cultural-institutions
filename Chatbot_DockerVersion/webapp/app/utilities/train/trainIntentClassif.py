# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor

# error tracking
from logErrors import logErrorsInCSV

# setting the correct path of the chat bot app
import os

from app.utilities.train.logErrors import logErrorsInCSV

app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))
app_path = os.path.abspath((os.path.join(app_path, '..')))

# configuring logging
import logging
import mindmeld as mm
logging.getLogger('mindmeld').setLevel(logging.INFO)
mm.configure_logs()

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

# setting parameters for training
feature_dict = {
    'bag-of-words': { 'lengths': [1, 2] },
    'edge-ngrams': { 'lengths': [1, 2] }
}

search_grid = {
  'C': [0.01, 1, 10, 100, 1000],
  'class_bias': [0, 0.3, 0.7, 1]
}

hyperparam_settings = {
  'type': 'k-fold',
  'k': 10,
  'grid': search_grid
}

for domain in nlp.domains:

    # training classifier for domain
    clf = nlp.domains[domain].intent_classifier
    clf.fit(model_settings={'classifier_type': 'logreg'},
            features=feature_dict,
            param_selection=hyperparam_settings)

    path_classif = app_path + "/models/domain_" + domain + "_intent_model.pkl"
    clf.dump(path_classif)

    # evaluate classifier
    try:
        logErrorsInCSV(clf, "error_domain_" + domain + "_intentClassif.csv")
    except:
        pass