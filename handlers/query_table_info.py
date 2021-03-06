# -*- coding: UTF-8 -*-
# Date: 2018-12-29
# Author: tang
#
import json
from request_base_handler import BaseHandler
import sys
sys.path.append("..")
from logger_file import logger

# Request: post
# Params:
# {
#     "type":"oracle",
#     "host":"172.16.90.252",
#     "port":1521,
#     "user":"yi_bo",
#     "passwd":"yi_bo",
#     "dbname":"orcl",
#     "charset":"utf-8",
#     "src_table":"TEST_TABLE",
#     "dest_table":"my_test_table"
# }
#
class QueryTableInfoHandler(BaseHandler):

    def get(self):
        self.response_json(None, -1, 'Not implements')

    def post(self):
        logger.info("request remote client id is %s ..." % self.request.remote_ip)

        if self.request.body is None or len(self.request.body) == 0:
            self.response_json(None, -1, 'Invalid param!')

        logger.info("[Request]:%s" % self.request.body)

        try:
            params = json.loads(self.request.body)
            self.query_table_info(**params)
        except Exception, e:
            self.response_json(None, -1, 'error:%s' % e.message)
        finally:
            pass

    def query_table_info(self, type, host, port, user, passwd, dbname, charset, src_table, dest_table):

        if not BaseHandler.dbmapper.has_key(type):
            self.response_json(None, -1, 'Not Support databse type :%s' % type)

        dbclass = BaseHandler.dbmapper.get(type)
        reader = dbclass(
            host=host,
            port=port,
            dbname=dbname,
            username=user,
            password=passwd,
            charset=charset
        )
        reader.connect()
        ret, create_table_sql, columns_names, key_columns_names = reader.get_mysql_create_table_sql(src_table,
                                                                                                    dest_table, True)
        reader.close()

        if ret is not True:
            self.response_json(None, -1, "failed,reason:%s" % create_table_sql)

        result = {}
        result['create_sql'] = create_table_sql
        result['columns'] = columns_names
        result['primary_key'] = key_columns_names
        self.response_json(result)
