# -*- coding: utf-8 -*-

import scrapy

from SpiUqam.items import *

class UdeMspider(scrapy.Spider):
    name = "udem"
    allowed_domains = ["umontreal.ca"]
    start_urls = [
        ### utiliser structure-du-programme permet de faire une seule requete au site de l'udem
        "https://admission.umontreal.ca/programmes/baccalaureat-en-informatique/structure-du-programme/"
        #"https://admission.umontreal.ca/programmes/baccalaureat-en-physique/structure-du-programme/",
        #"https://admission.umontreal.ca/programmes/baccalaureat-en-demographie-et-statistique/structure-du-programme/",
        #"https://admission.umontreal.ca/programmes/baccalaureat-en-sciences-de-la-sante-ergotherapie/structure-du-programme/"
    ]

    def parse(self, response):
        #informations propres au programme
        item = SpiProgramme()
        item['titreprog'] = response.xpath('//title/text()').extract()
        item['presprog'] = response.xpath('normalize-space(//script[@type="application/ld+json"])').extract() ##donne un JSON, a reformater mieux
        item['structprog'] = response.xpath('//div[@class="l-wrap"]/div[@class="l-twothird"]').extract()
        #item['objprog'] = response.xpath('normalize-space(//div[@class="OBJECTIF"]/div/p)').extract()
        yield item
        #aller chercher les liens vers les cours
        x = 0
        programme = response.xpath('//tbody[@class="programmeCourse fold"]')
        for cours in programme:
            itemcours = SpiCours()
            string = ""
            titre = cours.xpath('normalize-space(tr/td[1]/text())').extract()
            sigle = cours.xpath('tr/th/a/text()').extract()
            #string.join(sigle[0])
            #string.join(" ")
            #string.join(titre[0])
            itemcours['titre'] = [sigle[0] + " " + titre[0]]
            liste = cours.xpath('//div[@class="txt"]/text()').extract()
            itemcours['description'] = [liste[x].strip()]
            itemcours['progOrigine'] = item['titreprog']
            x += 1
            yield itemcours
