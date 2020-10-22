import json
import math
from collections import OrderedDict

import scrapy
from ..items import WeiboItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=1005051669879400']

    def parse(self, response):
        r = json.loads(response.text)
        item = WeiboItem()

        if r['ok']:
            for key in item.fields:
                item[key] = r['data']['userInfo'].get(key, '')
            params = {
                'containerid': '230283' + str(item['id']) + '_-_INFO'
            }
            yield scrapy.FormRequest(url='https://m.weibo.cn/api/container/getIndex?', formdata=params, method='GET',
                                     meta={'item': item}, callback=self.parse_card_info)

    def parse_card_info(self, response):
        item = response.meta['item']
        user_info = {}
        r = json.loads(response.text)
        zh_list = [
            u'生日', u'所在地', u'小学', u'初中', u'高中', u'大学', u'公司', u'注册时间',
            u'阳光信用'
        ]
        en_list = [
            'birthday', 'location', 'education', 'education', 'education',
            'education', 'company', 'registration_time', 'sunshine'
        ]

        for i in en_list:
            user_info[i] = ''
        if r['ok']:
            cards = r['data']['cards']
            if isinstance(cards, list) and len(cards) > 1:
                card_list = cards[0]['card_group'] + cards[1]['card_group']
                for card in card_list:
                    if card.get('item_name') in zh_list:
                        user_info[en_list[zh_list.index(
                            card.get('item_name'))]] = card.get(
                            'item_content', '')
            item['user_info'] = user_info
        params = {
            # 231051_-_followers_-_1669879400_-_1042015:tagCategory_050
            'containerid': '231051_-_followers_-_' + str(item['id']) + '_-_1042015:tagCategory_050',
            'page': '1',
        }
        star_list = []
        yield scrapy.FormRequest(url='https://m.weibo.cn/api/container/getIndex', formdata=params, method='GET',
                                 meta={'item': item, 'star_list': star_list, 'page': 1}, callback=self.parse_stars)

    def parse_stars(self, response):
        item = response.meta['item']
        page = response.meta['page'] + 1
        star_list = response.meta['star_list']
        r = json.loads(response.text)

        for i in r['data']['cards'][-1]['card_group']:
            # TODO 讲每一个被关注的人再yield回parse_starts
            star_list.append(i['user']['id'])

        if page <= math.ceil(int(item['follow_count']) / 20) and page <= 10:
            params = {
                'containerid': '231051_-_followers_-_' + str(item['id']) + '_-_1042015:tagCategory_050',
                'page': str(page),
            }
            yield scrapy.FormRequest(url='https://m.weibo.cn/api/container/getIndex', formdata=params, method='GET',
                                     meta={'item': item, 'star_list': star_list, 'page': page},
                                     callback=self.parse_stars)
        else:
            item['star_list'] = star_list
            yield item
            # https://m.weibo.cn/api/container/getIndex?containerid=100505 1669879400
            for star in star_list:
                yield scrapy.Request(url='https://m.weibo.cn/api/container/getIndex?containerid=100505%d' % star,
                                     callback=self.parse)
