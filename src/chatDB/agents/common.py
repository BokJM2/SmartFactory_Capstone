#!/usr/bin/python
# -*- coding:utf8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import math
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    AgentExecutor = None
    create_tool_calling_agent = None
from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain.memory import ConversationBufferWindowMemory
except ImportError:
    from langchain_community.memory import ConversationBufferWindowMemory

from config import cfg
