FROM python:3.6.1

RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install requests

COPY . /spider
WORKDIR /spider

CMD ./spider_crawl.sh