"""
This modul contains the code to train the classifiers for all domains.
First, the parameters for the machine learning pipeline are set.
Second, the available MindMeld classifiers are trained using a grid search.
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
nlp.build()

# setting parameters for training
feature_dict = {
    'bag-of-words': { 'lengths': [1, 2] },
    'edge-ngrams': { 'lengths': [1, 2] }
}

# setting hyperparamter settings for logistic regression
search_grid_logreg = {
  'C': [0.01, 1, 10, 100, 1000],
  'class_bias': [0, 0.3, 0.7, 1]
}

hyperparam_settings_logreg = {
  'type': 'k-fold',
  'k': 10,
  'grid': search_grid_logreg
}

# setting hyperparamter settings for svm
search_grid_svm = {
  'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
  'C': [0.01, 1, 10, 100, 1000],
  'gamma': [0.001, 0.0001]
}

hyperparam_settings_svm = {
  'type': 'k-fold',
  'k': 10,
  'grid': search_grid_svm
}

# setting hyperparamter settings for random forest
search_grid_rforest = {
  'criterion': ['gini', 'entropy'],
  'n_estimators': [10, 100, 1000], #warn herasugenommen
  'min_samples_split': [2, 3, 5]
}

hyperparam_settings_rforest= {
  'type': 'k-fold',
  'k': 10,
  'grid': search_grid_rforest
}

print("Train classifiers.")
# train logistic regression
clf_logreg = nlp.domain_classifier
clf_logreg.fit(model_settings={'classifier_type': 'logreg'},
               features=feature_dict,
               param_selection=hyperparam_settings_logreg)

print("Logistic Regression done.")

# train svm
clf_svm = nlp.domain_classifier
clf_svm.fit(model_settings={'classifier_type': 'svm'},
            features=feature_dict,
            param_selection=hyperparam_settings_svm)

print("SVM done.")

# train random forest
clf_rforest = nlp.domain_classifier
clf_rforest.fit(model_settings={'classifier_type': 'rforest'},
                features=feature_dict,
                param_selection=hyperparam_settings_rforest)

print("Random Forest done.")

# evaluating classifier performance

print("Evaluate classifiers.")

# evaluate logistic regression
eval_logreg = clf_logreg.evaluate()
stats_logreg1 = eval_logreg.get_stats()
stats_logreg2 = stats_logreg1['stats_overall']
accuracy_logreg = stats_logreg2['accuracy']
# print("Results for Logistic Regression:")
# print("get stats: " + str(stats_logreg1) + ", stats overall: " + str(stats_logreg2) + ", accuracy: " + str(accuracy_logreg))

# evaluate svm
eval_svm = clf_svm.evaluate()
stats_svm1 = eval_svm.get_stats()
stats_svm2 = stats_svm1['stats_overall']
accuracy_svm = stats_svm2['accuracy']
# print("Results for SVM:")
# print("get stats: " + str(stats_svm1) + ", stats overall: " + str(stats_svm2) + ", accuracy: " + str(accuracy_svm))

# evaluate random forest
eval_rforest = clf_rforest.evaluate()
stats_rforest1 = eval_rforest.get_stats()
stats_rforest2 = stats_rforest1['stats_overall']
accuracy_rforest = stats_rforest2['accuracy']
# print("Results for Random Forest:")
# print("get stats: " + str(stats_rforest1) + ", stats overall: " + str(stats_rforest2) + ", accuracy: " + str(accuracy_rforest))

# nehme den besten nach Accuracy
bestmodel = np.argmax([accuracy_logreg, accuracy_rforest, accuracy_svm])

print("Accuracy Logistic Regression = " + str(accuracy_logreg) + ", Accuracy Random Forest = " + str(
  accuracy_rforest) + ", Accuracy SVM = " + str(accuracy_svm))
print("Indize des besten Modells (0 = LogReg, 1 = RForest, 2 = SVM): " + str(bestmodel))

model = [clf_logreg, clf_rforest, clf_svm][bestmodel]

print("Dump Model.")
# saving model for later use
path_classif = app_path+"/models/domain_model.pkl"
model.dump(path_classif)

# evaluate classifier
print("Error CSV file")
logErrorsInCSV(model,"error_domainClassif.csv")



