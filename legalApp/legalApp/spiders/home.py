import scrapy
from scrapy.loader import ItemLoader
from legalApp.items import HomeLegalAppItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['legalapp.gov.co']
    start_urls = ['https://legalapp.gov.co']

    def parse(self, response):
        categorias = response.xpath('//div[@class="caja"]')
        Id = 0
        
        for cat in categorias:
            Id += 1
            loader = ItemLoader(item=HomeLegalAppItem(), selector=cat, response=response)
            loader.add_value('Id', Id)
            loader.add_xpath('categoria', './/a/div[2]/text()')
            loader.add_xpath('link', './/a/@href')
            
            yield loader.load_item()
        