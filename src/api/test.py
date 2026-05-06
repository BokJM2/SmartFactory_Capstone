#!/usr/bin/python
# -*- coding:utf8 -*-
from fashion import get_data
from fashion import generate_response
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--model', type=str, default='gpt-3.5-turbo')

args = parser.parse_args()

if __name__ == '__main__':
    # query = input('Please input your query: ')
    query = '香港理工大学全部订单'
    data, err = get_data(query, model=args.model, return_sql=True)

    sql = json.loads(data)['sql']

    data = json.loads(data)['rows']


    if err:
        print(f'Error: {err}')

    else:
        print('#'*50 + ' Result of executing SQL ' + '#'*50)
        print(data)
        response = generate_response(
            user_query=f'''
            Please use the content within the <Context></Context> tags as your knowledge to answer user questions.
            <Context>
            SQL query used to retrieve data from the database:
            {sql},
            Data retrieved from the database based on user questions:
            {data}
            </Context>
            User question: {query}
            ''',
            system_query='',
            model="gpt-3.5-turbo"
        )
        print('#'*50 + ' Response ' + '#'*50)
        print(response)



    # get
    # connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
    #                              cursorclass=pymysql.cursors.DictCursor)
    # cursor = connection.cursor()
    # cursor.execute(sql)
    # rows = cursor.fetchall()
    # json.dumps(rows, default=datetime_to_str, ensure_ascii=False)