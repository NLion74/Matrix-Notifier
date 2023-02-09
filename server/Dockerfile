FROM debian

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install flask

WORKDIR /app

COPY ./ ./

ENV docker yes

ENV port 5505

ENV sqlimit 100

EXPOSE 5505

CMD [ "python3", "app.py" ]