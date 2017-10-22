# -*- coding: utf-8 -*-

import scrapy
from SpiUqam.items import *

class LavalSpider(scrapy.Spider):
    name = "laval"
    allowed_domains = ["ulaval.ca"]
    start_urls = [
        #"https://www.ulaval.ca/les-etudes/programmes/repertoire/details/baccalaureat-en-administration-des-affaires-baa.html",
        "https://www.ulaval.ca/les-etudes/programmes/repertoire/details/baccalaureat-en-sociologie-ba.html"
    ]

    def parse(self, response):
        #informations propres au programme
        item = SpiProgramme()
        item['titreprog'] = response.xpath('//title/text()').extract()
        item['presprog'] = response.xpath('//div[@id="apercu_content"]/div/div[@class="bloc descprog"]/div/div/p/text()').extract()
        item['structprog'] = response.xpath('//div[@id="structure-programme_content"]').extract()
        yield item
        #aller chercher les liens vers les cours
        programme = response.xpath('//table[@class="cours"]//td[@class="col1"]/a')
        for cours in programme:
            url_partiel = cours.xpath('@href').extract()
            url_string = "".join(url_partiel)
            url = "https://www.ulaval.ca" + url_string
            #On cree la requete
            r = scrapy.Request(url, callback=self.parse_dir_contents)
            r.meta['origine'] = item['titreprog'] #servira de fk
            yield r

    #informations propres aux différents cours
    #ATTENTION: A cause des multi-concentrations, il est possible que certains cours
    #se retrouvent plusieurs fois dans la db géré par l'import sur Flask???
    def parse_dir_contents(self, response):
        item = SpiCours()
        string = ""
        sigle = response.xpath('//h1[@class="fiche"]/text()').extract()
        titre = response.xpath('//h1[@class="fiche"]/span/text()').extract()
        item['titre'] = [sigle[0] + titre[0]]
        item['description'] = response.xpath('normalize-space(//div[@id="renseignements_content"]//div[@class="txt"]/text())').extract()
        item['progOrigine'] = response.meta['origine']
        yield item
