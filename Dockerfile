FROM python:3.9.13-bullseye

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt