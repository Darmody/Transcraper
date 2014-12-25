# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy2 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = 'Scraper_meihua'

SPIDER_MODULES = ['Scraper.spiders']
NEWSPIDER_MODULE = 'Scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy2 (+http://www.yourdomain.com)'

DOWNLOAD_HANDLERS = {
    # 'http': 'scrapyjs.dhandler.WebkitDownloadHandler',
    # 'https': 'scrapyjs.dhandler.WebkitDownloadHandler',
}

DOWNLOADER_MIDDLEWARES = {
	'scrapy_proxy.proxyMiddleware.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

ITEM_PIPELINES = {
	'Scraper.pipelines.RcdArticlePipeline': 1000,
	
	# 'scrapy_redis.pipelines.RedisPipeline': 1,
}

# redis scheduling
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

SCHEDULER_PERSIST = True

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

REDIS_URL = 'redis://10.0.0.4:6379'

# LOG SETTING
# LOG_LEVEL = 'INFO'
# LOG_ENABLED = False
# LOG_STDOUT = True
# LOG_FILE = 'logs/' + ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16))) + '_scrapy.log'

# Graphite
# STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'

# concurrent

# CONCURRENT_REQUESTS = 1
# CONCURRENT_REQUESTS_PER_DOMAIN = 1

# user agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'

# timeout
# DOWNLOAD_TIMEOUT = 5

# DOWNLOAD_DELAY = 0.6

# webservice
# WEBSERVICE_HOST = '0.0.0.0'

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
