# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiProgramme(scrapy.Item):
    titreprog = scrapy.Field()
    presprog = scrapy.Field()
    structprog = scrapy.Field()
    #html de la structure du prog
    #Nb: Il faudra tout de meme ajouter un doctype/head/meta utf-8

class SpiCours(scrapy.Item):
    titre = scrapy.Field()
    description = scrapy.Field()
    progOrigine = scrapy.Field()
