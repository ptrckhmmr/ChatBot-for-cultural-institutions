#!/bin/sh

# navigate to virtual environment
cd virtualEnv

# activate it
source bin/activate

# start mindmeld
mindmeld num-parse --start

# go back to origin
cd ..

## start elastic manually
# check if mac first
if [[ "$OSTYPE" == "darwin"* ]]; then

	echo "I am a MAC computer"

	curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.0.tar.gz -o elasticsearch-6.7.0.tar.gz
	tar -zxvf elasticsearch-6.7.0.tar.gz
	cd elasticsearch-6.7.0/bin
	./elasticsearch

else 
	echo "I am not a MAC computer"
	sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:6.7.0
	sudo docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.7.0

fi


