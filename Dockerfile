FROM python:3

MAINTAINER Bryce Handerson

COPY . /src

RUN pip install /src

EXPOSE 8080

WORKDIR /src

ENTRYPOINT ["python", "/src/pbnh/run.py"]
