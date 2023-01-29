FROM debian

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install matrix-nio requests

WORKDIR /app

COPY ./ ./

ENV docker yes

ENV port 5505

ENV host server

ENV botuser ""

ENV botpass ""

ENV homeserver ""

ENV roomid ""

CMD [ "python3", "main.py" ]