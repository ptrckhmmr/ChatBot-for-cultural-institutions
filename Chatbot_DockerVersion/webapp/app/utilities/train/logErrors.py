# importing csv for error tracking
import csv

def logErrorsInCSV(classifier,filename):

    eval = classifier.evaluate()
    print(eval.get_stats()['stats_overall']['accuracy'])

    # writing incorrect results to .csv file
    out = csv.writer(open(filename,"w"), delimiter=';',quoting=csv.QUOTE_ALL)
    out.writerows(list(eval.incorrect_results()))