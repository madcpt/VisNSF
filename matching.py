import json
import re
import MySQLdb
from tqdm import tqdm

DEBUG = False

conn = MySQLdb.connect(
    host='202.120.36.29', port=13307, user='mobilenet', passwd='mobilenet',
    db='am_paper', charset='utf8mb4'
)
local_conn = MySQLdb.connect(
    host='localhost', user='root', passwd='xxxx', db='academic',
    charset='utf8mb4'
)

# {
#     "result": "true",
#     "ratifyNo": "U1533134",
#     "projectAdmin": "355359",
#     "participants": [
#         [
#             "100883549",
#             "u82aeu5c11u77f3",
#             "u535au58ebu751f",
#             "",
#             "u6e05u534eu5927u5b66"
#         ],
#         [
#             "pj3b19cf73ecf0ae10901d7cb93cf135e3",
#             "u82cfu8d8a",
#             "u535au58ebu751f",
#             "",
#             "u6e05u534eu5927u5b66"
#         ],
#         [
#             "pjb1e01426fccff494f512947b72e44940",
#             "u5468u5ddd",
#             "u7855u58ebu751f",
#             "",
#             "u6e05u534eu5927u5b66"
#         ],
#         [
#             "pjd5b7ec80e100ed0e6e7fb8ce3cd82a9c",
#             "u4e8eu51e4u864e",
#             "u52a9u7406u5de5u7a0bu5e08",
#             "",
#             "u5317u4eacu9996u90fdu56fdu9645u673au573au80a1u4efdu6709u9650u516cu53f8u98deu884cu533au7ba1u7406u90e8"
#         ],
#         [
#             "pj3b1d6eb671bf84243bdf7a5c52ee8d3f",
#             "u674eu5065",
#             "u9ad8u7ea7u5de5u7a0bu5e08",
#             "",
#             "u5317u4eacu9996u90fdu56fdu9645u673au573au80a1u4efdu6709u9650u516cu53f8u98deu884cu533au7ba1u7406u90e8"
#         ]
#     ]
# }

unicode_start = re.compile(r'u(\d)')
author_c = conn.cursor()
local_c = local_conn.cursor()
aff_cache = {}
n_unmatched_aff = 0
# include principal and participant
author_cache = {}
# not including unmatched authors whose institution not in am_affiliation
n_unmatched_author = 0
# same name and affiliation
same_name = []


def find_aff_id(name: str):
    global n_unmatched_aff
    try:
        aff_id = aff_cache[name]
    except KeyError:
        local_c.execute('SELECT affiliation_id FROM am_affiliation WHERE '
            'name_cn=%s LIMIT 1', (name,))
        aff_id = local_c.fetchone()
        if aff_id is None:
            n_unmatched_aff += 1
        else:
            aff_id = aff_id[0]
        aff_cache[name] = aff_id
    return aff_id


def find_author_id_with_aff(name: str, aff_id: int):
    global n_unmatched_author
    author_c.execute(
        'SELECT author_id FROM am_author WHERE '
        'last_known_affiliation_id=%s AND name=%s LIMIT 2',
        (aff_id, name)
    )
    row = author_c.fetchone()
    if row is None:
        result = None
        n_unmatched_author += 1
    else:
        result = row[0]
        if author_c.fetchone() is not None:
            same_name.append((name, aff_id))
    return result


def find_author_id(my_id: str, name: str, aff_name: str):
    aff_id = find_aff_id(aff_name)
    if aff_id is None:
        return None, None
    if len(my_id):
        try:
            author_id = author_cache[my_id]
        except KeyError:
            author_id = find_author_id_with_aff(name, aff_id)
            author_cache[my_id] = author_id
    else:
        author_id = find_author_id_with_aff(name, aff_id)
    return aff_id, author_id


if __name__ == '__main__':
    c = local_conn.cursor()
    cn_co = 'SELECT * FROM cn_co'
    if DEBUG:
        cn_co += ' LIMIT 100'
    c.execute(cn_co)
    for i, row in tqdm(enumerate(c.fetchall()), total=314862):
        try:
            if i % 10000 == 9999:
                local_conn.commit()
                print()
                print(i, f'''completed:
    aff_cache = {len(aff_cache)} (miss rate: {n_unmatched_aff / len(aff_cache)})
    author_cache = {len(author_cache)} (miss rate: {n_unmatched_author / len(author_cache)})
    same_name = {len(same_name)}''')

            result = json.loads(re.sub(unicode_start, r'\\u\1', row[0]))
            ratifyNo = result['ratifyNo']
            participants = result['participants']

            local_c.execute(
                'SELECT projectManager, supportOrg FROM nsfc_conclusion '
                'WHERE approvalNumber=%s', (ratifyNo,)
            )
            admin = local_c.fetchone()
            if admin is None:
                local_c.execute(
                    'SELECT 项目负责人, 依托单位 FROM nsfc_approval '
                    'WHERE 批准号=%s', (ratifyNo,)
                )
                admin = local_c.fetchone()
            aff_id, admin_id = find_author_id(result['projectAdmin'], admin[0], admin[1])

            local_c.execute(
                'SELECT id FROM cn_nnsf_grants WHERE approval_number = %s LIMIT 1',
                (ratifyNo,)
            )
            grant_id = local_c.fetchone()[0]

            if aff_id is not None:
                local_c.execute(
                    'UPDATE cn_nnsf_grants SET affiliation_id = %s WHERE id = %s',
                    (aff_id, grant_id)
                )
            if admin_id is not None:
                local_c.execute(
                    'UPDATE cn_nnsf_grants SET principal_id = %s WHERE id = %s',
                    (admin_id, grant_id)
                )

            for my_id, name, occupation, _, aff in participants:
                _, author_id = find_author_id(my_id, name, aff)
                if author_id is not None:
                    local_c.execute(
                        'INSERT INTO cn_nnsf_grants_participants VALUES (%s, %s)',
                        (grant_id, author_id)
                    )
        except Exception as e:
            print(e, i, row[0], sep='\n')
