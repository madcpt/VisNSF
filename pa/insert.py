import pymysql
#import search

log_f = open('search-log.tsv', 'a')


def insert_journal_conf(aproval,journal,conf,paper):
    con_engine = pymysql.connect(host = '121.36.243.233' ,user = 'mobilenet', password ='aqL79&EAeHrwokc7' , database = 'academic', port=3306, charset = 'utf8',autocommit =True)
    cursor = con_engine.cursor()
    sql = "insert into grant_author(grant_aproval,paper_journal_name,paper_conference,paper_name) values(%d,\'%s\',\'%s\',\'%s\')"%(int(aproval),journal,conf,paper)
    cursor.execute(sql)
    print(aproval, journal, conf, paper, sep='\t', file=log_f)

#insert_journal_conf('11290163','Chin. J. Chem.','')
