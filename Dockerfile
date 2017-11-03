FROM onsdigital/flask-crypto

COPY server.py /app/server.py
COPY settings.py /app/settings.py
COPY requirements.txt /app/requirements.txt
COPY Makefile /app/Makefile
COPY startup.sh /app/startup.sh
COPY sequences.py /app/sequences.py

RUN mkdir -p /app/logs

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

RUN make build

ENTRYPOINT ./startup.sh
