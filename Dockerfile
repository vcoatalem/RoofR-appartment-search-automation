FROM python:3

WORKDIR /app

ADD requirements.txt /app

RUN pip install requests
RUN pip install -r requirements.txt

ADD . /app

CMD [ "python", "src/run_docker.py" ]