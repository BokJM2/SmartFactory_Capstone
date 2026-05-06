#!/usr/bin/python
# -*- coding:utf8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from functions import *


model = ChatOpenAI(
    model=cfg.smart_llm_model,
    api_key=cfg.openai_api_key,  # if you prefer to pass api key in directly instaed of using env vars
    base_url=cfg.openai_base_url,
    temperature = 0.0
)

@tool(parse_docstring=True)
def tool_allocate_task_order(order_id: Optional[int] = None, order_name: Optional[str] = None) -> str:
    """ Allocate the cutting task and sewing tasks for all products belonging to the order, and return
    the allocated tasks and corresponding working groups.

    Args:
        order_id: The order ID, an integer.
        order_name: The order name, a string.
    """
    return allocate_task_order(order_id=order_id, order_name=order_name)

@tool(parse_docstring=True)
def tool_find_cutting_task(cutting_task_id: str):
    """ Find the cutting task by the cutting task ID.

    Args:
        cutting_task_id: The cutting task ID.
    """
    return find_cutting_task(cutting_task_id=cutting_task_id)

@tool(parse_docstring=True)
def tool_find_sewing_task(sewing_task_id: str):
    """ Find the sewing task by the sewing task ID.

    Args:
        sewing_task_id: The sewing task ID.
    """
    return find_sewing_task(sewing_task_id=sewing_task_id)



# @tool(parse_docstring=True)
# def tool_void() -> str:
#     """ When the command/query cannot be handled by any given tools. You should call this function.
#
#     Args:
#
#     """
#     return "I'm sorry, but I can't assist with that request."

@tool(parse_docstring=True)
def tool_get_wip_materials(product_id: str) -> str:
    """ Get the required work-in-progress materials for a product. The return value is a list of work-in-progress materials with their IDs and quality.

    Args:
        product_id: The product ID.
    """
    return get_wip_materials(product_id)

@tool(parse_docstring=True)
def tool_get_original_materials(wip_id: str) -> str:
    """ Get the original materials for a work-in-progress material. The return value is a list of original materials with their IDs and quality.

    Args:
        wip_id: The work-in-progress material ID.
    """
    return get_original_materials(wip_id)

@tool(parse_docstring=True)
def tool_get_warehouse_materials(material_id: str) -> str:
    """ Query the list of materials in the warehouse with an id equal to material_id.

    Args:
        material_id: The material ID.
    """
    return get_warehouse_materials(material_id)

@tool(parse_docstring=True)
def tool_find_order_details(order_id: int) -> str:
    """ Find the product details of an order by the order ID.

    Args:
        order_id: The order ID.
    """
    return find_details_of_order(order_id)

@tool(parse_docstring=True)
def tool_complete_task(task_id: str) -> str:
    """ Complete the task with the given task ID.

    Args:
        task_id: The task ID.
    """
    return complete_task(task_id)

@tool(parse_docstring=True)
def tool_store_materials(material_id: str, quantity: int, warehouse_id: int=1) -> str:
    """ Store the materials with the given material ID and quantity in the warehouse with the given warehouse ID.

    Args:
        material_id: The material ID.
        quantity: The quantity of materials.
        warehouse_id: The warehouse ID, default is 1.
    """
    return store_materials(material_id, quantity, warehouse_id)



# tools = [allocate_task_order, void]
# tools = [tool_allocate_task_order, tool_find_cutting_task, tool_find_sewing_task, tool_get_wip_materials,
#          tool_get_original_materials, tool_get_warehouse_materials, tool_find_order_details]
tools = [tool_allocate_task_order, tool_find_order_details, tool_complete_task, tool_store_materials]
tools_dict = {tool.name: tool for tool in tools}

tools_description_str = "\n\n".join([f"{tool.name}: {tool.description}\n{str(tool.args)}" for tool in tools])

# tools = [pow1]

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

# agent = model.bind_tools(tools)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Several tools are available to you. You should handle the command/query with the correct tool. "
                   "If you cannot handle it, please call the tool {{tool_void}} without any parameters and return the response without any modification."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)



    # product_select_sql = f"""SELECT * FROM products WHERE id = {};"""

if __name__ == '__main__':
    questions = [
        'find the cutting task with id=1 and the sewing task with id=3, judging whether their working group names are the same.',
        # 'allocate task for the order whose name is PolyU_Tshirt',
        # 'allocate task order with id=1',
        # 'find cutting task with id=1',
        # 'find sew task with id=3',
        # 'find richest working group'
    ]
    for question in questions:
        print(
            agent_executor.invoke({"input": question})
        )












