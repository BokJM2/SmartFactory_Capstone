from chatgpt import create_chat_completion
from config import cfg
import json

extract_entity_prompt_template = """
# role
你是专业的实体提取模型，你能够从给定的问题中提取出不同种类的实体。

# 实体类型
需要提取的实体类型包括：
- customers.customer_name
- orders.order_name
- products_types.description
- products.attributes
- materials.name
- warehouse.name
- working_group.name

# 实体类型说明
- customers.customer_name：顾客姓名，人名、企业或组织名称 eggs "张三", "香港理工大学"
- orders.order_name：订单名称 eggs "订单A", "3号订单"
- products_types.description：产品类型名称 eggs "裙子", "T恤"
- products.attributes：产品样式 egg "红色M码", "黑色小号"
- materials.name：生产衣服需要的材料名称 eggs "棉布", "丝绸"
- warehouse.name：仓库名称 eggs "主仓库", "仓库B"
- working_group.name：裁剪或缝纫任务的工作小组名称 eggs "大师裁剪组" "专家缝纫组"

# 输出要求
1. 从问题中提取出所有可能的实体，并按照上述类型进行分类
2. 以JSON格式输出结果，每种实体类型对应一个列表，如果某种类型没有提取到实体，则对应一个空列表
3. 只输出JSON格式的结果，不要包含其他说明文字

# 问题
{question}

# 输出要求
使用json格式输出，当问题中没有对应实体信息时，请输出空数组

# JSON输出格式示例
{{
    "customers.customer_name": ["张三", "香港理工大学"],
    "orders.order_name": ["订单A"],
    "products_types.description": ["裙子", "T恤"],
    "products.attributes": ["红色大号"],
    "materials.name": ["棉布"],
    "warehouse.name": [],
    "working_group.name": [],
}}
"""

def extract_entities(question):
    """
    使用ChatGPT从输入的问题中提取实体。
    
    :param question: 输入的问题
    :return: 包含提取实体的字典
    """
    prompt = extract_entity_prompt_template.format(question=question)
    messages = [
        {"role": "system", "content": "You are an entity extraction model."},
        {"role": "user", "content": prompt}
    ]
    
    response = create_chat_completion(
        messages, 
        model=cfg.smart_llm_model,
        response_format="json_object"
    )
    
    try:
        entities = json.loads(response)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response")
        entities = {}
    return entities

# 示例使用
if __name__ == "__main__":
    sample_question = "张三在1月份下了一个订单A，包含5件红色大号T恤，使用优质棉布制作"
    extracted_entities = extract_entities(sample_question)
    print("提取的实体:")
    print(json.dumps(extracted_entities, ensure_ascii=False, indent=2))
