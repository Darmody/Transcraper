# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Scraper.items import rcdAriticleItem
import Scraper.custom_settings as SETTING

from scrapy import log
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

import re
import redis
import json
import time
	

# rcd文章处理
class RcdArticlePipeline(object):

	def __init__(self):
		
		# scrapy-json解析
		self.encoder = ScrapyJSONEncoder()
	
	def process_item(self, item, spider):

		return deferToThread(self._process_item, item, spider)

	def _process_item(self, item, spider):

		if not isinstance(item, rcdAriticleItem):

			return item

		# 存储数据
		if len(item['title']) > 0:

			item['title'] = item['title'][0].decode('unicode_escape').encode('utf-8')
			item['articleLink'] = item['articleLink'][0].decode('unicode_escape').encode('utf-8')
			item['abstract'] = item['abstract'][0].decode('unicode_escape').encode('utf-8')
			item['catalog'] = [s.decode('unicode_escape').encode('utf-8') for s in item['catalog']] 
			
			for theTime in item['post_time']:

				if theTime.find('(') != -1:
					
					if theTime.find('ago') != -1:

						item['post_time'] = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
					else:

						# 解析日期
						pattern = re.compile(r'\((.*)\)')	
			
						theTime = pattern.search(theTime.decode('unicode_escape').encode('utf-8')).group(1)
						
						item['post_time'] = theTime

					break

			item['found_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))		#抓取时间			

			# redis存储

			# 定义redis服务器连接
			self.redis_storage = redis.from_url(SETTING.REDIS_STORAGE_URL)
			self.redis_server = redis.from_url(SETTING.REDIS_SERVER_URL)

			# 存储article信息
			self.redis_storage.set('rcd_article:' + item['articleLink'], self.encoder.encode(item))

			# 蔓延
			# self.redis_server.rpush('sina_comment_cn:start_urls', 'http://weibo.cn/comment/' + item['weibo_id'])

		return item