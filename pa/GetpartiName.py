import pymysql

f1 = open('parti.txt','r')
f2 = open('apro.txt','r')
pars = f1.readlines()
apros = f2.readlines()
length = len(pars)
con_engine1 = pymysql.connect(host = 'localhost' ,user = 'root', password ='cjz122530' , database = '学者', port=3306, charset = 'utf8',autocommit =True)
cursor1 = con_engine1.cursor()

for i in range(length):
    par = pars[i].strip('\n')
    par = par.split(' ')
    try:
        apro = int(apros[i].strip('\n'))
        print(apro)
    except:
        continue
    for j in par:
        try:
            pname = j
            sql = "update cn_nnsf_grants_participants set grant_id=%d, participant_name=\'%s\' where ISNULL(participant_name) limit 1;"%(apro,j)
            print(sql)
            cursor1.execute(sql)
        except:
            continue

