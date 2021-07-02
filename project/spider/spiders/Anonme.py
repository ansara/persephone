import logging
import os
import ssl
from urllib.parse import urljoin

import pymongo
import requests
import scrapy
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rp_spider.items import AnonmeItem, CommentItem

password = os.environ["IBM_CLOUD_PASSWORD"]


logging.basicConfig(filename="spiderlog.txt", level=logging.INFO)


class AnonmeSpider(scrapy.Spider):
    name = "anonme"

    # https://anonib.archivedyou.com/ --> much more and older content
    # http://banned.pics/can/index.html --> mirror of anonme, seems to be less recent

    start_urls = [
        "https://anonme.tv/can/catalog.html",
    ]

    def __init__(self):

        try:
            client = MongoClient(
                f"mongodb://admin:{password}@f443f26c-22db-4cfc-b0db-17d6de5f58ff-0.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-1.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-2.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860/ibmclouddb?authSource=admin&replicaSet=replset",
                ssl=True,
                ssl_ca_certs="/home/adam/trafficking_data_jam/rp_spider/286a39f3-e1b8-4381-a83b-08ca9153eae0",
                ssl_cert_reqs=ssl.CERT_NONE,
            )

            logging.info("Sucessfully connected to database within spider")
            self.db = client.ibmclouddb

        except ConnectionFailure:
            logging.info("Error connecting to database within spider")

    def parse(self, response):
        thread_init = response.xpath(
            "//div[@class='threads']//div[@class='thread grid-li grid-size-small']//@href"
        ).extract()
        threads = []

        # remove bad links
        for word in thread_init:
            if "res" in word and "#" not in word and "http" not in word:
                threads.append(word)

        # create list of tuples with each thread link, and number of comments in thread
        try:
            number_comments = response.xpath(
                "//div[@class='threads']//div[@class='thread grid-li grid-size-small']//div[@class='replies']/strong/text()"
            ).extract()
            for val in range(len(number_comments)):
                number_comments[val] = number_comments[val].split(" ")[1]

            print(len(threads), len(number_comments))
            threads = list(
                zip(threads, number_comments)
            )  # match number of comments with correct thread

        except Exception:
            logging.info(f"Error parsing mainpage. URL: {response.url}")

        for thread in threads:
            url = urljoin("https://anonme.tv", thread[0])

            collection_name = response.url.split("/")[3]

            # only process page if thread does not exist in database or comments need to be updated
            existing_thread = self.db[collection_name].find_one({"url": url})
            if (
                not existing_thread
                or "comments" not in existing_thread
                or len(existing_thread["comments"]) != int(thread[1])
            ):
                yield scrapy.Request(url, callback=self.parse_thread)

    def parse_thread(self, response):

        thread_item = AnonmeItem()

        thread_item["location"] = response.url.split("/")[3]
        thread_item["url"] = response.url

        print(response.url)

        try:

            thread_item["original_post_text"] = "\n".join(
                response.xpath(
                    "//div[@class='post op']/div[@class='body']/text()"
                ).extract()
            )
            thread_item["original_post_date"] = response.xpath(
                "//div[@class='post op']/p//label/time/@datetime"
            ).extract()[0]
            thread_item["original_post_id"] = response.xpath(
                "//div[@class='post op']//*[@class='post_no']/text()"
            ).extract()[1]

            if response.xpath(
                "//div[@class='post op']/*[@class='subject']/text()"
            ).extract():
                thread_item["subject"] = response.xpath(
                    "//div[@class='post op']/*[@class='subject']/text()"
                ).extract()[0]

            original_post_image = urljoin(
                "https://anonme.tv",
                response.xpath("//p[@class='fileinfo']/a/@href").extract_first(),
            )
            original_post_image_name = response.xpath(
                "//p[@class='fileinfo']/span[@class='unimportant']/span/text()"
            ).extract_first()

            req = requests.get(original_post_image)
            thread_item["original_post_image_info"] = {
                "image_title": original_post_image_name,
                "image_data": req.content,
            }

            req.close()

        except Exception:
            logging.info(f"Error parsing thread information. URL: {response.url}")

        thread_item["comments"] = []

        comments = response.xpath("//*[@class='post reply']")

        for comment in comments:

            comment_item = CommentItem()

            try:
                text = "\n".join(comment.xpath(".//*[@class='body']/text()").extract())
                date = comment.xpath("./p/label/time/@datetime").extract()[0]
                comment_id = comment.xpath(".//*[@class='post_anchor']/@id").extract()[
                    0
                ]
                comment_link = urljoin(response.url, "#" + comment_id)

                comment_item = {
                    "text": text,
                    "date": date,
                    "comment_id": comment_id,
                    "comment_link": comment_link,
                }

                # comments that this one replies to
                if comment.xpath(".//*[@class='body']/a/@onclick"):
                    reply_ids = comment.xpath(".//*[@class='body']/a/text()").extract()

                    for val in range(len(reply_ids)):
                        reply_ids[val] = reply_ids[val][2:]

                    comment_item["reply_ids"] = reply_ids

                # other comments that mention this one
                mentioned_by = comment.xpath(
                    ".//*[@class='mentioned unimportant']/a/text()"
                )
                if mentioned_by:
                    comment_item["mentioned_by"] = mentioned_by.split(" ")

            except Exception:
                logging.info(
                    f"Error extracting comment information. URL: {response.url}"
                )

            try:

                image_urls = comment.xpath(".//*[@class='fileinfo']/a/@href").extract()
                original_image_names = comment.xpath(
                    ".//p[@class='fileinfo']/span[@class='unimportant']/span/text()"
                ).extract()

                image_urls = [value for value in image_urls if value != " "]
                original_image_names = [
                    value for value in original_image_names if value != " "
                ]

                if len(image_urls) != len(original_image_names):
                    logging.info(f"Potential issues extracting images")

                image_urls_tuples = list(zip(image_urls, original_image_names))

                if len(image_urls_tuples) > 0:
                    comment_item["image_info"] = []

                # get list of image urls for comment and download them in base64 format
                for image_info in image_urls_tuples:
                    image_url = urljoin("https://anonme.tv", image_info[0])
                    req = requests.get(image_url)

                    if len(original_image_names) == len(image_urls):
                        comment_item["image_info"].append(
                            {"image_title": image_info[1], "image_data": req.content}
                        )

                    else:
                        comment_item["image_info"].append({"image_data": req.content})

            except Exception:
                logging.info(f"Error extracting images. URL: {response.url}")

            thread_item["comments"].append(comment_item)

        return thread_item
