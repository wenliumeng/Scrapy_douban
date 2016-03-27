# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class DoubanmoiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    year = Field()
    score = Field()
    director = Field()
    classification = Field()
    actor = Field()

class DoubanbookItem(scrapy.Item):
    name = Field()
    images = Field()
    author = Field()
    publisher = Field()
    publisher_year = Field()
    original_name = Field()
    translator = Field()
    page_number = Field()
    price = Field()
    binding = Field()
    series = Field()
    ISBN = Field()
    score = Field()
    evaluate_number = Field()
    one_star = Field()
    two_star = Field()
    three_star = Field()
    four_star = Field()
    five_star = Field()
