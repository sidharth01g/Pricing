FROM ubuntu:16.04


RUN apt-get update -y\
  && apt-get install -y python3-pip python3-dev \
  && apt-get install -y ssh curl \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./pricing/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 4776

ENTRYPOINT [ "python3" ]

CMD [ "pricing/src/app.py" ]