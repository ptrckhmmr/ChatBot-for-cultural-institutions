## Instructions for extending the range of functions
### Creation of domains, intents and entities

 1. Generate and store training & test data according to the MindMeld syntax in the corresponding directory of the chatbot. Relevant help file:

    - `Utilities/Fragen_mit_Entities/Erstellen_Fragen_Entities.ipynb`

The resulting training and test data must be saved under "Chatbot_DebuggingVersion/app/domains/NameOfDomain/NameOfIntent/".

 2. If necessary, create a knowledge base, entity mapping and gazetteers and integrate them into the chatbot. Relevant help files:

    - `Utilities/Umwandlung_in_JSON/Creation_KnowledgeBase_Gazetteer.ipynb`
    - `Umwandlung_in_JSON/EntityMappingEXHIBITION.ipynb`

    The knowledge base must be stored under "Chatbot_DebuggingVersion/app/data/", the entity mappings and Gazetteers under "Chatbot_DebuggingVersion/app/entities/NameOfEntity/".

 3. Training the individual classifiers. Execute the train*.py files:
    - `Chatbot_DebuggingVersion/app/utilities/trainDomainClassif.py`
    - `Chatbot_DebuggingVersion/app/utilities/trainIntentClassif.py`
    - `Chatbot_DebuggingVersion/app/utilities/trainEntityRecognizer.py`

    The trained models are automatically added to the chatbot directory.

 4. Add the intent in __ init __.py according to the MindMeld syntax. Relevant file:
    - `Chatbot_DebuggingVersion/app/__init__.py`

 5. Execute and test the chatbot in your browser. Relevant file:

    - `Chatbot_DebuggingVersion/webapp/flask_app.py`
