import psycopg2
from api.exceptions import DataBaseException


def move(count, storage_name_from, storage_name_to, application):
    try:
        conn_from = psycopg2.connect(dbname="storage_", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        conn_to = psycopg2.connect(dbname="storage_to", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        print("Подключение к storage_to и storage_from установлено")
    except:
        raise DataBaseException
    
    cursor1 = conn_from.cursor()
    from_minus = """ update table_from set "from" = "from" - %s where id = %s;"""
    cursor1.execute(from_minus, (count, storage_name_from)) 
    conn_from.commit()

    cursor2 = conn_to.cursor()
    to_plus = """ update table_to set "to" = "to" + %s  where id = %s;"""
    cursor2.execute(to_plus, (count, storage_name_to))
    conn_to.commit()

    application.status = 'executed'
    application.save()

    cursor2.close()
    cursor1.close()
    conn_to.close()
    conn_from.close()
