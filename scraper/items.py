# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class CovivioItem(Item):
    id = Field()
    title = Field()
    link = Field()
    anzahl_zimmer = Field()
    adresse = Field()
    regionaler_zusatz = Field()
    wohnflaeche = Field()
    kaltmiete = Field()
    merkmale = Field()
    bilder = Field()
