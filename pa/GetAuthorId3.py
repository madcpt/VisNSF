import pymysql


con_engine1 = pymysql.connect(host = 'localhost' ,user = 'root', password ='cjz122530' , database = '学者', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()
con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
cursor2 = con_engine2.cursor()
f = open('apro.txt','r')

def fetch_apro(apro):
    sql1 = "select paper_id from grant_author where grant_aproval=\'%s\';"%apro
    cursor1.execute(sql1)
    paper_ids = cursor1.fetchall()
    return paper_ids

def fetch_author_id(paper_id):
    sql2 = "select author_id from am_paper_author where paper_id=%d;"%paper_id
    cursor2.execute(sql2)
    author_ids = cursor2.fetchall()
    return author_ids

def insert_author_id(author_id,paper_id):
    sql3 = "update grant_author set author_id=%d where paper_id=%d and ISNULL(author_id) limit 1;"%(author_id,paper_id)
    cursor1.execute(sql3)
    print(sql3)

def getAuthorId():
    count = 0
    for l in f:
        print('count: ',count)
        count += 1
        if count <= 2400:
            continue
        if count == 4770:
            return
        apro = l.strip('\n')
        paper_ids = fetch_apro(apro)
        for i in paper_ids:
            try:
                author_ids = fetch_author_id(i[0])
                for j in author_ids:
                    insert_author_id(j[0],i[0])
            except:
                continue

getAuthorId()
