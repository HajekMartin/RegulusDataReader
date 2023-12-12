RUN bash -c 'echo -e Starting Dockerfile....' 

FROM python:3.8-slim

COPY . /usr/src/app

RUN bash -c 'echo -e pip instal....' 

RUN pip install -r /usr/src/app/requirements.txt

RUN bash -c 'echo -e python3 script....'

CMD ["python", "/usr/src/app/main.py"]
