FROM node:18-bullseye AS node_step

WORKDIR /srv/web/
COPY . /srv/web/
RUN cd /srv/web \
 && npm install \
 && npm run build

FROM nginx:latest

COPY ./nginx/nginx-default.template /etc/nginx/conf.d/default.template
COPY ./nginx/nginx-nginx.conf /etc/nginx/nginx.conf

# Copy public directory from repository (contains index.php and other webroot files)
COPY ./public /srv/web/public
# Copy build result of node build step
COPY --from=node_step /srv/web/public/build /srv/web/public/build

CMD envsubst '$FASTCGI_PASS' < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
