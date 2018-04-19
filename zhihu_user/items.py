# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    name = Field()
    follower_count = Field()
    answer_count = Field()
    articles_count =Field()
    headline = Field()
    id = Field()
    url_token =Field()



