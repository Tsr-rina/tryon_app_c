FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y git \
    && apt-get install -y python-is-python3 \
    && apt-get install -y python3-pip \
    && apt-get install -y sudo \
    && apt-get install -y make \
    && apt-get install -y file \
    && apt-get install -y uvicorn

WORKDIR /app
ADD ./src/ /app/

COPY requirements.txt /app/

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8080"]
