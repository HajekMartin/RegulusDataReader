FROM python:3.8-slim

COPY . /usr/src/app

#RUN pip install -r /usr/src/app/requirements.txt

CMD ["python", "/usr/src/app/main.py"]
