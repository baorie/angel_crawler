# -*- coding: utf-8 -*-
import scrapy
import os

class AngelLoginSpider(scrapy.Spider):
    name = 'angel_login'
    login_url = 'http://angel.co/login/'
    start_urls = [login_url]

    def parse(self, response):
        # extract the csrf token
        token = response.css('meta[name="csrf-token"]::attr(content)').extract_first()
        # dictionary with form values
        data = {
                'csrf-token': token,
                'user_email': os.environ.get('ANGEL_USER'),
                'user_password': os.environ.get('ANGEL_PW'),
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_info)
    
    def parse_info(self, response):
        self.log('I just visited: ' + response.text())
        pass

