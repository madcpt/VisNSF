import pymysql

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def fetch_journal(apro):
    sql1 = "select paper_journal_name from grant_author where grant_aproval=\'%s\';"%apro
    cursor1.execute(sql1)
    journals = cursor1.fetchall()
    return journals

def fetch_journal_id(journal):
    if is_Chinese(journal):
        return False
    sql2 = "select journal_id from am_journal where name=\'%s\' limit 1;"%journal
    cursor2.execute(sql2)
    journal_id = cursor2.fetchone()
    if not journal_id:
        return False
    return journal_id[0]

def insert_journal_id(journal,journal_id):
    sql3 = "update grant_author set journal_id = %d where paper_journal_name = \'%s\' and  ISNULL(journal_id);"%(journal_id,journal)
    cursor1.execute(sql3)
    print(sql3)

con_engine1 = pymysql.connect(host = '121.36.243.233' ,user = 'mobilenet', password ='aqL79&EAeHrwokc7' , database = 'academic', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()
f = open('apro.txt','r')

def match_journal_id():
    count = 0
    for l in f:
        print('count: ',count)
        count += 1
        if count <= 25742:
            continue
        if count == 100000:
            return
        apro = l.strip('\n')
        journals = fetch_journal(apro)
        for j in journals:
            journal = j[0]
            if not journal:
                continue
            journal_id = fetch_journal_id(journal)
            if not journal_id:
                continue
            insert_journal_id(journal,journal_id)



match_journal_id()





