#!/usr/bin/python
# -*- coding:utf8 -*-
import matplotlib.pyplot as plt
import os
# set font type as Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(project_dir)

fig_size = (2.5, 2.5)


questions_sources = {
    'Customer': 11,
    'Production \n Manager': 26,
    'Worker': 18
}

# generate a 饼图 for the questions_sources
def generate_pie_chart(questions_sources, path=None):
    # set the figure size
    # colors = ['#66b3ff','#ff9999','#ffcc99']
    fig, ax = plt.subplots(figsize=fig_size)
    # ax.pie(questions_sources.values(), labels=questions_sources.keys(), autopct='%1.1f%%', startangle=90, colors=colors)
    ax.pie(questions_sources.values(), labels=questions_sources.keys(), autopct='%1.1f%%', startangle=90)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    # plt.show()

generate_pie_chart(questions_sources,f'{project_dir}/outputs/figs/questions_sources_user.pdf' )


questions_operation_type = {
    'I & Q': 4,
    'U & Q': 5,
    'U & I & Q': 2,
    'Q': 44,
}
generate_pie_chart(questions_operation_type, f'{project_dir}/outputs/figs/questions_operation_type.pdf')

# 数字1出现了11次
# 数字2出现了20次
# 数字3出现了11次
# 数字4出现了10次
# 数字5出现了3次
questions_schema_num = {
   '1': 11,
    '2': 20,
    '3': 11,
    '4': 10,
    '5': 3
}
def genera_num_bar_chart(questions_schema_num, path):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.bar(questions_schema_num.keys(), questions_schema_num.values(), color='skyblue')
    plt.xlabel('Number of Related Tables')
    plt.ylabel('Number of Questions')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    # plt.show()

genera_num_bar_chart(questions_schema_num, f'{project_dir}/outputs/figs/questions_schema_num.pdf')
