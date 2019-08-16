# -*- coding: utf-8 -*-
import scrapy
from edina.items import EdinaItem

class EdinaSpider(scrapy.Spider):
    name = 'edinaSpider'
    # allowed_domains = ['https://www.edina.com.ec/']
    start_urls = ['https://www.edina.com.ec/guia-telefonica/guia_telefonica.aspx?txtBuscarPlus=&txtDondePlus=9%3A238%3A-1%3BGuayaquil%2C+Guayas&b=empresas&c=Guayaquil%2C+Guayas']

    def parse(self, response):
        containers = response.xpath('//div[@class="box box__ins1 estiloSep"]')
        for c in containers:
            name = c.xpath('.//h2/text()').extract_first()
            direction = c.xpath('.//p[contains(.,"Dirección")]/text()').extract()
            category = c.xpath('.//h3//a/text()').extract()
            website = c.xpath('.//a[contains(@rel, "nofollow")]/@href').extract_first()
            anounce = EdinaItem()
            anounce['name'] = name
            anounce['direction'] = direction
            anounce['category'] = ';'.join(category)
            if website is not None:
                anounce['website'] = website[website.index('http'):website.index('&i=')]
            yield anounce

        next_page = ''.join(response.xpath('//a[contains(., "Siguiente") and @class="estLinkPagi"]/@href').extract())
        print(next_page)
        if next_page is not None:
            yield response.follow('https://www.edina.com.ec/' + next_page, callback=self.parse)

