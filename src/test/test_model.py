#!/usr/bin/python
# -*- coding:utf8 -*-


#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import json
import sys

import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/chatDB')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 添加args
import argparse
import global_token

parser = argparse.ArgumentParser(description='generate ground truth for questions')
parser.add_argument('--q_id', type=int, default=-1, help='generate ground truth for a specific question')
parser.add_argument('--model_name', type=str, default='', help='name of model')
parser.add_argument('--requests_dir', type=str, default='2024-10-31', help='dir of requests')
parser.add_argument('--llm_model', type=str, default='gpt-4o', help='dir of requests')



args = parser.parse_args()

model_name = args.model_name

if model_name == 'cwm_wo_tool':
    # 设置环境变量 THOUGHT_OPEN 为 False
    os.environ['TOOL_OPEN'] = 'False'
if model_name == 'cwm_wo_thought':
    os.environ['THOUGHT_OPEN'] = 'False'
if model_name == 'cwm_wo_tool_thought':
    os.environ['TOOL_OPEN'] = 'False'
    os.environ['THOUGHT_OPEN'] = 'False'
if model_name == 'single':
    os.environ['SINGLE_SQL_STEP'] = 'True'

if model_name == 'cwm_wo_rewriter':
    os.environ['ENABLE_REWRITE_QUERY'] = 'False'

os.environ['SMART_LLM_MODEL'] = args.llm_model

from chatdb import generate_chat_responses, init_database, cfg
mysql_db = init_database()

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load questions/q0702/*.json
# filter_q = None
if args.q_id != -1:
    filter_q = [args.q_id]
else:
    filter_q = None

# The output directory
outputs_dir = os.path.join(project_dir, 'outputs', '{}-{}'.format(args.model_name, cfg.smart_llm_model))
os.makedirs(outputs_dir, exist_ok=True)
refresh = True

# The directory of requests
requests_dir = os.path.join(project_dir, 'questions', args.requests_dir)

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
    global_token.reset_token_count()
    sql_results, sql_commands, err, response, context_abstract = generate_chat_responses(
        user_inp=q, mysql_db=mysql_db, historical_message=historical_message, context_abstract=context_abstract
    )
    return sql_results, response, global_token.get_token_count()
    # return None
requests_list = os.listdir(requests_dir)
requests_list.sort(key=lambda x: int(x.split('.')[0]))

for f in requests_list:
    if f.endswith('.json') and question_filter(f) and is_exist(f, outputs_dir) is False:
        print(f)
        with open(os.path.join(requests_dir, f), 'r') as file:
            q = json.loads(file.read())
            try:
                sql_results, response, token_used = handle_request(q['q_en'])
                q['steps'] = sql_results
                q['response'] = response
                del q['gt']
                q['token_used'] = token_used
            except:
                q['steps'] = []
                q['response'] = 'A critical issue was discovered during the operation.'
                q['token_used'] = None
            with open(os.path.join(outputs_dir, f), 'w', encoding='utf-8') as out:
                out.write(json.dumps(q, indent=4, ensure_ascii=False, default=str))
                # utf-8 encoding
        # break
    else:
        # print(f'{f} exists. Skip.')
        pass
        # break





