FROM python:3.8-slim

COPY . /usr/src/app

RUN bash -c 'pip instal....'

RUN pip install -r /usr/src/app/requirements.txt

RUN bash -c 'python3 script....'

CMD ["python", "/usr/src/app/main.py"]
