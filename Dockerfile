FROM python:3

MAINTAINER Bryce Handerson

COPY . /src

RUN pip install /src

EXPOSE 5001

ENTRYPOINT ["python", "/src/pbnh/run.py"]
