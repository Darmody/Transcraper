#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import selenium
import json
import redis

from scrapy import log

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import sys;
sys.path.append(".")

import custom_settings as SETTING

i = 0

NODE_ACCOUNT_POOL = SETTING.NODE + SETTING.ACCOUNT_POOL

class CookieManage:

	def __init__(self):

		self.redis = redis.Redis(host=SETTING.REDIS_STORAGE_HOST, port=6379)

	# 登录并返回cookie
	def login(self, username, password):

		service_args = [
			'--proxy=' + SETTING.PROXY_IP,
			'--proxy-auth=471306909:13571845363',
			'--proxy-type=http',
		]

		browser = webdriver.PhantomJS(executable_path=SETTING.PHANTOMJS_LOCATION, 
			service_args=service_args)

		browser.get(SETTING.LOGIN_URL)

		un = browser.find_element_by_name('mobile')
		un.send_keys(username)
		pd = browser.find_elements_by_tag_name('input')[1]
		pd.send_keys(password)
		browser.find_elements_by_tag_name('input')[7].click()

		return browser.get_cookies()

	def relogin(self):

		for i in range(0, SETTING.MATCHES):

			account = eval(self.redis.lindex(SETTING.NODE_ACCOUNT_POOL, i))

			account['cookie'] = self.login(account['username'], account['password'])

			self.redis.lset(SETTING.NODE_ACCOUNT_POOL, i, account)

			log.msg('账号重新登录：' + account.__str__(), level=log.INFO)

	def updateAccountInfoFromFile(self):

		accountFile = open('../file/' + SETTING.NODE + '_account_info.txt', 'r')

		for line in accountFile:

			if line.startswith('IP:'):

				continue

			attrs = line.split('----')

			if len(attrs) > 0 :

				cookie = self.login(attrs[0], attrs[1])

				newAccount = {'username': attrs[0], 'password': attrs[1], 'cookie': cookie}

				print '添加账号：' + newAccount.__str__()

				self.redis.rpush(SETTING.NODE_ACCOUNT_POOL, newAccount)

	def updateAccountInfoFromPool(self):

		for i in range(0, SETTING.MATCHES):

			account = eval(self.redis.lpop(SETTING.ACCOUNT_STORAGE_POOL))

			if account == None:

				print '账号池已空'

				return

			cookie = self.login(account['username'], account['password'])

			newAccount = {'username': account['username'], 'password': account['password'], 'cookie': cookie}

			print '添加账号：' + newAccount.__str__()

			self.redis.rpush(SETTING.NODE_ACCOUNT_POOL, newAccount)

	def initNode(self):

		r = redis.Redis(host=SETTING.REDIS_STORAGE_HOST, port=6379)

		ip = r.lpop(SETTING.IP_STORAGE_POOL)

		if ip == None:

			print 'ip池已空'

			return

		f = open('home/scraper/Scraper/Scraper/custom_settings.py', 'a')

		f.write('PROXY_IP = http://' + ip + '\n')

		print '获取到新的IP:' + ip

		r.incr('node_code')

		node_code = r.get('node_code')

		f.write('NODE = node' + node_code.__str__())

		print '节点建立，编号：' + node_code.__str__()

		f.close()


	def switchAccount(self, index, requestUrl, key):

		data = self.redis.lindex(SETTING.NODE_ACCOUNT_POOL, index)

		if data is None:

			raise NoAccountException(requestUrl, key)

		return data

class NoAccountException(Exception):

	def __init__(self, requestUrl, key):

		Exception.__init__(self)

		r = redis.Redis(host=SETTING.EDIS_SERVER_HOST, port=6379)		

		r.rpush(key, requestUrl)

		log.msg('no valid account in the account pool.', level=log.ERROR)

def main():

	cm = CookieManage()

	cm.initNode()

	cm.updateAccountInfoFromPool()

if __name__ == '__main__':
    main()
