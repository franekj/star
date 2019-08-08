#!/bin/sh
set -e

# URL for the primary database, in the format expected by sqlalchemy (required
# unless linked to a container called 'db')
: ${CKAN_SQLALCHEMY_URL:=}
# URL for solr (required unless linked to a container called 'solr')
: ${CKAN_SOLR_URL:=}
# URL for redis (required unless linked to a container called 'redis')
: ${CKAN_REDIS_URL:=}
# URL for datapusher (required unless linked to a container called 'datapusher')
: ${CKAN_DATAPUSHER_URL:=}

CONFIG="${CKAN_CONFIG}/production.ini"

abort () {
  echo "$@" >&2
  exit 1
}

set_environment () {
  export CKAN_SITE_ID=${CKAN_SITE_ID}
  export CKAN_SITE_URL=${CKAN_SITE_URL}
  export CKAN_SQLALCHEMY_URL=${CKAN_SQLALCHEMY_URL}
  export CKAN_SOLR_URL=${CKAN_SOLR_URL}
  export CKAN_REDIS_URL=${CKAN_REDIS_URL}
  export CKAN_STORAGE_PATH=/var/lib/ckan
  export CKAN_DATAPUSHER_URL=${CKAN_DATAPUSHER_URL}
  export CKAN_DATASTORE_WRITE_URL=${CKAN_DATASTORE_WRITE_URL}
  export CKAN_DATASTORE_READ_URL=${CKAN_DATASTORE_READ_URL}
  export CKAN_SMTP_SERVER=${CKAN_SMTP_SERVER}
  export CKAN_SMTP_STARTTLS=${CKAN_SMTP_STARTTLS}
  export CKAN_SMTP_USER=${CKAN_SMTP_USER}
  export CKAN_SMTP_PASSWORD=${CKAN_SMTP_PASSWORD}
  export CKAN_SMTP_MAIL_FROM=${CKAN_SMTP_MAIL_FROM}
  export CKAN_MAX_UPLOAD_SIZE_MB=${CKAN_MAX_UPLOAD_SIZE_MB}
  export CKAN_LOCALE_DEFAULT=${CKAN_LOCALE_DEFAULT}
  export CKAN_LOCALE_ORDER=${CKAN_LOCALE_ORDER}
  export CKAN_SITE_INTRO_TEXT=${CKAN_SITE_INTRO_TEXT}
}

write_config () {
  ckan-paster make-config --no-interactive ckan "$CONFIG"
}

# Wait for PostgreSQL
while ! pg_isready -h db -U postgres; do
  sleep 1;
done

# If we don't already have a config file, bootstrap
if [ ! -e "$CONFIG" ]; then
  echo "!!! writing config file !!!!"
  write_config
  echo "!!! set env !!!!"
  set_environment
  echo "!!! db init !!!!"
  ckan-paster --plugin=ckan db init -c "${CKAN_CONFIG}/production.ini"

  echo "!!! creating user systemuser !!!!"
  ckan-paster --plugin=ckan user add systemuser email=jiri@hrad.ec password=Heslo123 apikey="58d94d5c-7766-4f1b-bc7a-b3034ecf5942" -c "${CKAN_CONFIG}/production.ini"  
  echo "!!! adding rights to systemuser !!!!"
  ckan-paster --plugin=ckan sysadmin add systemuser -c "${CKAN_CONFIG}/production.ini" 
#  echo "!!! adding permissiong for datastore !!!!"
#  ckan-paster --plugin=ckan datastore set-permissions -c /etc/ckan/production.ini | ckan-paster --plugin=ckan -i db psql -U ckan
fi

# Get or create CKAN_SQLALCHEMY_URL
if [ -z "$CKAN_SQLALCHEMY_URL" ]; then
  abort "ERROR: no CKAN_SQLALCHEMY_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_SOLR_URL" ]; then
    abort "ERROR: no CKAN_SOLR_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_REDIS_URL" ]; then
    abort "ERROR: no CKAN_REDIS_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_DATAPUSHER_URL" ]; then
    abort "ERROR: no CKAN_DATAPUSHER_URL specified in docker-compose.yml"
fi

set_environment
ckan-paster --plugin=ckan db init -c "${CKAN_CONFIG}/production.ini"
exec "$@"
