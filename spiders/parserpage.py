from lxml import etree
import traceback
import re


class Parser(object):
    def parser(self, response, spider_rule):
        '''
        解析器，根据config.py中的'type'选择解析方式
        :return proxy_list
        '''
        if spider_rule['type'] == 'xpath':
            return self.xpath_parser(response, spider_rule)
        elif spider_rule['type'] == 're':
            return self.re_parser(response, spider_rule)
        else:
            print('{}此种解析方法未开发'.format(spider_rule['type']))

    def xpath_parser(self, response, spider_rule):
        try:
            page = etree.HTML(response)
            tags = page.xpath(spider_rule['node'])
            # print(tags)
            proxy_list = []
            for tag in tags[2:]:
                ip = tag.xpath(spider_rule['target']['ip'])[0]
                port = tag.xpath(spider_rule['target']['port'])[0]
                proxy = {
                    'proxy': ip + ':' + port
                }
                proxy_list.append(proxy)
            return proxy_list
        except Exception as e:
            print(e)
            # traceback.print_exc()
            print('解析IP地址出错')

    def re_parser(self, resp, parse_rule):
        try:
            trs = re.findall(parse_rule['pattern'], resp, re.S)
            proxy_list = []
            for tr in trs[1:]:
                ip = re.findall(parse_rule['target']['ip'], tr)[0]
                port = re.findall(parse_rule['target']['port'], tr)[0]
                proxy = {
                    'proxy': ip + ':' + port
                }
                proxy_list.append(proxy)
            return proxy_list
        except Exception as e:
            print(e)
            print('解析IP地址出错')
            # traceback.print_exc()

