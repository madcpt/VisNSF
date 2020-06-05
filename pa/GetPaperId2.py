import pymysql
import time

con_engine1 = pymysql.connect(host = 'localhost' ,user = 'root', password ='cjz122530' , database = '学者', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()
f = open('apro.txt','r')

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def fetch_journals_papers(apro):
    sql1 = "select journal_id,paper_name from grant_author where grant_aproval=\'%s\';"%apro
    cursor1.execute(sql1)
    journals_papers = cursor1.fetchall()
    return journals_papers

def find1(paper):
    sql1 = "select paper_id from am_paper where title=\'%s\' limit 1;"%paper
    print(sql1)
    cursor2.execute(sql1)
    return cursor2.fetchone()[0]

def find2(paper,journal_id):
    sql2 = "select paper_id from (select paper_id,title from am_paper where journal_id=%d) as t where title=\'%s\' limit 1; "%(journal_id,paper)
    print(sql2)
    cursor2.execute(sql2)
    return cursor2.fetchone()[0]

def insertID(paper_id,paper):
    sql3 = "update grant_author set paper_id=%d where paper_name=\'%s\';"%(paper_id,paper)
    cursor1.execute(sql3)
    print(sql3)

def getPaperid():
    count = 0
    for l in f:
        print('count: ',count)
        count += 1
        if count <= 2400:
            continue
        if count == 4770:
            return
        apro = l.strip('\n')
        journals = fetch_journals_papers(apro)
        for j in journals:
            journal_id = j[0]
            paper = j[1]
            paper_id = 0
            try:
                if not journal_id:
                    continue
                else:
                    paper_id = find2(paper,journal_id)
            except:
                continue
            insertID(paper_id,paper)


getPaperid()





