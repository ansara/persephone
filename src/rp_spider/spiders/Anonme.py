import logging
from urllib.parse import urljoin
import datetime
import pytz

import scrapy
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rp_spider.items import AnonmeItem, CommentItem

from mongodb.db import connect_db

logging.basicConfig(filename="spiderlog.txt", level=logging.ERROR)

"TODO: when updating an existing thread, make sure certain information is not overwritten"
class AnonmeSpider(scrapy.Spider):
    name = "anonme"

    start_urls = [
        "https://anonposted.com",
    ]

    def __init__(self):
        try:
            self.db = connect_db()
            logging.info("Sucessfully connected to database within spider")

        except ConnectionFailure as e:
            logging.error(f"Error connecting to database within spider: {e}")
            exit(0)

    def parse(self, response):
        for url in response.xpath("/html/body/div/div/div[4]/div/div//@href").extract():
            yield scrapy.Request(response.url + url+'catalog.html', callback=self.parse_region)

        for url in response.xpath("/html/body/div/div/div[5]/div/div//@href").extract():
            yield scrapy.Request(response.url + url+'catalog.html', callback=self.parse_region)

    def parse_region(self, response):

        thread_init = response.xpath("//div[@class='threads']//div[@class='thread grid-li grid-size-small']//@href").extract()
        threads = []

        # remove bad links
        for word in thread_init:
            if "res" in word and "#" not in word and "http" not in word:
                threads.append(word)

        # create list of tuples with each thread link, and number of comments in the thread
        try:
            number_comments = response.xpath(
                "//div[@class='threads']//div[@class='thread grid-li grid-size-small']//div[@class='replies']/strong/text()"
            ).extract()

            for val in range(len(number_comments)):
                number_comments[val] = number_comments[val].split(" ")[1]

            threads = list(
                zip(threads, number_comments)
            )  # match number of comments with respective thread

        except Exception as e:
            logging.error(f"Error parsing mainpage. URL: {response.url}: {e}")


        for thread in threads:
            url = urljoin("https://anonposted.com", thread[0])

            collection_name = response.url.split("/")[3]

            # only process page if thread does not exist in database or comments need to be updated
            existing_thread = self.db[collection_name].find_one({"url": url})
            if (
                not existing_thread
                or "comments" not in existing_thread
                or len(existing_thread["comments"]) != int(thread[1]) #new comments have been added to the thread --> extract them
            ):
                yield scrapy.Request(url, callback=self.parse_thread, meta={'handle_httpstatus_list': [302],})

    def parse_thread(self, response):

        thread_item = AnonmeItem()

        thread_item["date_of_last_scrape"] = datetime.datetime.now(pytz.utc).isoformat()
        thread_item["location"] = response.xpath("/html/body/header/h1/text()").extract()[0].split('-')[1].lstrip()
        thread_item["url"] = response.url

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

            if response.xpath("//div[@class='post op']//*[@class='subject']/text()").extract():
                thread_item["subject"] = response.xpath(
                    "//div[@class='post op']//*[@class='subject']/text()"
                ).extract()[0]

            original_post_image = urljoin(
                "https://anonposted.com",
                response.xpath("//p[@class='fileinfo']/a/@href").extract_first(),
            )
            original_post_image_name = response.xpath(
                "//p[@class='fileinfo']/span[@class='unimportant']/span/text()"
            ).extract_first()

            thread_item["original_post_image"] = {
                "image_title": original_post_image_name,
                "image_url": original_post_image,
            }

        except Exception as e:
            logging.error(f"Error parsing thread information. URL: {response.url}: {e}")

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

            except Exception as e:
                logging.error(
                    f"Error extracting comment information. URL: {response.url}: {e}"
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

                # get list of image urls for comment
                for image_info in image_urls_tuples:
                    image_url = urljoin("https://anonposted.com", image_info[0])

                    if len(original_image_names) == len(image_urls):
                        comment_item["image_info"].append(
                            {"image_title": image_info[1], "image_url": image_url}
                        )

                    else:
                        comment_item["image_info"].append({"image_url": image_url})

            except Exception as e:
                logging.error(f"Error extracting images. URL: {response.url}: {e}")

            thread_item["comments"].append(comment_item)
    
        return thread_item
