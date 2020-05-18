import pymysql


def get_connector(target='acemap', db_name='am_paper'):
    if target == 'acemap':
        # Connect to the database
        connection = pymysql.connect(host='202.120.36.29',
                                     port=13307,
                                     user='mobilenet',
                                     password='mobilenet',
                                     db=db_name,
                                     # charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    elif target == 'local':
        raise NotImplementedError('You have to implement this part by yourself')
    else:
        raise ValueError
    return connection


if __name__ == '__main__':
    connection = get_connector()
    try:
        with connection.cursor() as cursor:
            sql = "select * from am_paper.am_paper_author where am_paper.am_paper_author.author_id = 1000000003"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        # connection.commit()
    finally:
        connection.close()
