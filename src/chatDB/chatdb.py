import json, re, time
from mysql import MySQLDB
from config import cfg
import time
import sys
# from chatdb_prompts import prompt_ask_steps, prompt_ask_steps_no_egs
from cwm_prompts import prompt_ask_steps, prompt_ask_steps_no_egs, prompt_single_sql_step
from tables import init_database, database_info, table_details
try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.prompts import PromptTemplate
from chatgpt import create_chat_completion
from call_ai_function import populate_sql_statement, populate_operation_statement
from chat import chat_with_ai, generate_abstract_context, create_chat_message, create_chat_completion, generate_final_response, generate_intermediate_thought
from rewrite_query import rewrite_query
if cfg.tool_open:
    try:
        from agents.agent_tools import tools_description_str, agent_executor
    except Exception:
        cfg.tool_open = False
        tools_description_str = ""
        agent_executor = None
else:
    tools_description_str = ""
    agent_executor = None





def get_steps_from_response(response):
    # Regular expression patterns to extract step number, description, and SQL query
    operation_type = "SQL"
    if cfg.tool_open:
        operation_type += "|Tool"
    if cfg.thought_open:
        operation_type += "|Thought"

    pattern = rf"Step(\d+):\s+(.*?)\n({operation_type})[\s]+`(.*?)`"

    # pattern = r"Step(\d+):\s+(.*?)\n(SQL|Tool|Thought)[\s]+`(.*?)`"
    matches = re.findall(pattern, response, re.DOTALL)

    # Extract information and create list of dictionaries
    result = []
    for match in matches:
        step_number = int(match[0])
        description = match[1]
        operation_type = match[2]
        operation = match[3]
        # print(sql_query+'\n')
        result.append({
            "id": step_number,
            "description": description.strip(),
            "operation_type": operation_type.strip(),
            "operation": operation.strip(),
        })
    print(result)
    return result


def init_system_msg():
    if cfg.single_sql_step:
        sys_temp = """
You are Chat With MES, a powerful AI assistant, a variant of ChatGPT that can utilize the database of the Manufacturing Execution System as external symbolic memory. \
You are an expert in databases, proficient in SQL statements and can use the database to help users.
For any user query, you should generate a single SQL statement to complete it.
The details of tables in the database are delimited by triple quotes.
\"\"\"
{table_details}
\"\"\"
        """
        sys_prompt = PromptTemplate(
            template=sys_temp,
            input_variables=[],
            partial_variables={"table_details": table_details}
        )
        return sys_prompt.format()

    if cfg.tool_open:
        sys_temp = """
You are Chat With MES, a powerful AI assistant, a variant of ChatGPT that can \
1) decide to invoke some provided tools to solve the query. \
2) utilize the database of the Manufacturing Execution System as external symbolic memory. \
For any user query, you should always prioritize using the given tool to complete it.
The following are the tools you can use, including their names, descriptions, and input args.
\"\"\"
{tool_details}
\"\"\"
Only if you cannot handle the command/query with any given tools, You are authorized to directly access the database.
In this case, you are an expert in databases, proficient in SQL statements and can use the database to help users. \
The details of tables in the database are delimited by triple quotes.
\"\"\"
{table_details}
\"\"\"
        """
        sys_prompt = PromptTemplate(
            template=sys_temp,
            input_variables=[],
            partial_variables={"table_details": table_details, "tool_details": tools_description_str}
        )
    else:
        sys_temp = """
You are Chat With MES, a powerful AI assistant, a variant of ChatGPT that can utilize the database of the Manufacturing Execution System as external symbolic memory. \
you are an expert in databases, proficient in SQL statements and can use the database to help users. \
The details of tables in the database are delimited by triple quotes.
\"\"\"
{table_details}
\"\"\"
        """
        sys_prompt = PromptTemplate(
            template=sys_temp,
            input_variables=[],
            partial_variables={"table_details": table_details}
        )
    sys_prompt_str = sys_prompt.format()
    return sys_prompt_str


def chain_of_memory(sql_steps, mysql_db):
    num_step = len(sql_steps)
    results_history = []
    new_mem_ops = []
    for i in range(num_step):
        cur_step = sql_steps[i]
        print(f"\nStep{cur_step['id']}: {cur_step['operation_type']}, {cur_step['description']}\n")
        if cfg.sleep:
            time.sleep(1)
        ori_operation_cmd = cur_step['operation']
        if need_update_sql(ori_operation_cmd):
            list_of_operation_str = populate_operation_statement(ori_operation_cmd, results_history, cur_step['operation_type'])
            print(list_of_operation_str)
            new_mem_ops.append(list_of_operation_str)
            for operation_str in list_of_operation_str:
                # 如果operation_str中包含 ASK!，则需要用户输入
                # if "ASK!" in operation_str:
                #     # operation_str = input("Please provide the information needed: ")
                #     operation_str = "Please provide the information needed: "
                #     results_history.append(f'Please ask the user for the required information: {operation_str}')
                #     return results_history, new_mem_ops
                if cur_step['operation_type'] == 'SQL':
                    print(f"Execute: \n{operation_str}\n")
                    sql_results, sql_res_str = mysql_db.execute_sql(operation_str)
                    print(f"Database response:\n{sql_res_str}\n")
                    results_history.append(
                        {'type': 'SQL', 'sql': operation_str, 'description': cur_step['description'], 'results': sql_results if sql_results else sql_res_str}
                    )
                elif cur_step['operation_type'] == 'Tool':
                    try:
                        response = agent_executor.invoke({"input": cur_step['description'] + '\n' + operation_str})
                    except Exception as e:
                        response = str(e)

                    print(f"Tool invoking response:\n{response}\n")
                    results_history.append({'type': 'Tool', 'results': response})
                elif cur_step['operation_type'] == 'Thought':
                    # results_history.append(f'Thought: {operation_str}')
                    result_of_thought = generate_intermediate_thought(
                        operation_str, results_history, cfg.smart_llm_model, cfg.smart_token_limit
                    )
                    print(f"Thought Step:\n{result_of_thought}\n")
                    results_history.append({'type': 'Thought', 'operation': operation_str, 'results': result_of_thought})
                else:
                    results_history.append(f'Unknown operation type: {cur_step["operation_type"]}')

        else:
            new_mem_ops.append([ori_operation_cmd])
            if cur_step['operation_type'] == 'SQL':
                print(f"Execute: \n{ori_operation_cmd}\n")
                sql_results, sql_res_str = mysql_db.execute_sql(ori_operation_cmd)
                print(f"Database response:\n{sql_res_str}\n")
                results_history.append(
                    {'type': 'SQL', 'sql': ori_operation_cmd, 'description': cur_step['description'],
                     'results': sql_results if sql_results else sql_res_str}
                )
            elif cur_step['operation_type'] == 'Tool':
                response = agent_executor.invoke({"input": cur_step['description'] + '\n' + ori_operation_cmd})
                print(f"Tool invoking response:\n{response}\n")
                results_history.append({'type': 'Tool', 'results': response})
            elif cur_step['operation_type'] == 'Thought':
                # results_history.append(f'Thought: {ori_operation_cmd}')

                result_of_thought = generate_intermediate_thought(
                    ori_operation_cmd, results_history, cfg.smart_llm_model, cfg.smart_token_limit
                )
                print(f"Thought Step:\n{result_of_thought}\n")
                results_history.append({'type': 'Thought', 'operation': ori_operation_cmd, 'results': result_of_thought})
            else:
                results_history.append(f'Unknown operation type: {cur_step["operation_type"]}')


    return results_history, new_mem_ops


def generate_chat_responses(user_inp, mysql_db, historical_message, context_abstract=""):
    # ask steps
    if cfg.enable_rewrite_query:
        user_inp = rewrite_query(user_inp)

    # prompt_ask_steps_str = prompt_ask_steps.format(user_inp=user_inp)
    if cfg.single_sql_step:
        prompt_ask_steps_str = prompt_single_sql_step.format(user_inp=user_inp)
    else:
        prompt_ask_steps_str = prompt_ask_steps.format(user_inp=user_inp, context_abstracts=context_abstract)

    # prompt_ask_steps_str = prompt_ask_steps_no_egs.format(user_inp=user_inp, context_abstracts=context_abstract)
    response_steps = chat_with_ai(init_system_msg(), prompt_ask_steps_str, historical_message, None,
                                  token_limit=cfg.smart_token_limit)

    historical_message[-2]["content"] = prompt_ask_steps_no_egs.format(user_inp=user_inp, context_abstracts=context_abstract)

    response_steps_list_of_dict = get_steps_from_response(response_steps)
    print(response_steps_list_of_dict)

    if len(response_steps_list_of_dict) == 0:
        print(f"NOT NEED MEMORY: {response_steps}")
        # return None, None, "None",
        sql_results_history, new_mem_ops = [], []
        # historical_message[-1]["content"] = str(sql_results_history)
        # create_chat_completion(
        #     [create_chat_message('system', '')]
        # )
        responses = generate_final_response(user_inp, sql_results_history, cfg.smart_llm_model, cfg.smart_token_limit)
    else:
        print(f"NEED MEMORY: {response_steps}")
        sql_results_history, new_mem_ops = chain_of_memory(response_steps_list_of_dict, mysql_db)
        # historical_message[-1]["content"] = str(sql_results_history)
        # create_chat_completion(
        #     [create_chat_message('system', '')]
        # )
        print(f"Data Retrival Completed, Generating the final responses...")
        responses = generate_final_response(user_inp, sql_results_history, cfg.smart_llm_model, cfg.smart_token_limit)

        print(f"Updating the context_abstract...")
        context_abstract = generate_abstract_context(user_inp, responses, cfg.smart_llm_model, context_abstract,
                                                 cfg.smart_token_limit)
    # historical_message[-1]["content"] = context_abstract
    # full_message_history, model, old_abstract, token_limit
    print("Finish!")
    return sql_results_history, new_mem_ops, None, responses, context_abstract

def need_update_sql(input_string):
    # pattern = r"<\S+>"
    pattern = r"<[^>]+>"
    matches = re.findall(pattern, input_string)
    # print(matches)
    # if matches:
    #     print("The pattern was found in the input string.")
    # else:
    #     print("The pattern was not found in the input string.")
    return matches


if __name__ == '__main__':

    # If parameters in command line, query = sys.argv[1] else query = input()

    enable_rewrite_query = True
    mysql_db = init_database(database_info, None)
    his_msgs = []
    print("START!")
    # query = sys.argv[1] if len(sys.argv) > 1 else input("USER INPUT: ")
    # query = "I am from The Hong Kong Polytechnic University. Today is July 2, 2024. Please help me create an order for 50 red T-shirts in size M and 30 blue sweaters in size XL."
    # query = "allocate task for the order whose name is PolyU_Tshirt"
    # query = ("I am from The Hong Kong Polytechnic University. Today is July 2, 2024. Please  help me create an order for 50 red T-shirts in size M and 30 blue sweaters in size XL."
    #          "Once the order is created, please proceed to allocate tasks.")
    # query = 'Find the latest order placed by the customer with the name "Polyu".'

    queries = [
        '寻找当前任务完成进度最快的裁剪组和缝纫组'
        # "今天是2024年11月8日。请帮用户香港理工大学创建一个订单，包括50件红色M号T恤和30件蓝色XL号毛衣，并自动分配生产任务",
        # "ID为1,3,5,9,11,13的原材料，他们的名字叫什么",
        # "PolyU的订单有多少个产品"
        # "Retrieve all orders and item details for the Customer PolyU",
        # "Find the latest order from polyu that requires a blue XL sweater, increase the quantity of the blue XL sweater by 10 units, and then automatically allocate the production tasks for this order."
        # "Find the latest order placed by the customer with the name 'Polyu'.",
        # "Find the order with the ID of 1.",
    ]

    # queries = [
    #     "查寻PolyU的顾客信息",
    #     "查寻这位顾客的订单信息"
    #     # "Find the latest order placed by the customer with the name 'Polyu'.",
    #     # "Find the order with the ID of 1.",
    # ]
    context_abstract = ""

    # iterate through the queries as query

    for query in queries:
        # 使用 rewrite_query 函数优化用户输入的问题
        # if enable_rewrite_query:
        #     query = rewrite_query(query)
        sql_results_history, new_mem_ops, err, response, context_abstract = generate_chat_responses(query, mysql_db, his_msgs, context_abstract)
        print("\n***********response***********\n", response)
        print("\n***********sql_results_history***********\n", sql_results_history)
        print("\n***********new_mem_ops***********\n", new_mem_ops)
        print("\n***********err***********\n", err)
        # query = input("USER INPUT: ")
