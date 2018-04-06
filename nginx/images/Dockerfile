FROM ubuntu:16.04
COPY ./service /home/service
COPY ./images /home/images
COPY ./conf /home/conf


RUN apt update && \
	apt install -y nginx && \
	apt install -y python3 && \
	apt install -y python3-pip && \
	apt install -y net-tools


RUN cp /home/conf/nginx.conf /etc/nginx/nginx.conf

RUN pip3 install -r /home/images/requirements.txt


# Expose host port
EXPOSE 80

WORKDIR /home/service

#CMD service nginx start  USE THIS IF YOU PUT daemon off; inside nginx.conf
CMD nginx -g "daemon off;"