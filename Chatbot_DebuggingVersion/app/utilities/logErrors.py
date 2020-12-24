"""
This module contains a function which evaluates the classifier and logs the wrongly classified instances
"""

# importing csv for error tracking
import csv

def logErrorsInCSV(classifier,filename):
    """
    This function evaluates the classifier and logs the wrongly classified instances.

    Input:
        classifier: trained MindMeld classifier
        filename: name of file in which evaluation results should be stored in

    Returns:
        Nothing.
    """

    eval = classifier.evaluate()
    print(eval.get_stats()['stats_overall']['accuracy'])

    # writing incorrect results to .csv file
    out = csv.writer(open(filename,"w"), delimiter=';',quoting=csv.QUOTE_ALL)
    out.writerows(list(eval.incorrect_results()))