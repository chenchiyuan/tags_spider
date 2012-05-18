# -*- coding: utf-8 -*-
__author__ = 'chenchiyuan'

import os
from pymongo import Connection
import fcntl
#from pymongo import Connection
START = 1500001
END = 1600000
#c = Connection()
#db = c.baike_tags
import codecs
#TODO loads to enable
#c = Connection()
#db = c.tags

class Tag(object):

    def __init__(self, name, num, tags, url, related_items):
        self.name = name
        try:
            self.num = int(num)
        except Exception:
            self.num = int(num.replace(':', ''))
        self.tags = tags
        self.url = url
        self.related_items = related_items

    def save(self):
        #db.tags.insert({'name': self.name, 'num': self.num, 'url': self.url, 'tags': self.tags, 'items': self.related_items})
        tags = '__'.join(self.tags)
        items = '__'.join(self.related_items)
        file = codecs.open("tags_%d_%d" %(START, END), 'a+', 'utf-8')
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(self.name+':::'+str(self.num)+':::'+self.url+':::'+tags+':::'+items+'\n')
        fcntl.flock(file, fcntl.LOCK_UN)
        file.close()


    @classmethod
    def remain_items(cls):
        try:
            file = open("tags_%d_%d" %(START, END), 'r')
        except Exception:
            file = open("tags_%d_%d" %(START, END), 'w')
            file.close()
            file = open("tags_%d_%d" %(START, END), 'r')

        fcntl.flock(file, fcntl.LOCK_UN)
        lines = file.readlines()
        file.close()

        results = []
        for line in lines:
            items = line.split(':::')
            if len(items) > 1:
                results.append(int(items[1]))

        origin = range(START, END+1)
        for r in results:
            origin.remove(r)

        return origin

    def to_mongo(self):
        try:
            db.tags.insert({'name': self.name, 'num': self.num, 'tags': self.tags, 'items': self.related_items})
        except Exception as err:
            print(err)

    @classmethod
    def loads(cls):
        path = '/home/chenchiyuan/projects/spider_baike/baike/'
        files = os.listdir(path)
        for file_name in files:
            if file_name.startswith('tags'):
                file = open(path+file_name, 'r')
                lines = file.readlines()
                file.close()

                i = 0
                for line in lines:
                    i = i + 1
                    num, d = divmod(i, 1000)
                    if d == 0:
                        print("processed %d000\n" % num)
                    cls.load_from_line(line)

    @classmethod
    def load_from_line(cls, line):
        items = line.split(':::')
        name = items[0]
        num = items[1]
        url = items[2]
        tags = items[3]
        relates = items[4]
        tags = tags.split('__')
        relates = relates.replace('\n', '').split('__')
        tag = Tag(name=name, num=num, url=url, tags=tags, related_items=relates)
        tag.to_mongo()