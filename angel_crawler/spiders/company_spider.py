# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CompanySpider(scrapy.Spider):
    name = 'company_spider'
    
    # custom_settings = {
    #     'SPLASH_URL': 'http://localhost:8050',
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'scrapy_splash.SplashCookiesMiddleware': 723,
    #         'scrapy_splash.SplashMiddleware': 725,
    #         'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    #     }
    #     'SPIDER_MIDDLEWARES': {
    #         'scrapy_splash.SplashDeduplicateArgsMiddleware': 810,
    #     }
    #     'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    # }

    def start_requests(self):
        yield SplashRequest(
            url='https://angel.co/companies?locations[]=1688-United+States&tab=hiring&stage[]=Series+A&stage[]=Series+B&stage[]=Series+C',
            callback=self.parse,
        )

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for entry in response.css('div.base.startup'):
            yield {
                'company': entry.css('a.startup-link::text').extract_first(),
                'pitch': entry.css('div.pitch::text').extract_first(), 
                'location': entry.css('div.column.location div.value div.tag a::text').extract_first(),
                'market': entry.css('div.column.market div.value div.tag a::text').extract_first(), 
                'website': entry.css('div.column.website div.value div.website a::attr(href)').extract_first(), 
                'employees': entry.css('div.column.company_size div.value::text').extract_first(), 
                'stage': entry.css('div.column.stage div.value::text').extract_first(),
                'total_raised': entry.css('div.column.raised div.value::text').extract_first(),
            }

