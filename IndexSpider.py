import json
import random
import time

import requests
from pyquery import PyQuery as pq
from tqdm import tqdm
from utils.header_config import user_agent
from utils.page import get_one_page_index, get_page_number


class LvtuIndexSpider(object):
    '''
    爬网页索引
    '''

    def __init__(self, first_title, second_title_url_dic):
        '''

        :param first_title: 大类
        :param second_title_url_dic: 小类 {}
        '''
        self.first_title = first_title
        self.second_title_url_dic = second_title_url_dic
        self.save_flag = 1

    def get_headers(self):
        return {'User-Agent': random.choice(user_agent)}

    def save_to_json(self, save_data, first_title, second_title, third_title, page):
        '''
        :param save_data: 要保存的数据  {'first_title':XXXX,
                                        'second_title':xxxx,
                                        'data'[{'third_title':xxxx,'url':xxxxx}]}
        :param first_title: 大类
        :param second_title: 小类
        :return:
        '''
        print('----------{}_{}_{}_{}-保存-------'.format(first_title, second_title, third_title, page))
        with open('data/{}_{}_{}_{}.json'.format(first_title, second_title, third_title, page), 'w',
                  encoding='utf8') as f:
            json.dump(save_data, f, ensure_ascii=False)

    def request_url(self, url):
        res = requests.get(url, headers=self.get_headers())
        if int(res.status_code) == 200:
            return res.text, pq(res.text)
        else:
            print('状态码--{}--'.format(str(res.status_code)))
            return ''

    def pq_page(self, doc):
        return get_one_page_index(doc)

    def get_page_number(self, doc):
        return get_page_number(doc)

    def run(self):
        for sub_tit_url in self.second_title_url_dic:
            second_tit = sub_tit_url['second_title']
            base_url = sub_tit_url['url']
            _, doc = self.request_url(base_url)
            page_num = self.get_page_number(doc)
            all_index_data = []
            start_page = 1
            print('----------{}-{}--正常爬-------'.format(self.first_title, second_tit))
            for page in tqdm(range(start_page, int(page_num) + 1)):
                time.sleep(0.8)
                url = base_url + str(page) + '/'
                _, doc = self.request_url(url)
                third_title, index_data = self.pq_page(doc)
                all_index_data.extend(index_data)
                if page % 100 == 0:
                    self.save_to_json(all_index_data, self.first_title, second_tit, third_title, page)
                    all_index_data = []


if __name__ == '__main__':
    with open('data/spider_map.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    for i in data:
        first = list(i.keys())[0]
        sec = i[first]
        index_spider = LvtuIndexSpider(first, sec)
        index_spider.run()
