def get_content(doc):
    '''
    获取页面内容
    :param doc:pq的类  doc = pq(text)
    :return:  {'strong': 问题列表,
                'content_index': 问题列表对应答案,
                'content_list': 所有文本，
                'daodu':导读 一般面向标题问题}
    '''
    strong = doc('div.detail-conts p strong').text().split()
    content_index = []
    content = doc('div.detail-conts p').text().split()
    daodu = doc('div.mt30.p20.lh22.s_c6.bg_f5').text()
    for i in range(len(strong) - 1):
        content_index.append((content.index(strong[i]), content.index(strong[i + 1])))
    content_index.append((content.index(strong[i + 1]), len(content)))
    if len(strong) == len(content_index):
        return {'strong': strong, 'content_index': content_index, 'content_list': content, 'daodu': daodu}
    else:
        return ''


def get_one_page_index(doc):
    '''
    :param doc: doc = pq(text)
    :return:  clas :种类
            title_and_url: {url:问题的URL,title:问题的内容}
    '''
    clas = doc('h2.f30.fb.fl').text()
    base_url = 'http://www.64365.com/'
    title_and_url = []
    for i in doc('div.tit.ect.fb').items():
        url = i('a').attr('href')
        title = i.text()
        title_and_url.append({'url': base_url + url, 'title': title})

    return clas, title_and_url


def get_page_number(doc):
    num = doc('div.page-bar.tc.mt20 a')[-2].text

    return int(num)
