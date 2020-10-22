# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboItem(Item):
    id = Field()
    screen_name = Field()
    profile_image_url = Field()
    profile_url = Field()
    statuses_count = Field()
    verified = Field()
    verified_type = Field()
    verified_type_ext = Field()
    verified_reason = Field()
    close_blue_v = Field()
    description = Field()
    gender = Field()
    mbtype = Field()
    urank = Field()
    mbrank = Field()
    followers_count = Field()
    follow_count = Field()
    cover_image_phone = Field()
    avatar_hd = Field()
    user_info = Field()
    star_list = Field()
