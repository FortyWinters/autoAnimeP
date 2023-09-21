FROM python:3.8

WORKDIR /autoAnime

COPY . /autoAnime

RUN pip install -r requirements.txt

CMD ["python", "app.py"]