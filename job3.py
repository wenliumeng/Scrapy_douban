# encoding: utf-8
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import MySQLdb
import MySQLdb.cursors
import re
import datetime

def ergodic(job,city):
    url = 'http://zhaopin.baidu.com/search'
    values={'query':job,'city':city}
    data = urllib.urlencode(values)
    req=urllib2.Request(url,data)
    response=urllib2.urlopen(req)
    html=response.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.find('div',id='selected-items').find('dl').find('b').string

def update(list):
    print(list)
    try:
        conn=MySQLdb.connect(host='xxx',user='my_root',passwd='xxx',port=3306)
        cur=conn.cursor() 
        conn.select_db('smartkitchens')
        value=[datetime.datetime.now().strftime("%m-%d"),list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10],list[11],list[12],list[13],list[14],list[15],list[16],list[17],list[18],list[19],list[20],list[21],list[22],list[23],list[24],list[25],list[26],list[27],list[28],list[29],list[30],list[31],list[32],list[33],list[34],list[35]]
        cur.execute('insert into jobs values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def get_data(job,city):
    l = []
    l.append(ergodic(job,city))
    l.append(ergodic(job,'重庆'))
    l.append(ergodic(job,'西安'))
    l.append(ergodic(job,'北京'))
    l.append(ergodic(job,'深圳'))
    l.append(ergodic(job,'广州'))
    l.append(ergodic(job,'杭州'))
    l.append(ergodic(job,'苏州'))
    l.append(ergodic(job,'昆明'))
    l.append(ergodic(job,'兰州'))
    l.append(ergodic(job,'西宁'))
    l.append(ergodic(job,'曲靖'))
    l.append(ergodic('android','成都'))
    l.append(ergodic('android','重庆'))
    l.append(ergodic('android','西安'))
    l.append(ergodic('android','北京'))
    l.append(ergodic('android','深圳'))
    l.append(ergodic('android','广州'))
    l.append(ergodic('android','杭州'))
    l.append(ergodic('android','苏州'))
    l.append(ergodic('android','昆明'))
    l.append(ergodic('android','兰州'))
    l.append(ergodic('android','西宁'))
    l.append(ergodic('android','曲靖'))
    l.append(ergodic('IOS','成都'))
    l.append(ergodic('IOS','重庆'))
    l.append(ergodic('IOS','西安'))
    l.append(ergodic('IOS','北京'))
    l.append(ergodic('IOS','深圳'))
    l.append(ergodic('IOS','广州'))
    l.append(ergodic('IOS','杭州'))
    l.append(ergodic('IOS','苏州'))
    l.append(ergodic('IOS','昆明'))
    l.append(ergodic('IOS','兰州'))
    l.append(ergodic('IOS','西宁'))
    l.append(ergodic('IOS','曲靖'))
    update(l)
      

if __name__ == '__main__':
    get_data('java','成都')
