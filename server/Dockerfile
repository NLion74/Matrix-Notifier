FROM debian

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY ./ ./

RUN pip3 install --user --no-cache-dir -r requirements.txt

ENV docker yes

ENV PORT 5505

ENV authorization false
ENV auth_secret ""

EXPOSE 5505

CMD [ "python3", "app.py" ]