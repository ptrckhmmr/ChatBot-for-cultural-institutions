#!/bin/sh

## clean start

rm -r virtualEnv
rm -r elasticsearch-6.7.0
rm elasticsearch-6.7.0.tar.gz

## install requirements

# 1) get configuration file for mindmeld
bash -c "$(curl -s  https://devcenter.mindmeld.com/scripts/mindmeld_init.sh)"

# 2) setting up workspace for virtual environment
mkdir virtualEnv
cd virtualEnv

# 3) activating virtual environment
virtualenv -p python3 .
source bin/activate

# 4) install mindmeld & start it
pip install mindmeld
mindmeld num-parse --start

# 5) install fuzzywuzzy for string comparison
pip install fuzzywuzzy
pip install python-Levenshtein

# go back to origin
cd ..

# start elastic search
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:6.7.0
sudo docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0

# rename old project folder if existent
mv app app2

# create MindMeld blueprint
mindmeld blueprint template app

# copy files from old project folder to new one
cp -R ./app2/* ./app/

# remove old project files
rm -r app2


