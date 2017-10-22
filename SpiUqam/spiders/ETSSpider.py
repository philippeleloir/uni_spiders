# -*- coding: utf-8 -*-

import scrapy

from SpiUqam.items import *

class ETSSpider(scrapy.Spider):
    name = "ets"
    allowed_domains = ["etsmtl.ca"]
    start_urls = [
        "https://www.etsmtl.ca/Programmes-Etudes/1er-cycle/Bac/7065"
    ]

    def parse(self, response):
        #informations propres au programme
        item = SpiudemProgramme()
        item['titreprog'] = response.xpath('//h1[@id="etsTP"]/text()').extract()
        item['presprog'] = response.xpath('//div[@id="plc_lt_zoneMain_pageplaceholder_pageplaceholder_lt_zoneContent_pageplaceholder_pageplaceholder_lt_zoneCenter_pageplaceholder_pageplaceholder_lt_zoneLeft_repeater_repItems_ctl00_ctl00_PanelObjectifs"]/text()').extract()[1:8]
        #aller chercher les liens vers les cours
        yield item
        programme = response.xpath('//div[@id="plc_lt_zoneMain_pageplaceholder_pageplaceholder_lt_zoneContent_pageplaceholder_pageplaceholder_lt_zoneCenter_pageplaceholder_pageplaceholder_lt_zoneLeft_repeater_repItems_ctl00_ctl00_PanelCoursASuivre"]//table[@class="etsTableauDeBase"]/tbody/tr')
        for cours in programme:
            itemtest = SpiudemCours()  ## a retirer + tester
            #definir le titre du cours - concaténation de deux champs
            sigle = cours.xpath('td[1]/text()').extract()
            titre = cours.xpath('td/a[1]/text()').extract()
            tc = sigle + titre
            string = " ".join(tc)
            ###On definit l'url du cours pour le callback
            url_partiel = cours.xpath('td/a[1]/@href').extract()
            url_string = "".join(url_partiel)
            url = "https://www.etsmtl.ca" + url_string
            r = scrapy.Request(url, callback=self.parse_dir_contents)
            r.meta['origine'] = item['titreprog'] # servira de fk
            r.meta['titrecours'] = [string]
            yield r
            #yield itemtest

    #informations propres aux différents cours
    def parse_dir_contents(self, response):
        item = SpiudemCours()
        item['titre'] = response.meta['titrecours']
        item['description'] = response.xpath('//span[@id="plc_lt_zoneMain_pageplaceholder_pageplaceholder_lt_zoneCenter_FicheCours_LabelDescription"]/text()').extract()
        item['progOrigine'] = response.meta['origine']
        #progMain = La premiere entree sur le site
        #progBulk = Une liste de tous les programmes avec <html>
        #progOrigine = Le programme a l'origine du crawl. -fk
        yield item
