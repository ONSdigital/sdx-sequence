FROM onsdigital/flask-crypto

ADD server.py /app/server.py
ADD settings.py /app/settings.py
ADD requirements.txt /app/requirements.txt
ADD startup.sh /app/startup.sh

RUN mkdir -p /app/logs

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -yq git gcc make build-essential python3-dev python3-reportlab
RUN git clone https://github.com/ONSdigital/sdx-common.git
RUN pip3 install ./sdx-common
RUN pip3 install --no-cache-dir -r /app/requirements.txt


ENTRYPOINT ./startup.sh
