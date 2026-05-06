from langchain.prompts import PromptTemplate
# from sql_examples_bak import egs

# load the examples from the sql_examples/*files in the same directory
import os
egs = []
sql_examples_dir = os.path.join(os.path.dirname(__file__), "sql_examples")
for file in os.listdir(sql_examples_dir):
    if file.endswith(".txt"):
        with open(os.path.join(sql_examples_dir, file), "r") as f:
            egs.append(f.read())



# prompt_ask_steps_temp = """
# Please tell me what basic operations, including tools or sql commands, should I use in order to respond to the "USER INPUT". \
# If it needs multiple operations, please list them step by step concisely, and indicate whether the operation involves calling a tool or accessing a database via SQL. \
# If there is no need to use any operations, reply to the "USER INPUT" directly.
# At all times, you should prioritize using the provided tool. If the tool does not meet the requirements, only then may you resort to using SQL.
# In any step,
# In your final output, you need to replace the IDs of all entities (customers, workers, materials, products) with their names. The original database ID numbers should not appear in the response.
# The progress of an order is defined as the percentage of completing the sewing task.
# The output should be a markdown code snippet formatted in the following schema, \
# including the leading and trailing "\`\`\`" and "\`\`\`":
# ```
# Step1: <Description of first step>
# SQL `SQL command for step1`
#
# Step2: <Description of second step>
# Tool `Tool name, arguments for tool, purpose of using this tool`
#
# ......
# ```
#
# Backticks are important and must be added at the beginning and end of the command for every step!
#
# Here are some examples:
# {egs}
#
# Here are some context abstracts:
# {context_abstracts}
#
# USER INPUT: {user_inp}
# ANSWER:
# """

prompt_ask_steps_temp = """
Please tell me what basic operations, including tool, sql, or thought, should I use in order to respond to the "USER INPUT". \
If it needs multiple operations, please list them step by step concisely, and indicate whether the operation involves calling a tool or accessing a database via SQL. \
If there is no need to use any operations, reply to the "USER INPUT" directly.
At all times, you should prioritize using the provided tool. If the tool does not meet the requirements, only then may you resort to using SQL.
In any step, 
In your final output, you need to replace the IDs of all entities (customers, workers, materials, products) with their names. The original database ID numbers should not appear in the response.
The output should be a markdown code snippet formatted in the following schema, \
including the leading and trailing "\`\`\`" and "\`\`\`":
```
Step1: <Description of first step>
SQL `SQL command for step1`

Step2: <Description of second step>
Tool `Tool name, arguments for tool, purpose of using this tool`

Step3: <Description of third step>
Thought `Purpose of this intermediate reasoning step, what intermediate results are expected. and how to get them based on the results from the previous steps.`

......
```

Backticks are important and must be added at the beginning and end of the command for every step!

Here are some examples:
{egs}

Here are some context abstracts: 
{context_abstracts}

USER INPUT: {user_inp}
ANSWER:
"""

prompt_summary_final_response_temp = """
Here is the translated text:

"# Role
You are the chatDB intelligent assistant, capable of answering user questions based on the execution results of SQL queries within the <sql-result> XML tag.
The user question is \n""{user_inp}".

SQL Result
<sql-result>{sql_results}</sql-result>

Answer Requirements
Do not mention that the information comes from the <sql-result> tag.
Use markdown to optimize your answer, and try to organize the results into a table format.
Respond to questions in a friendly and lively tone, and feel free to use some emoji expressions. 😄"
If the SQL result is empty, please reply the user directly according to his question: \n{user_inp}.
"""

prompt_intermediate_thought_temp = """

You are an internal node within a complex reasoning process. Your task is to perform a specific intermediate reasoning step. 
Please achieve the following objective by retrieving the required information from the context.
objective: 
"{operation_str}"

The historical context are as follows:
"{sql_results}"
"""

prompt_ask_steps = PromptTemplate(
        template=prompt_ask_steps_temp,
        input_variables=["user_inp", "context_abstracts"],
        partial_variables={
            "egs": '\n'.join(egs),
            # "egs": ""
        }
    )

prompt_ask_steps_no_egs = PromptTemplate(
        template=prompt_ask_steps_temp,
        input_variables=["user_inp", "context_abstracts"],
        partial_variables={
            "egs": ""
        }
    )
prompt_summary_final_response = PromptTemplate(
        template=prompt_summary_final_response_temp,
        input_variables=["user_inp", "sql_results"],
    )

# prompt_intermediate_thought
prompt_intermediate_thought = PromptTemplate(
        template=prompt_intermediate_thought_temp,
        input_variables=["operation_str", "sql_results"],
    )


if __name__ == '__main__':
    print(prompt_ask_steps.format(user_inp="Hi"))
