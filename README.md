# OpenChat
A dockerized web based chat application, built with Python, Flask, SocketIO, and uWSGI. Created by Joshua Schlichting.


## How to build and initially run the container
1. Clone this git repository and cd into it.
2. Execute `docker build -t <image name> .`
3. Execute `docker run --name <container name> -p 8000:8000 <image name>`, and feel free to use whichever port you desire on the host machine. Port `8000` for inside the container must remain the same.

## How to stop
Execute `docker stop <container name>`

## How to start (after initially building it)
Execute `docker start <container name>`

## License
MIT License

## Acknowledgments
  * Flask (http://flask.pocoo.org/)
  * SocketIO (https://socket.io/)
  * Flask-SocketIO (https://flask-socketio.readthedocs.io/en/latest/)
  * uWSGI (https://uwsgi-docs.readthedocs.io/en/latest/)
  * Docker (https://docker.com)
  
