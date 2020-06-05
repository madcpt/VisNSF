import pymysql
import time
from pypinyin import lazy_pinyin

def CtoE(name):
    namelist = lazy_pinyin(name)
    xing = namelist[0]
    minglist = namelist[1:]
    ming = ''
    for i in minglist:
        ming = ming + i
    Ename = ming + ' ' + xing
    Ename = Ename.title().lstrip()
    return Ename

con_engine1 = pymysql.connect(host = 'localhost' ,user = 'root', password ='cjz122530' , database = '学者', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'NSF_CN', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()
f = open('apro.txt','r')


def fetch_admin_name(apro):
    sql1 = "select projectManager from nsfc_conclusion where approvalNumber=\'%s\' limit 1;"%str(apro)
    print(sql1)
    cursor2.execute(sql1)
    admin_name = cursor2.fetchone()
    return admin_name

def fetch_admin_id(admin_name):
    sql2 = "select author_id from grant_author where author_name=\'%s\' limit 1;"%CtoE(admin_name)
    print(sql2)
    cursor1.execute(sql2)
    admin_id = cursor1.fetchone()
    print(admin_id)
    return admin_id[0]

def insert(admin_id,apro):
    sql3 = "update cn_nnsf_grants set principal_id=\'%s\' where approval_number=\'%s\';"%(admin_id,apro)
    print(sql3)
    cursor1.execute(sql3)



def do():
    count = 0
    cnt = 0
    for l in f:
        try:
            print('count: ',count)
            count += 1
            if count == 4700:
                return

            apro = int(l.strip('\n'))
            name = fetch_admin_name(apro)
            id = fetch_admin_id(name)
            insert(id,apro)
            cnt += 1
            print('cnt ',cnt)

        except:
            continue

do()
