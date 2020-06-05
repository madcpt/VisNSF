
import pymysql
import requests
import random
import time
import insert

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
def get_headers():
    user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

class NSFC_API:
    base_url1 = 'http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/'
    base_url2 = 'http://output.nsfc.gov.cn/baseQuery/data/resultsInfoData/'
    proxies = {'http':'http://10.10.10.10:80','https':'https://10.10.10.10:8765'}
    def query1(self, approval_num):
        r = requests.get(self.base_url1 + str(approval_num),headers=get_headers())
        raw_data = r.json()['data']
        return self.__parse_raw_data(raw_data)

    def query2(self, acheivement_id):
        r = requests.get(self.base_url2 + str(acheivement_id),headers=get_headers())
        raw_data = r.json()['data']
        return {'conf':raw_data['conferenceName'],'journal':raw_data['journalName']}

    @staticmethod
    def __parse_raw_data(raw_data):
        result_list = raw_data['resultsList']
        results = [
            {
                'title': result['result'][2],
                'acheivementid': result['result'][1],
                'authors': result['result'][4].rstrip('|').split('|')
            }
            for result in result_list
        ]

        return results


api = NSFC_API()

def paper_acheiment_id(aprovalnum):
    results = api.query1(aprovalnum)
    if not results:
        return False
    papers = []
    for i in results:
        papers.append((i['acheivementid'],i['title']))
    return papers

"""def paperId(papers):
    con_engine2 = pymysql.connect(host = '202.120.36.29', user = 'mobilenet', password = 'mobilenet', database = 'am_paper', port = 13307, charset = 'utf8')
    cursor2 = con_engine2.cursor()
    for i in papers:
        length = len(i)
        if length < 160:
            sql = "select paper_id from am_paper where title = \'" + i + "\' limit 1;"
        else:
            sql = "select paper_id from am_paper where locate(\'" + i[int(0.94*length):] + "\',title) = " + str(int(0.9*length)) + " limit 1;"
        print(sql)
        cursor2.execute(sql)
        ids = cursor2.fetchall()
        for id in ids:
            print(id)"""


f = open('apro.txt','r')
countline = 0
count = 0
errs = 0
flag = False
for l in f:
    if countline <  121046:
        countline += 1
        continue
    print('line: ',countline) #爬到第几行了（即第几个grant），下次再开始就修改第72行的数值
    countline += 1
    count += 1
    try:
        if count == 50:
            time.sleep(1)
            count = 0
        time.sleep(0.01)
        aproval = l.strip('\n')
        if not is_number(aproval):
            continue
        t = paper_acheiment_id(aproval)#用项目批准号获取paper的信息
        if not t:
            continue
        for i in t:
            time.sleep(0.01)
            journal_conf = api.query2(i[0])#请求paper
            insert.insert_journal_conf(aproval,journal_conf['journal'],journal_conf['conf'],i[1])#插数据库的操作，不用数据库就注释掉insert模块
            flag = False
            errs = 0
    except:
        print("Error!  ",errs)
        if errs == 20 and flag:
            break
        errs += 1
        flag = True
        continue
