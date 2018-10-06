import requests
import time
import traceback
from multiprocessing.pool import ThreadPool
from db.mongo_db import MongoDB
from requests.exceptions import ProxyError, ConnectTimeout

class Validate(object):

    def valid_many(self, proxy_list, method):
        pool = ThreadPool(16)
        for proxy in proxy_list:
            pool.apply_async(self.valid_one, args=(proxy,method))

        pool.close()
        pool.join()

    def valid_one(self, proxy, method, url='https://baidu.com'):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        proxies = {
            'http': 'http://' + proxy['proxy'],
            'https': 'http://' + proxy['proxy']
        }
        try:
            start_time = time.time()
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=8)
            delay = round(time.time() - start_time, 2)  # round()方法返回浮点数x的四舍五入值
            if resp.status_code == 200:
                proxy['delay'] = delay
                if method == 'insert':

                    MongoDB().insert(proxy)
                elif method == 'check':
                    MongoDB().update({'proxy': proxy['proxy']}, {'delay': proxy['delay']})

            else:
                print("无效ip:{}".format(proxy))
                if method == 'check':
                    MongoDB().delete({'proxy': proxy['proxy']})
        except (ProxyError, ConnectTimeout):
            print("无效ip:{}".format(proxy))
            if method == 'check':
                MongoDB().delete({'proxy': proxy['proxy']})

        except:
            pass
