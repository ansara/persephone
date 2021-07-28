import scrapy

# object that represents an entire thread
class AnonmeItem(scrapy.Item):
    original_post_text = scrapy.Field()
    original_post_date = scrapy.Field()
    original_post_id = scrapy.Field()
    original_post_image = scrapy.Field()
    date_of_last_scrape = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    subject = scrapy.Field()

    comments = scrapy.Field()  # uses commentItem object

class CommentItem(scrapy.Item):
    text = scrapy.Field()
    date = scrapy.Field()
    comment_id = scrapy.Field()
    comment_link = scrapy.Field()
    reply_ids = scrapy.Field()
    image_info = scrapy.Field()  # tuple of image name and url