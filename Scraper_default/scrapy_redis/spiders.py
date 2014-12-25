# -*- coding: utf-8 -*-

import connection

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spider import Spider
from scrapy import log
from scrapy.http import Request

from cookieManage.CookieManage import CookieManage

import cookieManage.CookieManage as cookiemanage
import json
import Scraper.custom_settings as SETTING_SCRAPER

class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    redis_key = None  # use default '<spider>:start_urls'

    def setup_redis(self):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name

        self.server = connection.from_settings(self.crawler.settings)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        self.log("Reading URLs from redis list '%s'" % self.redis_key)
    
    def page_handle(self, sel, page_source, url, category, content_type):
        """处理网页的解析"""

        # 保存网页源码
        page_source['page_source'] = [s.encode('unicode_escape') for s in sel.xpath('*').extract()]
        page_source['url'] = url
        page_source['category'] = category
        page_source['content_type'] = content_type
        page_source['title'] = [s.encode('unicode_escape') for s in sel.xpath('//head//title/text()').extract()]

        return page_source

    def push_url(self, url):
        """将url加入调度队列"""

        self.server.rpush(self.redis_key, url)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        url = self.server.lpop(self.redis_key)
        if url:
            return self.make_requests_from_url(url)

    def schedule_next_request(self):
        """Schedules a request if available"""
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_request()
        raise DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        """Avoids waiting for the spider to  idle before scheduling the next request"""
        self.schedule_next_request()

class RedisSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def set_crawler(self, crawler):
        super(RedisSpider, self).set_crawler(crawler)
        self.setup_redis()

class RedisSinaWeiboSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def set_crawler(self, crawler):
        super(RedisSpider, self).set_crawler(crawler)
        self.setup_redis()

    def push_except_url(self, url):

        self.server.rpush('%s:except_urls' % self.name, url)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        url = self.server.lpop(self.redis_key)
        if url:

            cm = CookieManage(SETTING_SCRAPER)

            account = eval(cm.switchAccount(cookiemanage.i, url, self.redis_key))

            cookiemanage.i = (cookiemanage.i + 1) % SETTING.MATCHES

            message = '[NEW REQUEST][RequestUrl:' + url + ']' + '[AccountInfo:' + account['username'] +  ']'

            log.msg(message, level=log.INFO)

            return Request(url, 
                cookies=account['cookie'], 
                # dont_filter=True, 
                # meta={'proxy': PROXY_IP}
                )

    def request_redirect_handle(self, response, cm):

        if response.url.find('login.weibo') >= 0:

            self.push_url(response.url)

            log.msg('invalid account cookie, retry logining.', level=log.WARNING)

            cm.relogin()

            return

        if response.url.find('weibo.cn/pub') >= 0:

            self.push_url(response.url)

            log.msg('redirecting to weibo pub page，the ip might be restricted! Check please.', level=log.WARNING)

            return