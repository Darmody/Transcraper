# -*- coding:utf-8 -*-

from selenium import webdriver

from twisted.internet import defer

from scrapy import log
from scrapy.http import HtmlResponse
from scrapy.core.downloader.handlers.http import HTTP10DownloadHandler

class WebkitDownloadHandler(HTTP10DownloadHandler):

    # 重写download_request方法
    def download_request(self, request, spider):

        # print 'real IP: ' + request.meta['proxy']

        if 'renderjs' in request.meta:

            d = defer.Deferred()
            d.addErrback(log.err, spider=spider)

            # 加载PhantomJS引擎
            driver = webdriver.PhantomJS(executable_path='/home/test/phantomjs-1.9.7-linux-x86_64/bin/phantomjs')

            # 设置超时
            driver.set_script_timeout(5)
            driver.set_page_load_timeout(5)

            self._login(driver)

            # 访问url
            driver.get(request.url)
            # 获取源码
            html = driver.page_source

            response = HtmlResponse(request.url, encoding='utf-8', body=html.encode('utf-8'))

            d.callback(response)

            return d

        else:
            return super(WebkitDownloadHandler, self).download_request(request, spider)

    # 登录方法
    def _login(self, driver):

        driver.get('http://weibo.com/login.php')
        # 模拟浏览器操作登录
        username = driver.find_element_by_class_name('username').find_element_by_tag_name('input')
        username.send_keys('yuxiaowei34@163.com')
        password = driver.find_element_by_class_name('password').find_element_by_tag_name('input')
        password.send_keys('Abcd1234')
        driver.find_element_by_class_name('W_login_form').find_element_by_class_name('W_btn_g').click()