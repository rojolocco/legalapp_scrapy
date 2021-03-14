import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from legalApp.items import PreguntasLegalAppItem


class PreguntasSpider(CrawlSpider):
    name = 'preguntas'
    allowed_domains = ['www.legalapp.gov.co']
    start_urls = ['https://www.legalapp.gov.co/categoria']
    
    ID = 0

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@id,"heading")]/h4/a'), callback='parse_item', follow=True),
    )
    

    def parse_item(self, response):
        preguntas = response.xpath('//i[@class="triangulo"]/following-sibling::a')
        Id_local = 0
        for q in preguntas:
            self.ID += 1
            Id_local += 1
            loader = ItemLoader(item=PreguntasLegalAppItem(), selector=q, response=response)
            loader.add_value('Id_total', self.ID)
            loader.add_value('Id_local', Id_local)
            loader.add_xpath('pregunta', './/text()')
            loader.add_xpath('link', './/@href')
            
            yield loader.load_item()
