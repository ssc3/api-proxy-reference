FROM ubuntu:16.04
COPY ./service /home/service
COPY ./images /home/images
COPY ./conf /home/conf


RUN apt update && \
	apt install -y python3 && \
	apt install -y python3-pip && \
	apt install -y net-tools

RUN pip3 install -r /home/images/requirements.txt

# Expose host port
EXPOSE 8001

WORKDIR /home/service
#CMD ["python3", "server.py"]
# USE THIS IF WANT TO RESTRICT RESPONSES ROIGINATING IN LOCAL HOST CMD gunicorn --reload -b 127.0.0.1:8001 -w 9 -t 300 -k gevent server:app
# CMD gunicorn --reload -b 0.0.0.0:8001 -w 4 -t 300 -k gevent server:app
CMD gunicorn -b 0.0.0.0:8001 -w 4 -t 300 --forwarded-allow-ips=* --access-logfile /tmp/gunicorn.access.log --error-logfile /tmp/gunicorn.error.log server:app