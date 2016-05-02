# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
import logging
import sys

class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('../cnblogs.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
            unix_socket='/tmp/mysql.sock'
        )
        try:
            dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        except:
            traceback.print_exc()
            raise
        return cls(dbpool)
    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
            d.addErrback(self._handle_error, item, spider)
            d.addBoth(lambda _: item)
        except:
            logging.log(logging.INFO, 'wright to db error : ' + traceback.print_exc())
        return d
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        linkmd5id = self._get_linkmd5id(item)
        #print linkmd5id
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from cd_cnblogs where item_id = %s
        """, (linkmd5id, ))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update cd_cnblogs set title = %s, description = %s, modify_time = %s,view_count = %s, comment_count = %s where item_id = %s
            """, (item['title'], item['desc'], now,item['view_count'], item['comment_count'], linkmd5id))

            logging.log(logging.INFO, 'Update Success : ' + item['title'])

        else:
            conn.execute("""
            insert into cd_cnblogs (item_id, title, description, link, list_url, create_time, post_time, post_author, view_count, comment_count)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (linkmd5id, item['title'], item['desc'], item['link'], item['list_url'], now, item['post_time'], item['post_author'], item['view_count'],item['comment_count']))

            logging.log(logging.INFO, 'Insert Success : ' + item['title'])

            #print """
            #    insert into cd_cnblogs(item_id, title, desc, link, list_url, create_time)
            #    values(%s, %s, %s, %s, %s, %s)
            #""", (linkmd5id, item['title'], item['desc'], item['link'], item['list_url'], now)

    #获取url的md5编码
    def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()
    #异常处理
    def _handle_error(self, failue, item, spider):
        logging.log(logging.INFO, failue)
