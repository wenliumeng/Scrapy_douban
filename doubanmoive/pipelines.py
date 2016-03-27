# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from doubanmoive import settings
import os
#coding：UTF-8
import urllib
import urllib2
import time
import os
import shutil
from scrapy.exceptions import DropItem
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors

class DoubanmoivePipeline(object):
    def __init__(self):
        if os.path.exists('newbook'):
            shutil.rmtree("newbook")
            os.mkdir("newbook")
        else:
            os.mkdir("newbook")
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'mydb',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        if item['images']:
            # 遍历每个页面item集合里面的所有url
            # 字符串判断，过滤所有.jpg和.png文件，只下载gif文件
            # 将url插入mongo数据库
            # 将url存放进txt，稍后可以用迅雷下载
            # a="http://img4.douban.com/mpic/s28265739.jpg"
            # urllib.urlretrieve(a,'D:\WEB\Python\doubanmoive\newbook\%s' % a.rsplit('/')[4])
            # for j in item['name']:
            #     f = open('D:\WEB\Python\doubanmoive\Log.txt','a')
            #     f.write(j)
            #     f.write(item['name'])
            #     f.write('\n')
            #     f.close()
            for i in item['images']:
                print("===================================")
                print(i)
                i=i.replace('mpic','lpic')
                print(i)
                print("===================================")
                if ".jpg" in i:
                    urllib.urlretrieve(i,'D:/WEB/Python/doubanmoive/newbook/%s' %i.rsplit('/')[4])
        else:
            raise DropItem(item)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute("select * from newbook where name= %s", (item['name'][0],))
        result = tx.fetchone()
        log.msg(result, level=log.DEBUG)
        print result
        if result:
            log.msg("Item already stored in db:%s" % item, level=log.DEBUG)
        else:
            tx.execute(\
                "insert into newbook (name,author,publisher,publisher_year,content,original_name,translator,page_number,price,binding,series,ISBN,score,evaluate_number,one_star,two_star,three_star,four_star,five_star) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                ('未知' if len(item['name']) == 0 else item['name'][0], '未知' if len(item['author']) == 0 else item['author'][0], '未知' if len(item['publisher']) == 0 else item['publisher'][0], '未知' if len(item['publisher_year']) == 0 else item['publisher_year'][0],' ','未知' if len(item['original_name']) == 0 else item['original_name'][0],'未知' if len(item['translator']) == 0 else item['translator'][0],'未知' if len(item['page_number']) == 0 else item['page_number'][0],'未知' if len(item['price']) == 0 else item['price'][0],'未知' if len(item['binding']) == 0 else item['binding'][0],'未知' if len(item['series']) == 0 else item['series'][0],'未知' if len(item['ISBN']) == 0 else item['ISBN'][0],'未知' if len(item['score']) == 0 else item['score'][0],'未知' if len(item['evaluate_number']) == 0 else item['evaluate_number'][0],'未知' if len(item['one_star']) == 0 else item['one_star'][0],'未知' if len(item['two_star']) == 0 else item['two_star'][0],'未知' if len(item['three_star']) == 0 else item['three_star'][0],'未知' if len(item['four_star']) == 0 else item['four_star'][0],'未知' if len(item['five_star']) == 0 else item['five_star'][0]))
                #('name','year','score','director','d','s','s','s','s','s','s','s','s','s','s','s','s','s','s'))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

    def close_spider(self,spider):
        print("end")

class DoubanmoivePipeline1(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'mydb',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self,tx,item):
        tx.execute("select * from doubanmoive where name= %s",(item['name'][0],))
        result=tx.fetchone()
        log.msg(result,level=log.DEBUG)
        print result
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            classification=actor=''
            lenClassification=len(item['classification'])
            lenActor=len(item['actor'])
            for n in xrange(lenClassification):
                classification+=item['classification'][n]
                if n<lenClassification-1:
                    classification+='/'
            for n in xrange(lenActor):
                actor+=item['actor'][n]
                if n<lenActor-1:
                    actor+='/'

            tx.execute(\
                "insert into doubanmoive (name,year,score,director,classification,actor) values (%s,%s,%s,%s,%s,%s)",\
                (item['name'][0],item['year'][0],item['score'][0],item['director'][0],classification,actor))
                #('name','year','score','director','d','s'))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)