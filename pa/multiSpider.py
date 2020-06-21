import threading
from queue import Queue
import requests
import insert
import sys
import time
requests.DEFAULT_RETRIES = 5
class NSFC_API:
    base_url1 = 'http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/'
    base_url2 = 'http://output.nsfc.gov.cn/baseQuery/data/resultsInfoData/'
    proxyHost = "dyn.horocn.com"
    proxyPort = "50000"

    # 代理隧道验证信息
    proxyUser = "E9DB1668647178213852"
    proxyPass = "p99PCN8B4mDi"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxy = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Connection': 'close' }
    def query1(self, approval_num):
        r = requests.get(self.base_url1 + str(approval_num),proxies=self.proxy,headers=self.headers)
        #print(r.content.decode())
        #print('-----------------',approval_num)
        raw_data = r.json()['data']

        return self.__parse_raw_data(raw_data)

    def query2(self, acheivement_id):
        r = requests.get(self.base_url2 + str(acheivement_id),proxies=self.proxy,headers=self.headers)
        #print(r.content.decode())
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
threadLock = threading.Lock()
def paper_acheiment_id(aprovalnum):
    results = api.query1(aprovalnum)
    if not results:
        return False
    papers = []
    for i in results:
        papers.append((i['acheivementid'],i['title']))
    return papers

class threadSpider(threading.Thread):
    def __init__(self, id, appro=0, tmp=0):
        threading.Thread.__init__(self)
        self.id = id
        self.appro = appro
        self.tmp = tmp
    def run(self):
        global cnt
        while not workQueue.empty():
            try:
                threadLock.acquire()
                self.appro= workQueue.get()
                print(self.id, ' starts ', cnt)
                print(self.appro)
                self.tmp = cnt
                cnt += 1
                threadLock.release()
                achievement_ids = paper_acheiment_id(self.appro)
                if not achievement_ids:
                    return
                for i in achievement_ids:
                    journal_conf = api.query2(i[0])  # 请求paper
                    insert.insert_journal_conf(self.appro, journal_conf['journal'], journal_conf['conf'], i[1])
                    time.sleep(0.005)
                time.sleep(0.005)
                print(self.id, ' ends ', self.tmp)
            except :
                print("Unexpected error:", sys.exc_info())
                print('error occurs in', self.tmp)
                break
                #continue

f = open('apro.txt','r')
cnt = int(sys.argv[1])
end = int(sys.argv[2])
workQueue = Queue(30)
threads=[]

for i in range(cnt):
    f.readline()
for i in range(30):
    l = f.readline()
    aproval = l.strip('\n')
    workQueue.put(aproval)
for i in range(20):
    threads.append(threadSpider(i))
    time.sleep(0.1)

for spider in threads:
    spider.start()


while cnt <= end:
    l = f.readline()
    aproval = l.strip('\n')
    workQueue.put(aproval)





