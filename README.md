# STAR

Řídící systém


						nejdriv .env!
cd project/ckan/contrib/docker/

CKAN_SITE_ID=mzp_ckan

CKAN_SITE_URL=https://t-star.env.cz

CKAN_PORT=5000

CKAN_MAX_UPLOAD_SIZE_MB=100

CKAN_SMTP_SERVER=mailhub.env.cz:25

CKAN_SMTP_STARTTLS=False

CKAN_SMTP_USER=

CKAN_SMTP_PASSWORD=

CKAN_SMTP_MAIL_FROM=root@env.cz

POSTGRES_PASSWORD=ckan

POSTGRES_PORT=5432

DATASTORE_READONLY_PASSWORD=datastore



docker-compose up -d redis db solr

docker-compose up -d ckan

docker exec ckan /usr/local/bin/ckan-paster --plugin=ckan datastore set-permissions -c /etc/ckan/production.ini | docker exec -i db psql -U ckan


docker-compose up -d datapusher harvester-fetch harvester-gather

docker-compose ps

docker-compose exec ckan bash

. /usr/lib/ckan/venv/bin/activate

cd /usr/lib/ckan/venv/src/ckan

paster sysadmin add datafiller -c /etc/ckan/production.ini

docker-compose up -d datapusher



#ladit:

docker-compose stop ckan

docker-compose rm -f ckan

docker-compose up -d ckan



ckanext-contact_us

ckanext-mapviews



#volání přes docker:

docker-compose exec ckan /usr/lib/ckan/venv/bin/paster --plugin=ckan user list -c /etc/ckan/production.ini

docker-compose exec ckan /usr/lib/ckan/venv/bin/paster --plugin=ckan plugin-info -c /etc/ckan/production.ini >plugins.txt

   -> a tady to právě vyklopí hlášku že tam je nějaká chyba v pluginech


      do production.ini přidat:

disqus.secret_key  = neRyfzRvowchXND2jk4R7s5RI0oOfJditJg4iVkhIPAnF9JA1pM6sjdXWugd3Iun

disqus.public_key  = 6304de17f01e446caa79d4f19333927d

disqus.name = t-star-env-cz

