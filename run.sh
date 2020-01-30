#!/bin/bash
echo "Stopping any running services ..."
docker-compose down
echo "Starting services ..."
docker-compose up --build -d
echo "Done !"
docker ps