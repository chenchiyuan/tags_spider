# -*- coding: utf-8 -*-
__author__ = 'chenchiyuan'

import fcntl
#from pymongo import Connection
START = 200001
END = 300000
#
#c = Connection()
#db = c.baike_tags
import codecs

class Tag(object):

    def __init__(self, name, num, tags, url, related_items):
        self.name = name
        self.num = num
        self.tags = tags
        self.url = url
        self.related_items = related_items

    def save(self):
        #db.tags.insert({'name': self.name, 'num': self.num, 'url': self.url, 'tags': self.tags, 'items': self.related_items})
        tags = '__'.join(self.tags)
        items = '__'.join(self.related_items)
        file = codecs.open("tags_%d_%d" %(START, END), 'a+', 'utf-8')
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(self.name+':::'+self.num+':::'+self.url+':::'+tags+':::'+items+'\n')
        file.close()
        fcntl.flock(file, fcntl.LOCK_UN)

    @classmethod
    def remain_items(cls):
        file = open("tags_%d_%d" %(START, END), 'r')
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