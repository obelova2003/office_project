import psycopg2
from api.exceptions import DataBaseConnectException
import pydapper

    
def move(storage_to, storage_from, application):

    dsn_to = f"postgresql+psycopg2://{storage_to.user}:{storage_to.password}@{storage_to.host}:{storage_to.port}/{storage_to.name}"
    dsn_from = f"postgresql+psycopg2://{storage_from.user}:{storage_from.password}@{storage_from.host}:{storage_from.port}/{storage_from.name}"

    try:
        with (pydapper.connect(dsn_from) as conn_from,
             pydapper.connect(dsn_to) as conn_to):
            
            print("Подключение к storage_to и storage_from установлено")

            with conn_from.cursor() as cursor1:
                from_minus = """update table_from set "from" = "from" - %s where id = %s;"""
                cursor1.execute(from_minus, (application.count, storage_from.column))
 
            with conn_to.cursor() as cursor2:
                to_plus = """UPDATE table_to SET "to" = "to" + %s WHERE id = %s;"""
                cursor2.execute(to_plus, (application.count, storage_to.column))
            
            application.status = 'executed'
            application.save()
    except Exception as e:
        print(str(e))
        conn_from.rollback()
        conn_to.rollback()
        raise DataBaseConnectException
