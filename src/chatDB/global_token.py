#!/usr/bin/python
# -*- coding:utf8 -*-
# 定义一个全局变量，用于跨模块共享
global_token_count = 0

# 可以定义一个函数来操作全局变量
def increment_token_count(amount):
    global global_token_count
    global_token_count += amount
    # print(f"Updated global_token_count: {global_token_count}")

def reset_token_count():
    global global_token_count
    global_token_count = 0
    # print(f"Reset global_token_count: {global_token_count}")

def get_token_count():
    return global_token_count