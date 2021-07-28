FROM python:3.6

RUN pip install --upgrade pip
RUN pip install nltk

COPY . /pipeline
WORKDIR /pipeline

CMD python3 handler.py