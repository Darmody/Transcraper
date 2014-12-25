# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
# import base64 

import Scraper.custom_settings as SETTING
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = SETTING.PROXY_IP
  
        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = SETTING.PROXY_IP
        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = SETTING.PROXY_AUTH # 'Basic ' + encoded_user_pass
