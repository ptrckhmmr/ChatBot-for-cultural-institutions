#!/bin/sh

## clean start

rm -r virtualEnv
rm -r elasticsearch-6.7.0
rm elasticsearch-6.7.0.tar.gz


## install requirements

# 1) install java
brew cask install java

# 2) get configuration file for mindmeld
# bash -c "$(curl -s  https://devcenter.mindmeld.com/scripts/mindmeld_init.sh)"

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
sudo -H easy_install pip
sudo -H pip install --upgrade virtualenv

# 3) setting up workspace for virtual environment
mkdir virtualEnv
cd virtualEnv

# 4) activating virtual environment
virtualenv -p python3 .
source bin/activate

# install mindmeld & start it
pip install mindmeld
mindmeld num-parse --start

# install fuzzywuzzy for string comparison
pip install fuzzywuzzy
pip install python-Levenshtein

# go back to origin
cd ..

# start elastic manually
curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.0.tar.gz -o elasticsearch-6.7.0.tar.gz
tar -zxvf elasticsearch-6.7.0.tar.gz
cd Elasticsearch-6.7.0/bin
./elasticsearch &




