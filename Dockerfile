FROM python:3.10.4-slim

LABEL Heyva Health <heyva.health@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install --upgrade pip && pip install -r requirement.txt

EXPOSE 8000

CMD [ "python", "./api/manage.py","runserver", "0.0.0.0:8000"]
