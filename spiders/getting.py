import chardet
import requests
import traceback
import time


class Downloader(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

    def downloader(self, url, parse_rule):
        '''
        下载器
        :param parse_rule: config.py中的爬虫规则
        :return: resp.text
        '''
        print('正在下载页面：{}'.format(url))
        try:
            resp = requests.get(url, headers=self.headers)
            resp.encoding = chardet.detect(resp.content)['encoding']
            if parse_rule.get('delay'):
                time.sleep(parse_rule.get('delay'))
            if resp.status_code == 200:
                return resp.text
            else:
                raise ConnectionError

        except :
            traceback.print_exc()  # 异常处理模块
            print('页面请求失败{}'.format(url))

