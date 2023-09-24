FROM python:3.8

WORKDIR /autoAnime

ADD src /autoAnime/src

ADD config_file /autoAnime/config_file

VOLUME log /autoAnime/log

COPY requirements.txt /autoAnime/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "src/app/app.py"]