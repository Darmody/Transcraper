# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# article

class meihuaPageSourceItem(Item):

	url = Field()						# 请求url
	page_source = Field()				# 网页源码 
	category = Field()					# 分类
	content_type = Field()				# 内容类型
	title = Field()						# 作者
	found_time = Field()				# 抓取时间

class meihuaPostItem(Item):

	url = Field()						# 请求url
	title = Field()						# 文章标题
	articleLink = Field()				# 原文链接
	abstract = Field()					# 内容摘要
	catalog = Field()					# 分类
	post_time = Field()					# 内容摘要日期
	found_time = Field()				# 抓取时间