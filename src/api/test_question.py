#!/usr/bin/python
# -*- coding:utf8 -*-
import argparse
import json

from fashion import generate_response
from fashion import get_data

parser = argparse.ArgumentParser()

parser.add_argument('--model', type=str, default='gpt-3.5-turbo')

args = parser.parse_args()

if __name__ == '__main__':
    id = 1
    with open(f'../../questions/q0702/{id}.json', 'r', encoding='utf-8') as file:
        question = json.load(file)
    query = question["q_en"]

    data, err = get_data(query, model=args.model, return_sql=True)

    sql = json.loads(data)['sql']
    rows = json.loads(data)['rows']
    execution_time = json.loads(data)['time']
    thought = json.loads(data)['thought']
    completion_tokens = json.loads(data)['completion_tokens']
    prompt_tokens = json.loads(data)['prompt_tokens']
    total_tokens = json.loads(data)['total_tokens']

    if err:
        print(f'Error: {err}')

    else:
        print('#' * 50 + ' Result of executing SQL ' + '#' * 50)
        print(rows)
        response = generate_response(
            user_query=f'''
             Please use the content within the <Context></Context> tags as your knowledge to answer user questions.
             <Context>
             SQL query used to retrieve data from the database:
             {sql},
             Data retrieved from the database based on user questions:
             {rows}
             </Context>
             User question: {query}
             ''',
            system_query='',
            model="gpt-3.5-turbo"
        )

        print('#' * 50 + ' Response ' + '#' * 50)
        print(response)

        if 'gt' in question:
            del question['gt']
        question["thought"] = thought
        question["sqls"] = [{
            "command": sql,
            "execution time": execution_time,
            "Result of executing SQL": rows,
        }]
        question["answer"] = response
        question['tokens'] = {}
        question['tokens']['completion_tokens'] = completion_tokens
        question['tokens']['prompt_tokens'] = prompt_tokens
        question['tokens']['total_tokens'] = total_tokens
        with open(f'../../outputs/gpt35/{id}.json', 'w', encoding='utf-8') as file:
            json.dump(question, file, ensure_ascii=False, indent=2)
