#!/bin/bash
docker-compose down
#time docker container prune -f
#time docker image prune -f
#time docker network prune -f
time docker volume prune -f
time docker-compose build --no-cache
docker-compose up -d ckan
sleep 1m
docker exec -it db sh /docker-entrypoint-initdb.d/00_create_datastore.sh
docker exec ckan /usr/local/bin/ckan-paster --plugin=ckan datastore set-permissions -c /etc/ckan/production.ini | docker exec -i db psql -U ckan
docker exec -it db psql -U ckan -f 20_postgis_permissions.sql
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-spatial spatial initdb -c /etc/ckan/production.ini
docker-compose restart ckan
docker-compose logs ckan
docker-compose up -d harvester-gather
docker-compose up -d harvester-fetch
