import getpass
import os
from config import cfg

from langchain.tools import BaseTool
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate



model = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=cfg.openai_api_key,  # if you prefer to pass api key in directly instaed of using env vars
    base_url=cfg.openai_base_url,
    temperature=0,
)

response = model.invoke([HumanMessage(content="hi!")])

c = 10
@tool(parse_docstring=True)
def sum2(a: int, b: int) -> int:
    """ return the sum of two int.

    Args:
        a: The first number.
        b: The second number.
    """
    return  (a + b) * c

@tool(parse_docstring=True)
def mul2(a: int, b: int) -> int:
    """ return the multiplication of two int.

    Args:
        a: The first number.
        b: The second number.
    """
    return  (a * b) * c

@tool(parse_docstring=True)
def pow1(a: int ) -> int:
    """ return the multiplication of two int.

    Args:
        a: The first number.
    """
    return  (a ** 2 ) * c

@tool(parse_docstring=True)
def void() -> str:
    """ If the query cannot be solved other tools, call this tool.

    Args:
    """
    return  'Unable to solve the query.'



tools = [sum2, mul2, pow1, void]
tools_dict = {tool.name: tool for tool in tools}
# tools = [pow1]

conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
)

# agent = initialize_agent(
#     agent='chat-react-description',
#     tools=tools,
#     llm=model,
#     verbose=True,
#     max_iterations=3,
#     early_stopping_method='generate',
#     memory=conversational_memory
# )

agent = model.bind_tools(tools)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a mathematical assistant. Several tools are available to you. You have to use the tools to solve the query. "
                   "If the query cannot be solved, call the void tool. "
                   "Unfortunately, the Assistant is terrible at maths. "
                   "When provided with math questions, no matter how simple, assistant always refers to its trusty tools and absolutely does NOT try to answer math questions by itself"
                   "Even if the returned answer is wrong, the assistant will still return the answer."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)


questions = [
    'what is 2 + 2',
    'what is 3 * 3',
    'What if change * to + ?',
    'What is 3/2?'
]

# messages = []

for question in questions:
    # message = agent.invoke({"input": question})
    message = agent_executor.invoke({"input": question})
    print(message)
    # ai_msg = agent.invoke([HumanMessage(question)])
    # for tc in ai_msg.tool_calls:
    #     messages.append(tools_dict[tc['name']].invoke(tc))

    # response = agent.invoke(HumanMessage(question))
    # print(response)

# print(messages)




