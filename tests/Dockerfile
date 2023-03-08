FROM debian

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY ./ ./

RUN pip install --no-cache-dir -r requirements.txt

ENV docker yes

ENV auth_secret ""

CMD ["pytest", "."]
