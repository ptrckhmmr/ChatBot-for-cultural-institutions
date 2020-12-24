def loadClassif(nlp, app_path):

    nlp.build()

    # loading domain classifier
    dc = nlp.domain_classifier
    dc.load(app_path+"/models/domain_model.pkl")

    # loading intent classifier
    for domain in nlp.domains:

        clf = nlp.domains[domain].intent_classifier

        try:
            clf.load(app_path + "/models/domain_" + domain + "_intent_model.pkl")
        except:
            nlp.domains[domain].intent_classifier.fit()

    # loading entity recognizer
    for domain in nlp.domains:
        for intent in nlp.domains[domain].intents:

            nlp.domains[domain].intents[intent].build()

            if nlp.domains[domain].intents[intent].entities != {}:
                er = nlp.domains[domain].intents[intent].entity_recognizer
                er.load(app_path + '/models/domain_' + domain + '_intent_' + intent + '_entity_recognizer.pkl')
