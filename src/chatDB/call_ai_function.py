from config import Config
import ast
import global_token
from chatgpt import create_chat_completion

cfg = Config()



# This is a magic function that can do anything with no-code. See
# https://github.com/Torantulino/AI-Functions for more info.
def call_ai_function(function, args, description, model=None):
    """Call an AI function"""
    if model is None:
        model = cfg.smart_llm_model
    # For each arg, if any are None, convert to "None":
    #print(f"\n=====before args========\n{args}")
    args = [str(arg) if arg is not None else "None" for arg in args]
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [
        {
            "role": "system",
            #"content": f"You are now the following python function: ```# {description}\n{function}```\n\nOnly respond with your `return` value. Do not include any other explanatory text in your response.",
            "content": f"You are now the following python function: ```# {description}\n{function}```\n\nDo not write any code. Only respond with your `return` value. Do not include any other explanatory text in your response.",
        },
        {"role": "user", "content": args},
    ]
    # print(messages[0]["content"])
    # print(messages[1]["content"])
    # print(args)
    #print(f"\n=====after args========\n{args}")
    response = create_chat_completion(
        model=model, messages=messages, temperature=0
    )
    #print(f"\n=====response========\n{response}")

    return response


def populate_sql_statement(sql_str: str, previous_sql_results: list[list[dict]]) -> list[str]:
    # Try to fix the SQL using GPT:
    function_string = "def populate_sql_statement(sql_str: str, previous_sql_results: list[list[dict]]) -> list[str]:"
    args = [f"'''{sql_str}'''", f"'''{previous_sql_results}'''"]
    description_string = "Find useful information in the results of the previous sql statement, and replace <> with the corresponding information."

    result_string = call_ai_function(
        function_string, args, description_string, model=cfg.smart_llm_model
    )
    # print("chatgpt", result_string)
    brace_index = result_string.index("[")
    result_string = result_string[brace_index:]
    last_brace_index = result_string.rindex("]")
    result_string = result_string[:last_brace_index + 1]
    # print(result_string)
    list_of_str = ast.literal_eval(result_string)
    return list_of_str

def rewrite_user_request(user_input: str, context: list[str]) -> str:
    # Try to fix the SQL using GPT:
    function_string = "def rewrite_user_request(user_input: str, context: list[str]) -> str:"
    args = [f"'''{user_input}'''", f"'''{context}'''"]
    description_string = ("Based on the dialogue context, compile a complete user request, "
                          "ensuring all important entity information is included.")

    result_string = call_ai_function(
        function_string, args, description_string, model=cfg.smart_llm_model
    )
    # print("chatgpt", result_string)
    return result_string

def populate_operation_statement(operation_str: str, previous_operating_results: list[list[dict]], op_type) -> list[str]:
    # Try to fix the SQL using GPT:
    function_string = "def populate_operation_statement(operation_str: str, previous_operation_results: list[list[dict]]) -> list[str]:"
    args = [f"'''{operation_str}'''", f"'''{previous_operating_results}'''"]
    description_string = (
        "Find useful information in the results of the previous operating statement, and replace <> with the corresponding information. "
        "If you are unable to identify the parameters within the <> using the given information."
        "If the operation type is 'Tool' and the tool must be invoked multiple times with varying parameters, "
        "please output a list of tool operations with distinct parameters."
    )
    result_string = call_ai_function(
        function_string, args, description_string, model=cfg.smart_llm_model
    )
    # print("chatgpt", result_string)
    try:
        brace_index = result_string.index("[")
        result_string = result_string[brace_index:]
        last_brace_index = result_string.rindex("]")
        result_string = result_string[:last_brace_index + 1]
        # print(result_string)
        if op_type == 'Tool':
            return [result_string]
        else:
            list_of_str = ast.literal_eval(result_string)

            return list_of_str
    except:
        return [result_string]



if __name__ == '__main__':
    previous_sql_results = [[{"sale_id": 3}],
                            [{"fruit_id": 2, "quantity_sold": 20}, {"fruit_id": 3, "quantity_sold": 20}]]
    sql_str = "SELECT fruit_id, quantity_sold FROM sale_items WHERE <sale_id>;"
    #     sql_str = """UPDATE fruits
    # SET stock_quantity = stock_quantity + <quantity_sold>
    # WHERE fruit_id = <fruit_id>;"""
