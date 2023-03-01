FROM python:3.10.4

LABEL Heyva Health <heyva.health@gmail.com>

ENV PYTHONUNBUFFERED 1


RUN mkdir /app
WORKDIR /app

COPY requirement.txt /app/
RUN pip install --upgrade pip && pip install -r requirement.txt

COPY . /app
RUN ls -alh /app

EXPOSE 8000

CMD [ "python", "./api/manage.py","runserver", "0.0.0.0:8000"]
