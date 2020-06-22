import pymysql
import time
import sys
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

con_engine1 = pymysql.connect(host = '121.36.243.233' ,user = 'mobilenet', password ='aqL79&EAeHrwokc7' , database = 'academic', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()
con_engine3 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'NSF_CN', port = 13307, charset = 'utf8')
cursor3 = con_engine3.cursor()
f = open('apro.txt','r')

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def fetch_journals_papers(apro):
    sql1 = "select journal_id,paper_name from grant_author where grant_aproval=%d;"%apro
    cursor1.execute(sql1)
    journals_papers = cursor1.fetchall()
    return journals_papers


def find2(paper,journal_id):
    sql2 = "select paper_id from am_paper where journal_id=%d and title=\'%s\' limit 1;"%(journal_id,paper)
    #print(sql2)
    cursor2.execute(sql2)
    return cursor2.fetchone()[0]

def insertID(paper_id,paper):
    sql3 = "update grant_author set paper_id=%d where paper_name=\'%s\';"%(paper_id,paper)
    cursor1.execute(sql3)
    print(sql3)

def fetch_author_id(paper_id):
    sql2 = "select author_id from am_paper_author where paper_id=%d;"%paper_id
    cursor2.execute(sql2)
    author_ids = cursor2.fetchall()
    return author_ids

def insert_author_id(author_id,paper_id):
    sql3 = "update grant_author set author_id=%d where paper_id=%d and ISNULL(author_id) limit 1;"%(author_id,paper_id)
    cursor1.execute(sql3)
    print(sql3)

def fetch_author_name(author_id):
    sql3 = "select name from am_author where author_id=%d limit 1;"%author_id
    #print(sql3)
    cursor2.execute(sql3)
    author_name = cursor2.fetchone()
    return author_name

def insert_author_name(author_name,author_id):
    sql4 = "update grant_author set author_name=\'%s\' where author_id=%d and ISNULL(author_name);"%(author_name,author_id)
    print(sql4)
    cursor1.execute(sql4)

def fetch_admin_name(apro):
    sql1 = "select projectManager from nsfc_conclusion where approvalNumber=\'%d\';"%apro
    #print(sql1)
    cursor3.execute(sql1)
    admin_name = cursor3.fetchone()[0]
    return admin_name

def fetch_admin_id(admin_name):
    sql2 = "select author_id from nsfc_conclusion where author_name=\'%s\' limit 1;"%admin_name
    #print(sql2)
    cursor1.execute(sql2)
    admin_id = cursor1.fetchone()
    #print(admin_id)
    return admin_id[0]

def insert_admin_id(admin_id,apro):
    sql3 = "update cn_nnsf_grants set principal_id=%d where approval_number=\'%d\';"%(admin_id,apro)
    print(sql3)
    cursor1.execute(sql3)

def judge(name):
    sql_judge = "select count(*) from nsfc_conclusion where instr(projectManager,\'%s\') limit 1;"%name
    cursor3.execute(sql_judge)
    j = cursor2.fetchone()[0]
    return j

def getPaperid():
    count = 0
    for l in f:
        flag = False
        print('count: ',count)
        count += 1
        if count <= 32671:
            continue
        if count == 100000:
            return
        try:
            apro = int(l.strip('\n'))
            journals = fetch_journals_papers(apro)
            Authors = set()
            Papers = set()
            prin = CtoE(fetch_admin_name(apro))
            print(apro,'----',prin)
        except:
            continue
        for j in journals:
            journal_id = j[0]
            paper = j[1]
            paper_id = 0
            try:
                if not journal_id:
                    continue
                else:
                    paper_id = find2(paper,journal_id)
                    if paper_id in Papers:
                        continue
                    Papers.add(paper_id)
                    author_ids = fetch_author_id(paper_id)
            except:
                continue
            for id in author_ids:
                try:
                    authorid = id[0]
                    if authorid in Authors:
                        continue
                    Authors.add(authorid)
                    author_name = fetch_author_name(authorid)[0]
                    if author_name != prin:
                        continue
                    insert_admin_id(authorid,apro)
                    flag = True
                    break
                except:
                    continue


            if flag:
                print(apro,'completes')
                break



getPaperid()





