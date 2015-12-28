#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
__author__ = 'vic'

wcg_mysql = dict(host='192.168.3.250',
                 database='wcg',
                 user='pabb',
                 password='pabb')
qjcg_mysql = dict(host='192.168.3.250',
                  database='qjcg',
                  user='pabb',
                  password='pabb')

sn_file = 'sn_csv.csv'

from torndb import Connection

wcg_db = Connection(**wcg_mysql)
qjcg_db = Connection(**qjcg_mysql)


def step1_iccid():
    # step1 export wcg iccid data
    iccids = wcg_db.query("SELECT iccid, id+'999999999' AS mobile FROM t_iccid")
    # import qjcg t_card table
    if iccids and len(iccids) > 0:
        for ic in iccids:
            sql = "insert into `t_card` (`iccid`, `mobile`) values('%s','%s')" \
                  % (ic['iccid'], ic['mobile'])
            try:
                ret = qjcg_db.execute(sql)
                print ret
            except Exception as e:
                print ic, e


def step2_sn_csv():
    # step 2 gen admin import csv file
    sql = "SELECT sn, '' AS pre, IF( hardware = 0 , 'ZJ210', 'ZJ210L') " \
          "AS ter_type FROM t_terminal_info WHERE service_status = 1 AND " \
          "login_time > 0"
    sns = wcg_db.query(sql)
    with open(sn_file, 'w') as f:
        if sns and len(sns):
            print "sn csv begin--------------"
            for sn in sns:
                line = "%s,,%s" % (sn['sn'], sn['ter_type'])
                print line
                f.writelines(line+'\n')

            print "sn csv end----------------"


if __name__ == '__main__':
    # step1_iccid()
    step2_sn_csv()
    pass
