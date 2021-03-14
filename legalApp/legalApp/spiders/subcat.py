import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from legalApp.items import RespuestasLegalAppItem


class SubcatSpider(CrawlSpider):
    name = 'subcat'
    allowed_domains = ['www.legalapp.gov.co']
    start_urls = ['https://www.legalapp.gov.co/sub/acciones-constitucionales']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//i[@class="triangulo"]/following-sibling::a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    
        descripcion = response.xpath('//*[@class="description textRegularjq"]').getall()
        que_hacer = response.xpath('//div[@id="quehacer"]/div').get()
        donde_acudir = response.xpath('//*[@id="ulacudir"]').getall()
        tenga_encuenta = response.xpath('//div[@id="tengaencuenta"]/div/div').getall()
        normatividad = response.xpath('.//*[@id="collapseDos"]/div').getall()
        fecha = response.xpath('//p[@class="update"]/text()').get()
        
        loader = ItemLoader(item=RespuestasLegalAppItem(), response=response)
        loader.add_xpath('pregunta', '//div[@class="titulo-imagen pull-left"]/following-sibling::h3/text()')
        loader.add_value('descripcion', descripcion)
        loader.add_value('que_hacer', que_hacer)
        loader.add_value('donde_acudir', donde_acudir)
        loader.add_value('tenga_encuenta', tenga_encuenta)
        loader.add_value('normatividad', normatividad)
        loader.add_value('fecha', fecha)
        
        yield loader.load_item()
