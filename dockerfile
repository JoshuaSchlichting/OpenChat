FROM python:latest

RUN apt update && apt install apt-file -y && apt-file update
RUN apt-get install build-essential

RUN python -m pip install --upgrade pip
RUN pip install Flask uwsgi flask-socketio gevent


#WORKDIR /home/Downloads
#RUN wget https://github.com/socketio/socket.io-client/archive/2.2.0.tar.gz
#RUN tar -xvzf socket.io-client-2.2.0.tar.gz
#RUN cd socket.io-client-2.2.0
#RUN mkdir /static
#RUN cp socket.io-client-2.2.0/dist/socket.io.slim.js /static/socket.io.slim.js
WORKDIR /app
ADD . .
EXPOSE 5000 8000


CMD ["uwsgi", "--ini", "/app/uwsgi.ini", "--http-websockets"]



