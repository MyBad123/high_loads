FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
RUN python3 manage.py makemigrations
EXPOSE 8000