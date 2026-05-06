import os
import json
import matplotlib.pyplot as plt
import numpy as np

folder_path = '../../outputs/cwm-gpt-4o'
# Change font to Times new roman
plt.rcParams['font.family'] = 'Times New Roman'

output_path = '../../outputs/figs/stacked_bar_chart.pdf'


def get_json(folder_path: str) -> list[list[dict]]:
    """
    读取文件夹中的所有json文件并返回json对象中step的内容

    :param folder_path: 文件夹路径
    :return: json对象中step的内容
    """
    ret = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # print(type(data)) <class 'dict'>
                ret.append(data['steps'])
    return ret


def count_steps(json_steps: list[list[dict]]) -> list[dict[str, int]]:
    """
    统计每个步骤中SQL、Tool、Thought的数量

    :param json_steps: json的step的内容
    :return: 每个步骤中SQL、Tool、Thought的数量
    """
    max_step = max(len(x) for x in json_steps)
    ret = []
    for i in range(max_step):
        ret.append({'SQL': 0, 'Tool': 0, 'Thought': 0})
    for step in json_steps:
        for idx, classify in enumerate(step):
            ret[idx][classify['type']] += 1
    # print(ret)
    return ret


def draw_stacking_diagram(steps_cnt: list[dict[str, int]]) -> None:
    """
    根据步骤数量生成堆叠柱状图

    :param steps_cnt: 每个步骤中SQL、Tool、Thought的数量
    :return:
    """
    # labels = [f'Step {i+1}' for i in range(len(steps_cnt))]
    labels = [f'{i+1}' for i in range(len(steps_cnt))]
    sql_counts = [step['SQL'] for step in steps_cnt]
    tool_counts = [step['Tool'] for step in steps_cnt]
    thought_counts = [step['Thought'] for step in steps_cnt]

    # 绘图
    fig, ax = plt.subplots(figsize=(5, 2))
    n = len(sql_counts)
    width = 0.35
    ind = np.arange(n)
    sql_plot = ax.bar(ind, sql_counts, width, label='SQL')
    tool_plot = ax.bar(ind, tool_counts, width, bottom=sql_counts, label='Tool')
    thought_plot = ax.bar(ind, thought_counts, width, bottom=[sql_counts[i] + tool_counts[i] for i in range(n)], label='Thought')
    # 设置y轴范围
    ax.set_ylim(0, 60)
    ax.set_xlabel('Steps')
    ax.set_ylabel('Frequency')
    # ax.set_title('Stacked Bar Chart of SQL, Tool, and Thought Steps')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

    # plt.savefig('stacked_bar_chart.png')


if __name__ == "__main__":
    json_steps = get_json(folder_path)
    draw_stacking_diagram(count_steps(json_steps))
