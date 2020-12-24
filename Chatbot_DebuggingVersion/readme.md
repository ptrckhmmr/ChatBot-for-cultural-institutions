# Chatbot Debugging Version - Pycharm

This folder contains a chatbot version that can be modified with a development environment. The trained models and labelled training files have to be copied into the folder with the deployable chatbot version. The background is that an interface in the source code must be overwritten for platform-independent deployments with Docker.

## Getting Started

To start the chatbot, different packages are needed. Especially, the dependencies of the used framework 'MindMeld' have to be considered. For the sake of simplicity, these processes have been automated with a script. However, these scripts were only configured for Linux and MacOS users. Windows users, please refer to the [documentation](https://www.mindmeld.com/docs/userguide/getting_started.html) of `MindMeld` and adapt the steps in the script.

### Script Linux (Ubuntu)

The installation process under Linux is straightforward. The script can be called with the following command.
```
source createEnvironment_ubuntu.sh
```
The command creates a virtual environment that contains all the required packages. Besides, Docker creates an interface to Elastic-Search, which is used for database queries. Then a mindmeld template is created into which the previous files are copied. 

If the environment has already been created, it is sufficient to restart the environment with the following command:

```
source initRequirements.sh
``` 

### Script MacOS

The MindMeld environment for MacOS is created in the same way as described above. The following commands are required for this: 

```
source createEnvironment_mac_step1.sh
source createEnvironment_mac_step2.sh
```

### Calling in the development environment

Once the script has been executed, the virtual environment interpreter can be executed in the development environment.

## Folder structure

The ``webapp`` folder contains the web interface for the chatbot. The most important file in this directory is the `flask_app.py`. In this, a Flask-App is created, which accesses the HTML-files in the folder `templates` and the stylistic elements in the directory `static`. Additionally, the Python files `loadClassifier.py` and `logging_config.py` provide auxiliary functions for the Flask application.

The chatbot with its models can be found under the folder `app`. The subfolders come from a structure given by `MindMeld`, which can be found in the native [documentation](https://www.mindmeld.com/docs/userguide/getting_started.html). The only exception to this is the `utilities` folder, in which help functions are defined.

## Deployment

After adding new intents or changes in the code, all changes must be transferred to the already deployed model. All you have to do is exchange the corresponding folders or files.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3ODU5OTY5NDldfQ===
-->
