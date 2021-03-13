import scrapy
from scrapy.loader import ItemLoader
from legalApp.items import CategoriaLegalAppItem


class CategoriaSpider(scrapy.Spider):
    name = 'categoria'
    allowed_domains = ['www.legalapp.gov.co']
    start_urls = ['https://www.legalapp.gov.co/categoria']

    def parse(self, response):
        subcategorias = response.xpath('//div[contains(@id,"heading")]/h4/a')
        
        for sub in subcategorias:
                
            loader = ItemLoader(item=CategoriaLegalAppItem(), selector=sub, response=response)
            loader.add_xpath('subcategoria', './/li/div/text()')
            loader.add_xpath('link', './/@href')
            
            yield loader.load_item()
