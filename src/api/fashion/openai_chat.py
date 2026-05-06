import json
from openai import OpenAI
import re
from config import conf

client = OpenAI(
    api_key=conf().get("openai_api_key", ""),
    base_url=conf().get("openai_base_url", "https://api.openai.com/v1")
)

GENERATE_SQL_PROMPT = """
# CONTEXT #
The MySQL database table structure for a clothing production management system is as follows:
```sql
CREATE DATABASE fashion DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE fashion;

-- 客户信息表
CREATE TABLE `customers` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '客户ID',
  `customer_name` VARCHAR(255) NOT NULL COMMENT '客户名称'
);

-- 订单信息表
CREATE TABLE `orders` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '订单ID',
  `user_id` VARCHAR(36) NOT NULL COMMENT '客户ID',
  `order_name` VARCHAR(255) NOT NULL COMMENT '订单名称',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订单创建时间'
);

-- 产品类型表
CREATE TABLE `products_types` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '产品类型ID',
  `description` VARCHAR(255) NOT NULL COMMENT '产品类型描述'
);

-- 产品表
CREATE TABLE `products` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '产品ID',
  `products_type_id` VARCHAR(36) NOT NULL COMMENT '产品类型ID',
  `attributes` VARCHAR(255) NOT NULL COMMENT '产品属性'
);

-- 原料表
CREATE TABLE `materials` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '原料ID',
  `name` VARCHAR(255) NOT NULL COMMENT '原料名称',
  `unit` VARCHAR(255) NOT NULL COMMENT '原料单位',
  `type` ENUM('wip', 'origin') NOT NULL COMMENT '原料类型'
);

-- 订单产品关系表
CREATE TABLE `order_product` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '订单产品ID', 
  `order_id` VARCHAR(36) NOT NULL COMMENT '订单ID',
  `product_id` VARCHAR(36) NOT NULL COMMENT '产品ID',
  `number` INTEGER NOT NULL DEFAULT 0 COMMENT '订单产品数量'
);

-- 工作组表
CREATE TABLE `working_group` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '工作组ID',
  `type` ENUM('sew', 'cut') NOT NULL COMMENT '工作组类型，缝纫小组、裁剪小组',
  `name` VARCHAR(255) NOT NULL COMMENT '工作组名称'
);

-- 订单产品裁剪任务表
CREATE TABLE `cutting_tasks` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '裁剪任务ID',
  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '裁剪任务开始时间',
  `end_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '裁剪任务结束时间',
  `working_group_id` VARCHAR(36) NOT NULL COMMENT '工作组ID',
  `order_product_id` VARCHAR(36) NOT NULL COMMENT '订单产品ID',
  `planned_number` INTEGER NOT NULL DEFAULT 0 COMMENT '计划裁剪数量',
  `completed_number` INTEGER NOT NULL DEFAULT 0 COMMENT '已完成裁剪数量',
  `is_started` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '裁剪任务是否已开始'
);

-- 订单产品缝纫任务表
CREATE TABLE `sewing_tasks` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '缝纫任务ID',
  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '缝纫任务开始时间',
  `end_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '缝纫任务结束时间',
  `working_group_id` VARCHAR(36) NOT NULL COMMENT '工作组ID',
  `order_product_id` VARCHAR(36) NOT NULL COMMENT '订单产品ID',
  `planned_number` INTEGER NOT NULL DEFAULT 0 COMMENT '计划缝纫数量',
  `completed_number` INTEGER NOT NULL DEFAULT 0 COMMENT '已完成缝纫数量',
  `is_started` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '缝纫任务是否已开始'
);

-- 订单产品裁剪任务原料分配表
CREATE TABLE `cutting_material_allocation` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '裁剪任务原料分配ID',
  `warehouse_material_id` VARCHAR(36) NOT NULL COMMENT '仓库原料ID',
  `cutting_task_id` VARCHAR(36) NOT NULL COMMENT '裁剪任务ID',
  `allocated_num` INTEGER NOT NULL DEFAULT 0 COMMENT '原料分配数量',
  `is_allocated` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '原料是否已分配'
);

-- 订单产品缝纫任务原料分配表
CREATE TABLE `sewing_material_allocation` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '缝纫任务原料分配ID',
  `warehouse_material_id` VARCHAR(36) NOT NULL COMMENT '仓库原料ID',
  `sewing_task_id` VARCHAR(36) NOT NULL COMMENT '缝纫任务ID',
  `allocated_num` INTEGER NOT NULL DEFAULT 0 COMMENT '原料分配数量',
  `is_allocated` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '原料是否已分配'
);

-- 仓库表
CREATE TABLE `warehouse` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '仓库ID',
  `name` VARCHAR(255) NOT NULL COMMENT '仓库名称'
);

-- 仓库产品关系表
CREATE TABLE `warehouse_product` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '仓库产品ID',
  `warehouse_id` VARCHAR(36) NOT NULL COMMENT '仓库ID',
  `product_id` VARCHAR(36) NOT NULL COMMENT '产品ID',
  `left_number` INTEGER NOT NULL DEFAULT 0 COMMENT '产品剩余库存数量'
);

-- 仓库原料关系表
CREATE TABLE `warehouse_material` (
  `id` VARCHAR(36) PRIMARY KEY COMMENT '仓库原料ID',
  `warehouse_id` VARCHAR(36) NOT NULL COMMENT '仓库ID',
  `material_id` VARCHAR(36) NOT NULL COMMENT '原料ID',
  `left_number` INTEGER NOT NULL DEFAULT 0 COMMENT '原料剩余库存数量'
);

-- 外键约束
ALTER TABLE `orders` ADD FOREIGN KEY (`user_id`) REFERENCES `customers` (`id`);
ALTER TABLE `products` ADD FOREIGN KEY (`products_type_id`) REFERENCES `products_types` (`id`);
ALTER TABLE `order_product` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);
ALTER TABLE `order_product` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
ALTER TABLE `warehouse_product` ADD FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`);
ALTER TABLE `warehouse_material` ADD FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`);
ALTER TABLE `warehouse_material` ADD FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`);
ALTER TABLE `sewing_tasks` ADD FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`);
ALTER TABLE `cutting_tasks` ADD FOREIGN KEY (`working_group_id`) REFERENCES `working_group` (`id`);
ALTER TABLE `cutting_tasks` ADD FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`);
ALTER TABLE `warehouse_product` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
ALTER TABLE `sewing_material_allocation` ADD FOREIGN KEY (`sewing_task_id`) REFERENCES `sewing_tasks` (`id`);
ALTER TABLE `cutting_material_allocation` ADD FOREIGN KEY (`cutting_task_id`) REFERENCES `cutting_tasks` (`id`);
ALTER TABLE `cutting_material_allocation` ADD FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`);
ALTER TABLE `sewing_material_allocation` ADD FOREIGN KEY (`warehouse_material_id`) REFERENCES `warehouse_material` (`id`);
ALTER TABLE `sewing_tasks` ADD FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`);
```

# OBJECTIVE #
Please carefully understand and study the provided MySQL database table structure. Based on the user's questions or instructions, first provide a step-by-step thought process, then give the correct executable SQL statement. Ensure that the provided SQL statement meets the user's question or instructions.

# RESPONSE FORMAT #
Please output the thought process and answer in the json format below, only output json, do not output any other extra character, Please keep one line of the generated SQL and do not split it into different lines:
{
  "thought": "",
  "sql": "sql1;sql2;...;"
}

"""


def generate_sql(query: str, model="gpt-4o") -> str:
    try:
        messages = [
            {"role": "system", "content": GENERATE_SQL_PROMPT},
            {"role": "user", "content": query}
        ]
        completion = client.chat.completions.create(model=model, messages=messages)
        response_text = completion.choices[0].message.content
        match = re.search(r'.*(\{.*?\}).*', response_text, re.DOTALL)
        json_obj = {}
        if match:
            json_str = match.group(1)
            print("生成的sql:", json_str)
            json_obj = json.loads(json_str)
            json_obj['completion_tokens'] = str(completion.usage.completion_tokens)
            json_obj['prompt_tokens'] = str(completion.usage.prompt_tokens)
            json_obj['total_tokens'] = str(completion.usage.total_tokens)
        return json_obj
    except Exception as e:
        raise Exception(f"生成SQL失败: {repr(e)}")


def generate_response(user_query: str, system_query, model="gpt-4o") -> str:
    try:
        messages = [
            {"role": "system", "content": system_query},
            {"role": "user", "content": user_query}
        ]
        completion = client.chat.completions.create(model=model, messages=messages)
        response_text = completion.choices[0].message.content
        return response_text
    except Exception as e:
        raise Exception(f"生成response失败: {repr(e)}")


if __name__ == "__main__":
    query = "香港理工大学的订单明细"
    print(generate_sql(query))
