# -*- coding: utf-8 -*-
import json
from pprint import pprint

from scrapy import Spider, Request

from zhihu_user.items import UserItem


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'Just_blue'
    url_user = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    url_follow = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}'
    follow_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20'

    url_fans = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}'
    fans_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20'

    def start_requests(self):
        yield Request(self.url_user.format(user = self.start_user,include = self.user_include ),callback=self.user_parse)
        yield Request(self.url_follow.format(user = self.start_user ,include = self.follow_include ,offset = 0),callback= self.follow_parse)
        yield Request(self.url_fans.format(user=self.start_user, include=self.follow_include, offset=0),callback=self.fans_parse)


    def user_parse(self, response):
        result = json.loads(response.text)
        pprint(result)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(self.url_follow.format(user=result.get('url_token'),include = self.follow_include,offset = 0),callback=self.follow_parse)

    def follow_parse(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield  Request(self.url_user.format(user = result.get('url_token'),include = self.user_include),callback=self.user_parse)

        if 'paging'in results.keys() and  results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.follow_parse)

    def fans_parse(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield  Request(self.url_user.format(user = result.get('url_token'),include = self.user_include),callback=self.user_parse)

        if 'paging'in results.keys() and  results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,self.fans_parse)



