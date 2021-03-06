#!/bin/bash
docker-compose down
time docker container prune -f
time docker image prune -f
time docker network prune -f
time docker volume prune -f
time docker-compose build --no-cache
docker-compose up -d ckan
sleep 1m
echo "#### DB INIT ####"
docker exec -it db sh /docker-entrypoint-initdb.d/00_create_datastore.sh
docker exec ckan /usr/local/bin/ckan-paster --plugin=ckan datastore set-permissions -c /etc/ckan/production.ini | docker exec -i db psql -U ckan
docker exec -it db psql -U ckan -f docker-entrypoint-initdb.d/20_postgis_permissions.sql
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-spatial spatial initdb -c /etc/ckan/production.ini
# validation
#docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-validation validation init-db -c /etc/ckan/production.ini

echo "#### SYSADM INIT ####"
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan user add systemuser email=ckan@mzp.cz password=Heslo123 apikey="50bfeb5d-ac92-4b76-ad1a-393b3c65ad0c" -c /etc/ckan/production.ini
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin add systemuser -c /etc/ckan/production.in

echo "#### HARVESTING INIT ####"
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan user add harvest email=ckan@mzp.cz password=Heslo123 -c /etc/ckan/production.ini
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckan sysadmin add harvest -c /etc/ckan/production.ini
docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-harvest harvester initdb -c /etc/ckan/production.ini

echo "#### HARVESTING HANDLERS ####"
nohup docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-harvest harvester gather_consumer -c /etc/ckan/production.ini &
nohup docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-harvest harvester fetch_consumer -c /etc/ckan/production.ini &

docker exec -it ckan /usr/local/bin/ckan-paster --plugin=ckanext-harvest harvester run -c /etc/ckan/production.ini
docker-compose --file docker-compose.elk_dev.yml down 
docker-compose --file docker-compose.elk_dev.yml up --detach ckan
docker-compose --file docker-compose.elk_dev.yml logs --follow ckan
