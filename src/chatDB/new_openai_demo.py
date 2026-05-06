from openai import OpenAI
import os

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.302.ai/v1"
)



# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message)
    print(completion.choices[0].message.content)
