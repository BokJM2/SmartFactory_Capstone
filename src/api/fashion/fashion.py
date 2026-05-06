import json
from datetime import datetime
import time
from typing import Tuple

import pymysql

from fashion.openai_chat import generate_sql
from config import conf


def get_data(query: str, model="gpt-4o", retry=3, return_sql=False) -> Tuple[str, str]:
    host = conf().get("mysql_host", "localhost")
    port = conf().get("mysql_port", 3306)
    user = conf().get("mysql_user", "root")
    password = conf().get("mysql_password", "123456")
    database = conf().get("mysql_database", "test")

    connection = None
    try:
        json_obj = generate_sql(query, model)
        sql = json_obj["sql"]
        thought = json_obj["thought"]
        completion_tokens = json_obj["completion_tokens"]
        prompt_tokens = json_obj["prompt_tokens"]
        total_tokens = json_obj["total_tokens"]
        # 创建连接
        connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        start_time = time.time()
        cursor.execute(sql)
        rows = cursor.fetchall()
        end_time = time.time()

        if return_sql:
            results = {
                'sql': sql,
                'rows': rows,
                'time': str(end_time - start_time),
                'thought': thought,
                'completion_tokens': completion_tokens,
                'prompt_tokens': prompt_tokens,
                'total_tokens': total_tokens
            }
            return json.dumps(results, default=datetime_to_str, ensure_ascii=False), ""
        else:
            return json.dumps(rows, default=datetime_to_str, ensure_ascii=False), ""
    except Exception as e:
        if retry > 0:
            time.sleep(1)
            print(f"exception: {repr(e)}, 剩余重试次数: {retry}, 重试中...")
            return get_data(query, model, retry - 1)
        else:
            return "", repr(e)
    finally:
        if connection:
            connection.close()


def datetime_to_str(o):
    if isinstance(o, datetime):
        return o.strftime("%Y年%m月%d日 %H:%M")
