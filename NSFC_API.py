import requests


class NSFC_API:
    """An API to fetch all papers published under some grant in NSFC.

    Attributes:
        approval_num: An integer indicating the approval number of grant to query.
    """
    
    base_url = 'http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/'

    def query(self, approval_num):
        r = requests.get(self.base_url + str(approval_num))
        raw_data = r.json()['data']
        
        return self.__parse_raw_data(raw_data)

    @staticmethod
    def __parse_raw_data(raw_data):
        result_list = raw_data['resultsList']
        results = [
            {
                'title': result['result'][2], 
                'type': result['result'][3],
                'authors': result['result'][4].rstrip('|').split('|')
            } 
            for result in result_list
        ]

        return results

if __name__ == "__main__":
    api = NSFC_API()
    results = api.query(10001011)

    for result in results:
        print(result)
