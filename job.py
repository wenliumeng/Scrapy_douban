# encoding: utf-8
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
import MySQLdb
import MySQLdb.cursors
import re
import datetime
def update():
    div = soup.find('div',id='selected-items').find('dl').find('b').string

    try:
        conn=MySQLdb.connect(host='xxx',user='my_root',passwd='xxx',port=3306)
        cur=conn.cursor() 
        conn.select_db('smartkitchens')
        value=[datetime.datetime.now().strftime("%m-%d"),div,'hi rollen','hi rollen']
        cur.execute('insert into jobs values(%s,%s,%s,%s)',value)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def get_data():
    
    title = datetime.datetime.now().strftime("%m-%d")
    with open('update.txt', 'r') as f:
        time = f.readline()
    if  title == time:
        print 'currently no update', title
        update()
    else:
        with open('update.txt', 'w') as f:
	    f.write(title)
	update()
      
while True:
    if __name__ == '__main__':
        url = 'http://zhaopin.baidu.com/search'
        values={'query':'java','city':'成都'}
        data = urllib.urlencode(values)
        req=urllib2.Request(url,data)
        response=urllib2.urlopen(req)
        html=response.read()
        soup = BeautifulSoup(html, "html.parser")
        get_data()
        time.sleep(86400)
