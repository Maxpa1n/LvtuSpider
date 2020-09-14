# coding=utf-8
import json
import os
import random
import time

import requests
from pyquery import PyQuery as pq
from tqdm import tqdm
from utils.header_config import user_agent
from utils.page import get_one_page_index, get_page_number, get_content


class PageSpider(object):
    def __init__(self, base_path, index_file):
        self.index_file = index_file
        self.path = os.path.join(base_path, index_file)

    def get_title(self, ):
        first_title, second_title, third_title, page = self.index_file.replace('.json', '').split('_')
        return first_title, second_title, third_title, page

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
        with open('data/content/{}_{}_{}_{}_content.json'.format(first_title, second_title, third_title, page), 'w',
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

    def pq_page(self, doc):
        return get_content(doc)

    def run(self):
        with open(self.path, 'r', encoding='utf8') as f:
            data = json.load(f)
        first_title, second_title, third_title, page = self.get_title()
        all_data = []
        for i in tqdm(data):
            try:
                question = i['title']
                url = i['url']
                flag, doc = self.request_url(url)
                if flag == 'FLAG':
                    continue
                content = self.pq_page(doc)
                content['question'] = question
                all_data.append(content)
            except:
                print('---------异常-------')
                continue
        self.save_to_json(all_data, first_title, second_title, third_title, page)


if __name__ == '__main__':
    base_path = 'data/index/'
    index_set = os.listdir(base_path)
    for index in index_set:
        a = PageSpider(base_path, index)
        a.run()
