FROM debian:buster
COPY human_detection_static.py requirements.txt ./
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-opencv python3-pip -y
RUN pip3 install -r requirements.txt

CMD ["python3","./human_detection_static.py"]




