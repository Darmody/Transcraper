# -*- coding: utf-8 -*-

# 自定义全局变量配置文件

# 节点
# NODE = 'node1'

# 数据存储
REDIS_STORAGE_URL = 'http://10.0.0.8:6379'
REDIS_STORAGE_HOST = '10.0.0.8'

# redis调度
REDIS_SERVER_URL = 'http://10.0.0.4:6379'
REDIS_SERVER_HOST = '10.0.0.4'

# Cookie管理
LOGIN_URL = 'http://login.weibo.cn/login/?ns=1'
ACCOUNT_POOL = ':account_pool'
ACCOUNT_STORAGE_POOL = 'account_storage_pool'
IP_STORAGE_POOL = 'ip_storage_pool'
MATCHES = 3

# phantomsjs路径
PHANTOMJS_LOCATION = '/home/scraper/phantomjs-1.9.7-linux-x86_64/bin/phantomjs'

# 代理IP
PROXY_AUTH = 'Basic NDcxMzA2OTA5OjEzNTcxODQ1MzYz'
# PROXY_IP = 'http://106.186.18.67:62011'