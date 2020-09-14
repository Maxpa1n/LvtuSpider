# coding=utf-8
import json
import random
import time

import requests
from pyquery import PyQuery as pq
from tqdm import tqdm
from utils.header_config import user_agent
from utils.page import get_one_page_index, get_page_number


class PageSpider(object):
    def __init__(self):
        pass

    def get_headers(self):
        return {'User-Agent': random.choice(user_agent)}

    def save_to_json(self, save_data, first_title, second_title, third_title, page):
        '''
        :param save_data: 要保存的数据  {'first_title':XXXX,
                                        'second_title':xxxx,
                                        'data'[{'third_title':xxxx,'url':xxxxx}]}
        :param first_title: 大类
        :param second_title: 小类
        :return: None
        '''
        print('----------{}_{}_{}_{}-保存-------'.format(first_title, second_title, third_title, page))
        with open('data/index/{}_{}_{}_{}.json'.format(first_title, second_title, third_title, page), 'w',
                  encoding='utf8') as f:
            json.dump(save_data, f, ensure_ascii=False)

    def request_url(self, url):
        res = requests.get(url, headers=self.get_headers(), allow_redirects=False)
        if int(res.status_code) == 200:
            return res.text, pq(res.text)
        else:
            time.sleep(5)
            print('状态码--{}--'.format(str(res.status_code)))
            return 'FLAG',pq(res.text)
if __name__ == '__main__':
    pass