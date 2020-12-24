#!/bin/bash

echo
echo "stopping all container"
docker stop $(docker ps -aq)
echo

echo
echo "deleting all container"
docker rm $(docker ps -aq)
echo

echo 
echo "removing all images"
docker rmi $(docker images -q)
echo

echo 
echo "starting chatbot"
docker-compose up
echo
