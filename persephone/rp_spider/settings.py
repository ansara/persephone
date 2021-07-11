# Scrapy settings for rp_spider project

BOT_NAME = "rp_spider"

SPIDER_MODULES = ["rp_spider.spiders"]
NEWSPIDER_MODULE = "rp_spider.spiders"

ROBOTSTXT_OBEY = False

# enables randomizing of user agents
DOWNLOADER_MIDDLEWARES = {
    "scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware": None,
    "random_useragent.RandomUserAgentMiddleware": 400,
}

# USER_AGENT_LIST = "/home/adam/persephone/persephone/rp_spider/user-agents.txt"

ITEM_PIPELINES = {"rp_spider.pipelines.MongoDBPipeline": 300}
