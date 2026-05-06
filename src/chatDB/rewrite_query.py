from chatgpt import create_chat_completion
from recall_knowledge import retrive_standard_entity_names
from config import cfg
from extract_entity import extract_entities



def generate_standard_entity_mapping(entities):
    mapping = []
    entity_mapping_template = f"""
    - entity_name: {{entity_name}}
      entity_type: {{entity_type}}
      possible_standard_entity_names: {{possible_standard_names}}
    """
    for entity_type, entity_list in entities.items():
        if entity_list:
            for entity_name in entity_list:
                possible_standard_names = ", ".join(retrive_standard_entity_names(entity_type, entity_name))
                if possible_standard_names:
                    mapping.append(entity_mapping_template.format(entity_type=entity_type, entity_name=entity_name, possible_standard_names=possible_standard_names))
    return "\n".join(mapping)

def rewrite_query(question):
    """
    使用ChatGPT对输入的问题进行优化，替换实体名称为标准实体名称。
    
    :param question: 输入的问题
    :return: 优化后的问题
    """
    entities = extract_entities(question)
    print("\n***********extracted entities***********\n", entities)
    standard_entity_mapping = generate_standard_entity_mapping(entities)
    # 如果没有标准实体，直接返回原问题
    if not standard_entity_mapping:
        print("\n***********no standard entity mapping, return orginal question***********\n", question)
        return question
    rewrite_query_prompt = f"""
        # role
        You are a professional question optimization model. You can replace entity names in questions with standard entity names.

        # Standard Entity Names
        The correspondence between entity names and possible standard entity names is as follows
        '''
        {standard_entity_mapping}
        '''

        # Output Requirements
        1. Convert entity names to the most probable standard entity names.
        2. Replace the original entity names with "<entity_type = standard_entity_name>"

        # Output Examples
        1. Original Question:
        Orders of PolyU
        Rewritten Question:
        <customers.customer_name = 'PolyU'> orders
        2. Original Question:
        What are the sewing tasks that use silk
        Rewritten Question:
        What are the sewing tasks that use <products.product_name = 'Silk'>
        3. Original Question:
        What does the main warehouse have
        Rewritten Question:
        What does <warehouse.warehouse_name = 'Main Warehouse'> have
        4. Original Question:
        What tasks does the Advanced Sewers group have
        Rewritten Question:
        What tasks does <working_group.name = 'Advanced Sewers'> have
        5. Original Question:
        What tasks does the Advanced Cutters group have
        Rewritten Question:
        What tasks does <working_group.name = 'Advanced Cutters'> have

        # Original Question
        {question}

        # Rewritten Question
        """
    # print("\n***********rewrite query prompt***********\n", rewrite_query_prompt)
    messages = [
        {"role": "system", "content": "You are a question optimization model."},
        {"role": "user", "content": rewrite_query_prompt}
    ]
    
    optimized_question = create_chat_completion(messages, model=cfg.smart_llm_model)
    print("\n***********optimized question***********\n", optimized_question)
    return optimized_question.strip()

# 示例使用
if __name__ == "__main__":
    original_question = "港大1月的订单包含哪些产品？"
    optimized_question = rewrite_query(original_question)
    print(f"原始问题: {original_question}")
    print(f"优化后的问题: {optimized_question}")
