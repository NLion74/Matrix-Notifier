FROM debian

RUN apt-get update && apt-get install -y python3 python3-pip libolm-dev

WORKDIR /app

COPY ./ ./

RUN pip3 install --user --no-cache-dir -r ./requirements.txt

ENV docker yes

ENV PORT 5505

ENV bot_user ""
ENV bot_pass ""
ENV home_server ""
ENV device_name "matrix-nio"

ENV authorization false
ENV auth_secret ""

CMD [ "python3", "main.py" ]