# -*- coding: utf-8 -*-

import scrapy

from SpiUqam.items import *

class UQAMSpider(scrapy.Spider):
    name = "uqam"
    allowed_domains = ["uqam.ca"]
    start_urls = [
        #"http://www.etudier.uqam.ca/programme?code=7054"
        "https://www.etudier.uqam.ca/programme?code=7316"
        #"https://www.etudier.uqam.ca/programme?code=7361",
        #"https://www.etudier.uqam.ca/programme?code=7060"
        #"http://www.etudier.uqam.ca/programme?code=7324"
    ]

    def parse(self, response):
        #informations propres au programme
        item = SpiProgramme()
        item['titreprog'] = response.xpath('normalize-space(//title/text())').extract()
        item['presprog'] = response.xpath('normalize-space(//div[@class="PRESENTATION"]/p)').extract()
        item['structprog'] = response.xpath('//div[@id="block-system-main"]').extract()
        yield item
        #aller chercher les liens vers les cours
        programme = response.xpath('//div[@class="bloc_cours"]//div[@class="actions"]/a')
        for cours in programme:
            url_partiel = cours.xpath('@href').extract()
            url_string = "".join(url_partiel)
            url = "https://etudier.uqam.ca" + url_string
            #On cree la requete
            r = scrapy.Request(url, callback=self.parse_dir_contents)
            r.meta['origine'] = item['titreprog'] # servira de fk
            yield r

    #informations propres aux différents cours
    def parse_dir_contents(self, response):
        item = SpiCours()
        item['titre'] = response.xpath('normalize-space(//title/text())').extract()
        item['description'] = response.xpath('normalize-space(//div[@class="rubrique"]/p)').extract()
        item['progOrigine'] = response.meta['origine']
        yield item
