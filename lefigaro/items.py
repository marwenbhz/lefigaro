# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LefigaroItem(scrapy.Item):
    # define the fields for your item here like:
    TITRE_ANNONCE = scrapy.Field()
    PRICE = scrapy.Field()
    M2_TOTAL = scrapy.Field()
    NBR_PIECES = scrapy.Field()
    NBR_CHAMBRES = scrapy.Field()
    VILLE = scrapy.Field()
    ANNONCE_LINK = scrapy.Field()
    CODE_POSTAL = scrapy.Field()
    AGENCE_NOM = scrapy.Field()
    #DESCRIPTION = scrapy.Field()
    ADRESSE = scrapy.Field()
    AGENCE_ADRESSE_TELEPHONE = scrapy.Field()
    PAYS = scrapy.Field()
