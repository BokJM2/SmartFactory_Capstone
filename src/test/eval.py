#!/usr/bin/python
# -*- coding:utf8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/chatDB')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from chat import chat_with_ai, generate_abstract_context, create_chat_message, create_chat_completion, generate_final_response, generate_intermediate_thought

from config import cfg
import token_counter
import json

import argparse
parser = argparse.ArgumentParser(description='generate ground truth for questions')
# parser.add_argument('--q_id', type=int, default=-1, help='generate ground truth for a specific question')
parser.add_argument('--model_name', type=str, default='cwm_wo_tool', help='name of model')
parser.add_argument('--requests_dir', type=str, default='2024-10-31', help='dir of requests')
# 修改还是新增
parser.add_argument('--all', type=int, default=1, help='all=1: evaluate all questions, all=0: evaluate specific question')
args = parser.parse_args()



eval_prompt = """
你现在是一个大语言模型输出结果的评判员，你将得到以下五个输入:
1. 原始问题
2. 标准答案
3. 标准答案的生成流程:包括SQL查询结果、工具调用结果、模型思维链推理结果
4. 被测试模型的回答
5. 被测试模型回答的生成流程: 包括SQL查询结果、工具调用结果、模型思维链推理结果

你需要评价被测试模型的回答以及生成答案的逻辑是否正确，如果错误请给出错误类别和错误原因。你的评价需要按照如下格式:
评价结果;错误类别;评价理由
其中错误类别包括以下六种：
1. Wrong COT：模型的回答不符合标准答案的逻辑推理过程，并且被测试模型的回答也与标准答案不符，
2. Wrong syntax：生成的SQL查询语句、工具调用语句过程中存在语法错误，被测试模型的回答中包含报错信息
3. Wrong calculation：模型进行数学计算时出现错误，比如计算任务完成百分比时，使用了错误的计算公式或者输入参数。
4. Wrong understanding: 模型对请求的理解出现了错误，导致答非所问或执行了与预期不符的操作
5. Information Deviation: 被测试模型在做查询时，给定了实体的名字但未能检索到有效信息
6. Else: 不属于上述五种错误类型的错误

错误类别应该严格隶属于上述五种错误类型中的一个。如果问题回答正确，错误类别留空

下面是例子：
True;; Both the answer and the process of generating the answer are correct.
或者
False; Wrong syntax; An error is made in the SQL query result. In step 5, The model did not identify the correct order_id from the SQL query result in step 3. 

注意:
1. 如果标准答案使用了Tool或者Thought，被测试模型没有使用Tool或者Thought也是被允许的,只要通过其他有效手段获得了所需的数据，且最后结果正确即可。
2. 如果被测试模型的回答或回答的生成流程中包含报错信息，比如SQL查询失败，工具调用失败等，直接认为回答错误,且错误类别为Wrong syntax。
3. 标准答案和被测试模型给出的答案会包含结论和数据两部分，如果被测试模型回答的结论正确，则不应判定为Wrong COT错误，除非被测试模型的结论与标准答案的结论不同
4. 如果被测试模型的回答包括正确答案，也可以被认为是正确的，例如：问题要求订单，但模型列出了订单详细，依然被认为正确
5. 如果被测试模型的回答数据格式与标准答案不符，或者结论一致但提供了比标准答案更丰富或更简略的回答，依然被认为是正确的


原始问题: {request}
标准答案: {gt_results}
标准答案生成流程: {gt_steps}
被测试模型回答: {test_results}
被测试模型回答生成流程: {test_steps}

请根据上述信息对被测试模型的回答进行评价。
"""

def eval_response(request, gt_results, gt_steps, test_results, test_steps, model, token_limit=cfg.smart_token_limit):
    # operation_str = f"原始问题: {request}\n标准答案: {gt_results}\n标准答案生成流程: {gt_steps}\n被测试模型回答: {test_results}\n被测试模型回答生成流程: {test_steps}"
    contexts = [create_chat_message("user", eval_prompt.format(
        request=request,
        gt_results=gt_results,
        gt_steps=gt_steps,
        test_results=test_results,
        test_steps=test_steps
    ))]
    tokens_remaining = token_limit - token_counter.count_message_tokens(contexts, "gpt-4")  #
    return create_chat_completion(
        model=model,
        messages=contexts,
        max_tokens=tokens_remaining,
   )

def eval_all(output_dir, gt_dir):
    if args.all == 1:
        file_open_mode = 'w'
    else:
        file_open_mode = 'a'
    with open(os.path.join(output_dir, 'eval.csv'), file_open_mode) as out_file:
        for f in os.listdir(output_dir):
            print('{}/{}'.format(output_dir, f))
            if f.endswith('.json'):
                with open(os.path.join(output_dir, f), 'r') as file:
                    test = json.loads(file.read())
                    with open(os.path.join(gt_dir, f), 'r') as file:
                        gt = json.loads(file.read())
                        response = eval_response(
                            request=gt['q_en'],
                            gt_results=gt['gt'],
                            gt_steps=gt['steps'],
                            # test_results=test['gt'],
                            test_results=test['response'],
                            test_steps=test['steps'],
                            model=cfg.smart_llm_model
                        )
                        out_file.write(f"{f};{response}\n")
                        # print(response)
    pass



if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    outputs_dir = os.path.join(project_dir, 'outputs', args.model_name)
    requests_dir = os.path.join(project_dir, 'questions', args.requests_dir)
    eval_all(outputs_dir, requests_dir)



