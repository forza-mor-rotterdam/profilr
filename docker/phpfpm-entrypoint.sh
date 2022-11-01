#!/bin/bash

set -u

echo "Starting php-fpm container"
echo "ENV: $APP_ENV"

cd /srv/web
php bin/console cache:warmup
chmod -R ugo+rwx /srv/web/var/cache

touch /srv/web/var/log/prod.log
touch /srv/web/var/log/prod.deprecations.log
chmod ugo+rwx /srv/web/var/log/prod.log
chmod ugo+rwx /srv/web/var/log/prod.deprecations.log
tail -f /srv/web/var/log/prod.log &
tail -f /srv/web/var/log/prod.deprecations.log &

php-fpm8.1
