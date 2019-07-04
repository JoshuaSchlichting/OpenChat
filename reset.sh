docker stop flasktest
docker rm flasktest
docker build -t flaskimage .
docker run --name flasktest -p 8000:8000 flaskimage
