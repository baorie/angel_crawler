# -*- coding: utf-8 -*-
import scrapy
import os

class CompanySpiderSpider(scrapy.Spider):
    name = 'company_spider'
    login_url = 'http://angel.co/login'
    start_urls = [login_url]

    def parse(self, response):
        # extract the csrf token value
        token = response.css('meta[name="csrf-token"]::attr(content)').extract_first()
        # create a python dictionary with the form values
        data = {
            'csrf-token' : token,
            'user_email': os.environ.get('ANGEL_EMAIL'),
            'password': os.environ.get('ANGEL_PASS'),
        }
        # submit a POST request to it
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_jobs)

    def parse_jobs(self, response):
        # parse the job page after the spider is logged in
        job_page_url = 'https://angel.co/jobs#find/f!%7B{}%7D'
        # change the double quotes to %22 later if you need to
        city_url = job_page_url.format("locations"%3A%5B"1664-New York City%2C NY"%5D)
        # for each company in the company listing
        for c in response.css('div.fbw9'):
            item = {
                'company_name': c.css('a.startup-link::text').extract_first(),
                'company_profile': c.css('div.tagline::text').extract_first(),
                # create expandable array of jobs w job_title and job_profile
                'job_title': c.css('div.listing-row div.top div.title a[target=_blank]::text').extract(),
                'job_profile': c.css('div.listing-row div.top div.tags::text').extract(),
            }
            yield item
            # incorporate JavaScript
