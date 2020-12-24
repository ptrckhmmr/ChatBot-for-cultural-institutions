# Chatbot Deployment Version - Docker

This folder contains the chatbot version, which can be deployed using `Docker`. The trained models and labelled training files must be taken from the folder with the debugging version. The background is that for platform-independent deployments with `Docker` an interface in the source code of `MindMeld` must be overwritten.

## Getting Started

To deploy the chatbot, the only requirement is that `Docker` is installed. More information about installing this software can be found on the website of [Docker](https://www.docker.com/).

The following command is required to run the chatbot:

    docker-compose up

Afterwards, the chatbot can be called under the IP address of the server and the port 5000.

## Folder structure

The folder `webapp` contains all files needed for the chatbot. All trained models, including the labelled data, are located in the subfolder `app`. The overwritten source code of `MindMeld` is stored in the directory `requirements`. The folders `static` and `templates` are needed by the Python file `flask_app.py` to create the Flask app.  The remaining Python scripts are auxiliary scripts. 

## Recommendations

To be able to handle as many requests to the chatbot as possible, it is advisable to configure a web server with [NGINX](https://www.nginx.com/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTQyMzQ2MTkyMl19
-->