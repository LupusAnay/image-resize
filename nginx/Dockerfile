FROM nginx:1.13-alpine
EXPOSE 80
RUN rm /etc/nginx/conf.d/default.conf
COPY app.conf /etc/nginx/conf.d
