# Utilities: How to use the help files

# Create training and test files

Consider questions and mark with keyword (e.g. EXHIBITION, ZEIT, etc.) and save as .txt file (UTF 8). 

Sample question: 
``How old is ARTIST?``?

The latter is converted into an entity label in the jupyter notebook Fragen_mit_Entities/Erstellen_Fragen_Entities.ipynb using regular expression and an entity list (insert the path to .txt file in notebook script).

Example output after script: 
`How old is (Claude Monet|artist)?`

Then the resulting train.txt and test.txt must be placed in the appropriate subdirectory. If necessary, a new domain and intent must be created according to the MindMeld structure.

# Creating the Knowledge Base

The notebook Umwandling_in_JSON/Creation_KnowledgeBase_Gazetteer.ipynb  can be used to create a Knowledge Base. The resulting files must be stored in the directory specified in the notebook.

A data record on which the Knowledge Base is based is required for this.

# Create a Gazetteer

To create a Gazetteer, you can use the notebook Umwandling_in_JSON/Creation_KnowledgeBase_Gazetteer.ipynb. The resulting files must be stored in the directory specified in the notebook.

A data set with entities on which the Gazetteers is based is required for this.

# Create the Entity Mapping

The notebook Umwandling_in_JSON/EntityMappingEXHIBITION.ipynb can be used to create a Gazetteer. The resulting files must be stored in the directory specified in the notebook.