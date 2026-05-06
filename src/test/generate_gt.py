#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import json
import sys

# 添加args
import argparse
parser = argparse.ArgumentParser(description='generate ground truth for questions')
parser.add_argument('--prompt_add', type=str, default='', help='add prompt for a question')
parser.add_argument('--q_id', type=int, default=-1, help='generate ground truth for a specific question')

args = parser.parse_args()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/chatDB')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print(sys.path)
from chatdb import generate_chat_responses, init_database
mysql_db = init_database()

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load questions/q0702/*.json
# filter_q = None
if args.q_id != -1:
    filter_q = [args.q_id]
else:
    filter_q = None

outputs_dir = os.path.join(project_dir, 'questions', '2024-10-31')
os.makedirs(outputs_dir, exist_ok=True)
refresh = True


def question_filter(q_name):
    # extract file name and to int
    try:
        q_name = int(q_name.split('.')[0])
        if filter_q is None:
            return True
        else:
            return q_name in filter_q
    except:
        return False

def is_exist(q_name, outputs_dir):
    if refresh:
        return False
    return os.path.exists(os.path.join(outputs_dir, q_name))


def handle_request(q):
    print(q)
    historical_message, context_abstract = [], ""
    sql_results, sql_commands, err, response, context_abstract = generate_chat_responses(
        user_inp=q, mysql_db=mysql_db, historical_message=historical_message, context_abstract=context_abstract
    )
    return sql_results, response
    # return None

for f in os.listdir(outputs_dir):
    if f.endswith('.json') and question_filter(f) and is_exist(f, outputs_dir) is False:
        print(f)
        with open(os.path.join(outputs_dir, f), 'r') as file:
            q = json.loads(file.read())
        hint = 'Hint: ' + q['hint'] if 'hint' in q.keys() else ''
        sql_results, response = handle_request(q['q_en'] + '. ' +  hint + f'\n{args.prompt_add}')
        q['steps'] = sql_results
        q['gt'] = response
        with open(os.path.join(outputs_dir, f), 'w', encoding='utf-8') as out:
            out.write(json.dumps(q, indent=4, ensure_ascii=False, default=str))
                # utf-8 encoding
        # break
    else:
        # print(f'{f} exists. Skip.')
        pass
        # break





