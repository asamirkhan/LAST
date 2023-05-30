FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./req.txt .
RUN pip install -r req.txt

WORKDIR /data


COPY . /data

RUN chmod +x start.sh
