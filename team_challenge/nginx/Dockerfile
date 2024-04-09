FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY ./staticfiles /team_challenge/staticfiles
COPY ./default.conf /etc/nginx/conf.d/default.conf