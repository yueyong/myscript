#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
ter_file = 'ter_file.csv'

from torndb import Connection
import os

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
          "AS ter_type, IF (vin IS NULL OR vin = '', sn, vin) " \
          "AS vin, IF (alias IS NOT NULL, alias, '') " \
          "AS cnum FROM t_terminal_info WHERE service_status = 1 AND " \
          "login_time > 0"
    sns = wcg_db.query(sql)
    with open(ter_file, 'w') as ter_f:
        with open(sn_file, 'w') as f:
            if sns and len(sns):
                print "sn csv begin--------------"
                lines = []
                ter_lines = []
                for sn in sns:
                    line = "%s,,%s" % (sn['sn'], sn['ter_type'])
                    print line
                    lines.append(line+'\n')
                    ter_line = "%s,%s,%s" % (sn['sn'], sn['vin'], sn['cnum'])
                    print(ter_line)
                    ter_lines.append(ter_line+'\n')
                f.writelines(lines)
                ter_f.writelines(ter_lines)
                print "sn csv end----------------"


def step3_car_ter_excel():
    if os.path.exists(ter_file):
        with open(ter_file) as f:
            lines = []
            for ter_line in f:
                ters = ter_line.split(",")
                sn = ters[0]
                vin = ters[1]
                cnum = ters[2]
                sql = "SELECT activate_code as ac from t_sn where sn = '%s'" \
                      % sn
                ac_code = qjcg_db.get(sql)
                print 'activate code : %s' % ac_code
                if ac_code:
                    ac = ac_code['ac']
                    line = "%s,%s,%s" % (ac, vin, cnum)
                    lines.append(line)
            with open('import_car_ter.csv', 'w') as ct_f:
                ct_f.writelines(lines)


if __name__ == '__main__':
    step1_iccid()
    # step2_sn_csv()
    # step3_car_ter_excel()
    pass
