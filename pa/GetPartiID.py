import pymysql
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
cursor3 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()

sql1 = "select participant_name from cn_nnsf_grants_participants;" #1389
cursor1.execute(sql1)

def fetch_parid(parname):
    Ename = CtoE(parname)
    sql2 = "select author_id from grant_author where author_name=\'%s\' limit 1;"%Ename
    cursor3.execute(sql2)
    print(sql2)
    id = cursor3.fetchone()
    return id

def insert_id(parid,parname):
    sql3 = "update cn_nnsf_grants_participants set participant_id=%d where participant_name=\'%s\' limit 1;"%(parid,parname)
    cursor3.execute(sql3)
    print(sql3)

def getPartiID():
    for i in range(1389):
        try:
            parname = cursor1.fetchone()[0]
            parid = fetch_parid(parname)[0]
            insert_id(int(parid),parname)
        except:
            continue
getPartiID()
