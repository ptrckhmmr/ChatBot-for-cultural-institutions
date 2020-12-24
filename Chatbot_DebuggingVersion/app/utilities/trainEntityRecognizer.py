"""
This modul contains the code to train the classifiers for all entities.
First, the parameters for the machine learning pipeline are set.
Second, the available mindmeld classifiers are trained using a grid search.
Third, only the best classifier is saved.
Forth, only the errors of the best classifier are written to a file.
"""

# importing necessary modules
from mindmeld.components import NaturalLanguageProcessor

# error tracking
from logErrors import logErrorsInCSV

# setting the correct path of the chat bot app
import os
import numpy as np
app_path = os.path.abspath((os.path.join(os.path.dirname(__file__), '..')))

# configuring logging
import logging
import mindmeld as mm
logging.getLogger('mindmeld').setLevel(logging.INFO)
mm.configure_logs()

# setting up NLU
nlp = NaturalLanguageProcessor(app_path)

# setting parameters for training
feature_dict = {
    'bag-of-words': {'lengths': [1, 2]},
    'edge-ngrams': {'lengths': [1, 2]}
}

# setting hyperparamter settings for maximum entropy markov model
search_grid_memm = {
    'penalty': ['l1', 'l2'],
    'C': [0.01, 1, 100, 10000]
}

hyperparam_settings_memm = {
  'type': 'k-fold',
  'k': 10,
  'grid': search_grid_memm
}

# setting hyperparamter settings for crf (conditional random field)
search_grid_crf = {
    'algorithm': ['lbfgs', 'l2sgd', 'ap', 'pa', 'arow'],
    'all_possible_states': [True, False],
    'all_possible_transitions': [True, False]
}

hyperparam_settings_crf = {
    'type': 'k-fold',
    'k': 10,
    'grid': search_grid_crf
}

# no lstm because not enough train data (need min 1000)
# # setting hyperparamter settings for LSTM (Bi-Directional Long Short-Term Memory (LSTM) Network)
search_grid_lstm = {
    'padding_length': [20, 50, 100],
    'batch_size': [10, 20, 30, 40, 50],
    'learning_rate': [0.001, 0.005, 0.01, 0.05],
    'number_of_epochs': [10, 20, 30, 40, 50]
 }

numberintents = 0

for domain in nlp.domains:
    for intent in nlp.domains[domain].intents:

        numberintents = numberintents + 1

        print("Intent No: " + str(numberintents))
        print("Intent: " + str(intent))

        nlp.domains[domain].intents[intent].build()

        if nlp.domains[domain].intents[intent].entities != {}:

            print("Train classifiers.")
            # train memm (maximum entropy markov model)
            er_memm = nlp.domains[domain].intents[intent].entity_recognizer
            er_memm.fit(model_settings={'classifier_type': 'memm'},
                        param_selection = hyperparam_settings_memm)

            # features = feature_dict),

            print("Maximum Entropy Markov Model done.")

            # train crf (conditional rational field)
            er_crf = nlp.domains[domain].intents[intent].entity_recognizer
            er_crf.fit(model_settings={'classifier_type': 'crf'},
                        param_selection=hyperparam_settings_crf)

            # features=feature_dict,

            print("CRF done.")

            print("Evaluate classifiers.")

            # evaluate memm (maximum entropy markov model)
            eval_memm = er_memm.evaluate()
            stats_memm1 = eval_memm.get_stats()
            stats_memm2 = stats_memm1['stats_overall']
            accuracy_memm = stats_memm2['accuracy']

            # evaluate crf
            eval_crf = er_crf.evaluate()
            stats_crf1 = eval_crf.get_stats()
            stats_crf2 = stats_crf1['stats_overall']
            accuracy_crf = stats_crf2['accuracy']

            # nehme den besten nach Accuracy
            bestmodel = np.argmax([accuracy_memm, accuracy_crf])


            print("Accuracy MEMM = " + str(accuracy_memm) + ", Accuracy CRF = " + str(accuracy_crf))
            print("Indize des besten Modells (0 = MEMM, 1 = CRF): " + str(bestmodel))

            model = [er_memm, er_crf][bestmodel]

            # save model for later use
            path_classif = app_path + '/models/domain_' + domain + '_intent_' + intent + '_entity_recognizer.pkl'
            model.dump(path_classif)

            # evaluate classifier
            try:
                logErrorsInCSV(model, "error_domain_" + domain + "_intent_" + intent + "_entity_recognizer.csv")
            except:
                pass