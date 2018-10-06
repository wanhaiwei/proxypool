import pymongo
from pymongo.errors import DuplicateKeyError


class MongoDB(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=4567)
        self.db = self.client['proxypool']
        self.proxies = self.db['proxies']
        self.proxies.ensure_index('proxy', unique=True)

    def insert(self, proxy):
        try:
            self.proxies.insert(proxy)
            print('插入成功：{}'.format(proxy))
        except DuplicateKeyError:
            pass

    def delete(self, conditions):
        self.proxies.remove(conditions)
        print('删除成功：{}'.format(conditions))

    def update(self, conditions, values):
        self.proxies.update(conditions, {"$set": values})
        print('更新成功：{},{}'.format(conditions, values))

    def get(self, count, conditions=None):
        conditions = conditions if conditions else {}
        count = int(count)
        items = self.proxies.find(conditions)
        # items = self.proxies.find(conditions, limit=count).sort('delay', pymongo.ASCENDING)
        items = list(items)
        return items

    def get_count(self):
        return self.proxies.count({})


if __name__ == '__main__':
    m = MongoDB()
    print(m.get(3))
