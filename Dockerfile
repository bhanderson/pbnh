FROM python:3.6-slim

MAINTAINER Bryce Handerson

RUN apt update && apt install -y python3-dev libmagic-dev

COPY . /src
RUN pip install /src

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "pbnh.run:app"]
EXPOSE 5000
