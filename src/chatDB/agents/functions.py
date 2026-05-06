#!/usr/bin/python
# -*- coding:utf8 -*-


import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import *


# from ..chatdb import mysql_db
from tables import init_database

from typing import Optional


mysql_db = init_database()

def complete_task(task_id: str, task_type: str, number):
    if task_type == 'cutting':
        task_select_sql = f'''
            SELECT planned_number, completed_number FROM cutting_tasks WHERE id = {task_id};
        '''
        task_select_sql_results, task_select_sql_res_str = mysql_db.execute_sql(task_select_sql)
        if task_select_sql_results[0]['planned_number'] <= task_select_sql_results[0]['completed_number'] + number:
            task_update_sql = f'''
                UPDATE cutting_tasks SET completed_number = completed_number + {number}, status = 2 WHERE id = {task_id};
            '''
        else:
            task_update_sql = f'''
                UPDATE cutting_tasks SET completed_number = completed_number + {number} WHERE id = {task_id};
            '''
            
    elif task_type == 'sewing':
        task_select_sql = f'''
            SELECT planned_number, completed_number FROM sewing_tasks WHERE id = {task_id};
        '''
        task_select_sql_results, task_select_sql_res_str = mysql_db.execute_sql(task_select_sql)
        if task_select_sql_results[0]['planned_number'] <= task_select_sql_results[0]['completed_number'] + number:
            task_update_sql = f'''
                UPDATE sewing_tasks SET completed_number = completed_number + {number}, status = 2 WHERE id = {task_id};
            '''
        else:
            task_update_sql = f'''
                UPDATE sewing_tasks SET completed_number = completed_number + {number} WHERE id = {task_id};
            '''
    else:
        print(f"Invalid task type {task_type}.")
        return
    task_update_sql_results = mysql_db.execute_sql(task_update_sql)
    return task_update_sql_results

def store_materials(material_id: str, quantity: int, warehouse_id: int):
    material_insert_sql = f'''
        INSERT INTO warehouse_material (material_id, warehouse_id, total_number, left_number) VALUES ({material_id}, {warehouse_id}, {quantity}, {quantity});
    '''
    material_insert_sql_results = mysql_db.execute_sql(material_insert_sql)
    # 判断是否插入成功
    if 'successfully' not in material_insert_sql_results[1]:
        return "Failed to store material"

    # 检索最新插入的记录
    material_select_sql = f'''
        SELECT * FROM warehouse_material WHERE id = {mysql_db.last_insert_row_id()};
    '''
    material_select_sql_results, material_select_sql_res_str = mysql_db.execute_sql(material_select_sql)
    return material_select_sql_results

def get_wip_materials(product_id: str):
    material_select_sql = f'''
        SELECT material_id, number FROM product_material WHERE product_id = {str(product_id)};
    '''
    material_select_sql_results, material_select_sql_res_str = mysql_db.execute_sql(material_select_sql)
    return material_select_sql_results

def get_original_materials(wip_id: str):
    material_select_sql = f'''
        SELECT origin_material_id, number FROM wip_material WHERE wip_id = {str(wip_id)};
    '''
    material_select_sql_results, material_select_sql_res_str = mysql_db.execute_sql(material_select_sql)
    return material_select_sql_results

def get_warehouse_materials(material_id: str):
    warehouse_material_select_sql = f'''
        SELECT id, warehouse_id, left_number FROM warehouse_material WHERE material_id = {str(material_id)};
    '''
    warehouse_material_select_sql_results, warehouse_material_select_sql_res_str = mysql_db.execute_sql(warehouse_material_select_sql)
    return warehouse_material_select_sql_results

def update_warehouse_materials(warehouse_material_id: int, left_number: int):
    if left_number < 0:
        print(f"Invalid left number {left_number} for warehouse material {warehouse_material_id}.")
        return
    warehouse_material_update_sql = f'''
        UPDATE warehouse_material SET left_number = {left_number} WHERE id = {warehouse_material_id};
    '''
    warehouse_material_update_sql_results = mysql_db.execute_sql(warehouse_material_update_sql)
    return warehouse_material_update_sql_results

def allocate_cutting_task(order_product_id: str, produced_wip_id: str, planned_number: int, working_group_id: str):
    cutting_task_insert_sql = f'''
        INSERT INTO cutting_tasks (order_product_id, produced_wip_id, planned_number, completed_number, working_group_id, status)
        VALUES ('{order_product_id}', '{produced_wip_id}', {planned_number}, 0, '{working_group_id}', 0);
    '''
    result = mysql_db.execute_sql(cutting_task_insert_sql)
    result_str = []

    if 'successfully' in result[1]:
        insert_id = mysql_db.last_insert_row_id()
        result_str.append('Allocate cutting task {} to {}.'.format(
            str(find_cutting_task(cutting_task_id=insert_id)[0]),
            find_working_group(work_group_id=working_group_id)[0]['name'],
        ))
    else:
         return "Failed to allocate cutting task. {}".format(result[0])

    ori_material_select_sql_results = get_original_materials(wip_id=produced_wip_id)

    for item in ori_material_select_sql_results:
        ori_m, ori_planned_number = item['origin_material_id'], math.ceil(item['number'] * planned_number)

        # 对 ori_planned_number 向上取整
        warehouse_material_select_sql_results = get_warehouse_materials(material_id=ori_m)
        for item in warehouse_material_select_sql_results:
            warehouse_material_id, warehouse_id, left_number = item['id'], item['warehouse_id'], item['left_number']
            used_number = min(left_number, ori_planned_number)
            ori_planned_number -= used_number
            left_number -= used_number
            update_warehouse_materials(warehouse_material_id=warehouse_material_id, left_number=left_number)
            result = allocate_cutting_materials(cutting_task_id=insert_id, warehouse_material_id=warehouse_material_id, allocated_number=used_number)
            # result_str += ['Allocate original material {} to cutting task {}: {}'.format(ori_m, insert_id, result)]
            result_str += ['Allocate {} original material(id={}) from warehouse(id={}) to sewing task (id={}): {}'.format(
                used_number, ori_m, warehouse_id, insert_id, result
            )]
            if ori_planned_number == 0:
                break
        if ori_planned_number > 0:
            allocate_cutting_materials(cutting_task_id=insert_id, warehouse_material_id=None, allocated_number=used_number)
            result_str += ['Not enough original material {} in warehouse. Please purchase more. {} additional units are required.'.format(
                    ori_m, ori_planned_number)]

    return result_str

def find_working_group(work_group_id: str):
    working_group_select_sql = f'''
        SELECT * FROM working_group WHERE id = {work_group_id};
    '''
    working_group_select_sql_results, working_group_select_sql_res_str = mysql_db.execute_sql(working_group_select_sql)
    return working_group_select_sql_results

def find_sewing_task(sewing_task_id: str):
    sewing_task_select_sql = f'''
        SELECT * FROM sewing_tasks WHERE id = {sewing_task_id};
    '''
    sewing_task_select_sql_results, sewing_task_select_sql_res_str = mysql_db.execute_sql(sewing_task_select_sql)
    return sewing_task_select_sql_results

def find_cutting_task(cutting_task_id: str):
    cutting_task_select_sql = f'''
        SELECT * FROM cutting_tasks WHERE id = {cutting_task_id};
    '''
    cutting_task_select_sql_results, cutting_task_select_sql_res_str = mysql_db.execute_sql(cutting_task_select_sql)
    return cutting_task_select_sql_results

def allocate_cutting_materials(cutting_task_id: str, allocated_number: int, warehouse_material_id: Optional[str] = None):
    allocate_cutting_materials_sql = f'''
        INSERT INTO cutting_material_allocation (cutting_task_id, warehouse_material_id, allocated_num, is_allocated)
        VALUES ({cutting_task_id}, {warehouse_material_id if warehouse_material_id else 'null'}, {allocated_number}, 0);
    '''
    result = mysql_db.execute_sql(allocate_cutting_materials_sql)
    return result

def allocate_sewing_materials(sewing_task_id: str, allocated_number: int, warehouse_material_id: Optional[str] = None):
    allocate_sewing_materials_sql = f'''
        INSERT INTO sewing_material_allocation (sewing_task_id, warehouse_material_id, allocated_num, is_allocated)
        VALUES ({sewing_task_id}, {warehouse_material_id if warehouse_material_id else 'null'}, {allocated_number}, 0);
    '''
    result = mysql_db.execute_sql(allocate_sewing_materials_sql)
    return result

def allocate_sewing_task(order_product_id: str, planned_number: int, working_group_id: str):

    sewing_task_insert_sql = f''' INSERT INTO sewing_tasks (order_product_id, planned_number, completed_number, working_group_id, status)
    VALUES ('{order_product_id}', {planned_number}, 0, '{working_group_id}', 0);
    '''
    result = mysql_db.execute_sql(sewing_task_insert_sql)

    if 'error' not in result[1]:
        insert_id = mysql_db.last_insert_row_id()
        return 'Allocate sewing task {} to {}.'.format(
            str(find_sewing_task(sewing_task_id=insert_id)[0]),
            find_working_group(work_group_id=working_group_id)[0]['name'],
        ), insert_id
    else:
        return "Failed to allocate sewing task.", None


# 寻找最空闲的cutting group
def find_cutting_group_working_load():
    """
    Find the most idle cutting group.
    :return:
    """
    cutting_group_select_sql = f'''
        SELECT working_group_id, SUM(planned_number - completed_number) AS unfinished_workload
        FROM cutting_tasks
        WHERE status != 2
        GROUP BY working_group_id;
    '''
    cutting_group_select_sql_results, cutting_group_select_sql_res_str = mysql_db.execute_sql(cutting_group_select_sql)
    return cutting_group_select_sql_results

def find_sewing_group_working_load():
    sewing_group_select_sql = f'''
        SELECT working_group_id, SUM(planned_number - completed_number) AS unfinished_workload
        FROM sewing_tasks
        WHERE status != 2
        GROUP BY working_group_id;
    '''
    sewing_group_select_sql_results, sewing_group_select_sql_res_str = mysql_db.execute_sql(sewing_group_select_sql)
    return sewing_group_select_sql_results

def find_details_of_order(order_id: int):
    condition = f"op.order_id = {order_id}"
    order_product_select_sql = f'''SELECT op.id, op.order_id, op.product_id, p.attributes, pt.description, op.number 
        FROM order_product op
        JOIN products p ON op.product_id = p.id
        JOIN products_types pt ON p.products_type_id = pt.id
        WHERE {condition};
    '''
    order_product_select_sql_results, order_product_select_sql_res_str = mysql_db.execute_sql(order_product_select_sql)
    return order_product_select_sql_results

def allocate_task_order(order_id: Optional[int] = None, order_name: Optional[str] = None) -> str:
    """ Allocate the cutting task and sewing tasks for all products belonging to the order, and return
    the allocated tasks and corresponding working groups.

    Args:
        order_id: The order ID, an integer.
        order_name: The order name, a string.
    """

    responses = []
    if order_id is not None:
        condition = f"o.id = {order_id}"
    else:
        condition = f"o.order_name = '{order_name}'"

    # 使用条件拼接SQL语句
    order_product_select_sql = f"""SELECT op.id, op.product_id, op.number, p.attributes, pt.description
        FROM order_product op
        JOIN orders o ON op.order_id = o.id
        JOIN products p ON op.product_id = p.id
        JOIN products_types pt ON p.products_type_id = pt.id
        WHERE {condition};"""

    order_product_select_sql_results, order_product_select_sql_res_str = mysql_db.execute_sql(order_product_select_sql)
    responses += ['The order products for the order {}: {}'.format(condition, order_product_select_sql_results)]



    for item in order_product_select_sql_results:
        order_product_id, product_number, product_id = item['id'], item['number'], item['product_id']

        # find the most idle sewing group and allocate the sewing task
        sewing_group_select_sql_results = find_sewing_group_working_load()
        most_idle_sewing_group = min(sewing_group_select_sql_results, key=lambda x: x['unfinished_workload'])
        result, insert_id = allocate_sewing_task(order_product_id=order_product_id, planned_number=product_number, working_group_id=most_idle_sewing_group['working_group_id'])
        responses += ['Allocate tasks for order product {}: {}'.format(order_product_id, result)]

        # for m, required_number in material_select_sql_results:
        material_select_sql_results = get_wip_materials(product_id=product_id)
        responses += ['Allocate material for the sewing task {}'.format(insert_id)]
        for item in material_select_sql_results:
            m, required_number = item['material_id'], item['number']
            total_required_number = required_number * product_number

            warehouse_material_select_sql_results = get_warehouse_materials(material_id=m)
            for item in warehouse_material_select_sql_results:
                warehouse_material_id, warehouse_id, left_number = item['id'], item['warehouse_id'], item['left_number']
                used_number = min(left_number, total_required_number)
                if used_number !=0 :
                    total_required_number -= used_number
                    left_number -= used_number
                    update_warehouse_materials(warehouse_material_id=warehouse_material_id, left_number=left_number)
                    result = allocate_sewing_materials(sewing_task_id=insert_id, warehouse_material_id=warehouse_material_id, allocated_number=used_number)
                    # responses.append(result)
                    responses += ['Allocate {} material(id={}) from warehouse(id={}) to sewing task (id={}): {}'.format(
                        used_number, m, warehouse_id, insert_id, result
                    )]

                if total_required_number == 0:
                    break

            if total_required_number > 0:
                result = allocate_sewing_materials(sewing_task_id=insert_id, warehouse_material_id=None, allocated_number=total_required_number)
                # responses.append(result)
                responses += ['Allocate {} material(id={}) from warehouse(id={}) to sewing task (id={}): {}'.format(
                    total_required_number, m, 'None', insert_id, result
                )]

                cutting_group_select_sql_results = find_cutting_group_working_load()
                most_idle_cutting_group = min(cutting_group_select_sql_results, key=lambda x: x['unfinished_workload'])
                result = allocate_cutting_task(
                    order_product_id=order_product_id, produced_wip_id=m, planned_number=total_required_number, working_group_id=most_idle_cutting_group['working_group_id']
                )
                responses += result

    return responses


if __name__ == '__main__':
    # allocate_task_order(order_name="PolyU_Tshirt")
    # result = allocate_task_order(order_name='PolyU_Tshirt')
    result = allocate_task_order(order_id=22)











