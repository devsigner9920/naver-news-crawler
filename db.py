import os
import time

import mysql.connector
from mysql.connector import Error
from functools import wraps


def connect_to_mysql(max_retries=5, delay=5):
    retries = 0
    connection = None

    while retries < max_retries:
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", 3306),
                user=os.getenv("DB_USER", "news"),
                password=os.getenv("DB_PASSWORD", "1234@"),
                database=os.getenv("DB_NAME", "news")
            )
            if connection.is_connected():
                print("MySQL에 성공적으로 연결되었습니다!")
                return connection
        except Error as e:
            retries += 1
            print(f"MySQL 연결 실패: {e}")
            if retries < max_retries:
                print(f"{delay}초 후 다시 시도합니다... (시도 횟수: {retries}/{max_retries})")
                time.sleep(delay)
            else:
                print("최대 재시도 횟수를 초과했습니다. 연결에 실패했습니다.")
                break

    return connection


# 데코레이터: DB 연결을 열고 닫는 로직을 자동으로 처리
def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect_to_mysql()
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
        return result

    return wrapper
