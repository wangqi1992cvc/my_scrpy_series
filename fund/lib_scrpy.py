# -*- coding: utf-8 -*-
"""
 @Topic:爬取的相关:
        1.数据获取
        2.数据处理
        3.数据存储...
 @Date: 2020-9-15
 @Author: terry.wang
"""
import requests
import datetime
from fake_useragent import UserAgent
from pyppeteer import launch
import asyncio
from time import time
from lib_logger import MyLogger
import logging


class libScrpy(MyLogger):
    _current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def __init__(self, level=logging.INFO):
        super().__init__(__name__, level=level)

    def mult_request(self, urls: list):
        """
        一起
        :param urls:多个url
        :return:
        """
        pass

    def request_method(self, url):
        """
        使用正常的request库请求
        :return:
        :param url:
        :return:
        """
        ua = UserAgent()
        headers = {
            'refer': 'http://fund.eastmoney.com/',
            'User-Agent': ua.random
        }
        start_time = time()
        resp = requests.request(method="GET", url=url, headers=headers)
        resp.encoding = 'utf-8'
        self.logger.info(f"request status_code:[{resp.status_code}]")

        if resp.status_code != 200:
            self.logger.info(f"Error url response status_code:{resp.status_code}")
            return

        end_time = time()
        self.logger.info(f"this request cost seconds:{end_time - start_time}")
        return resp.text

    async def pyppeteer_method(self, url):
        """
        使用pyppeteer库可以请求到js数据
        :param url:
        :return:
        """
        start_time = time()
        ua = UserAgent()
        launch_args = {
            "headless": True,
            'devtools': False,  # 控制界面的显示，用来调试
            "args": [
                "--start-maximized",
                "--no-sandbox",  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
                "--disable-infobars",
                "--ignore-certificate-errors",
                "--log-level=1",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--enable-extensions",
                "--window-size=1920,1080",
                "--refer=http://fund.eastmoney.com",
                f"\"--user-agent={ua.random}\"",
            ],
            'dumpio': True,  # 解决浏览器多开卡死
        }
        browser = await launch(**launch_args)
        page = await browser.newPage()
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                         '{ webdriver:{ get: () => false } }) }')
        resp = await page.goto(url=url, timeout=10000)
        self.logger.info(f"resp.status code:{resp.status}")
        if resp.status != 200:
            self.logger.info(f"Error resp.status code: {resp.status}.")
            return None
        text = await page.content()
        await browser.close()
        end_time = time()
        self.logger.info(f"this request cost seconds:{end_time - start_time}")

        return text

    def proxy_pool_set(self):
        """
        代理设置
        :return:
        """
        pass

    def save_to_file(self, content):
        """
        保存内容到文件
        :param content:
        :return:
        """
        pass

# if __name__ == "__main__":
#     scrpp=libScrpy()
#     resp=scrpp.fund_request_by_code('512000',1)
#     # resp=scrpp.fund_request_by_code('512000')

