import requests
import random
import time
import insert
from argparse import ArgumentParser
from itertools import islice
from tqdm import tqdm

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


arg_parser = ArgumentParser()
arg_parser.add_argument('--begin', type=int)
arg_parser.add_argument('--end', type=int)
args = arg_parser.parse_args()

if args.begin is None:
    with open('last.txt', 'r') as f:
        begin, count_line, end = tuple(int(s.rstrip('\n')) for s in f)
else:
    begin = count_line = args.begin
    end = args.end

flag = False
f = open('apro.txt','r')
errs = 0
for count_line, l in tqdm(
    enumerate(islice(f, count_line, end), count_line),
    initial=count_line - begin,
    total=end - begin
):
    try:
        if count_line % 50 == 0:
            time.sleep(1)
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
    except KeyboardInterrupt:
        with open('last.txt', 'w') as f:
            print(begin, count_line, end, sep='\n', file=f)
        break
    except:
        print("Error!  ",errs)
        if errs == 20 and flag:
            break
        errs += 1
        flag = True
        continue
