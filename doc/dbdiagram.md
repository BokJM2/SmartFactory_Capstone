

https://dbdiagram.io/d/garment-66398bc99e85a46d5526e2af

```
// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table customers {
  customer_id uuid [primary key]
  customer_name varchar
}

Table orders {
  id uuid [primary key]
  user_id uuid
  order_name varchar
  created_at timestamp
}
Table products_types{
  id uuid [primary key]
  description varchar
}

Table products{
  id uuid [primary key]
  products_type_id uuid
  attributes varchar
}

Table materials{
  id uuid [primary key]
  name varchar
  unit varchar
  type enum('wip', 'origin') // original material or work-in-progress
}


Table order_product{
  id uuid [primary key]
  order_id uuid
  product_id uuid
  number integer
}

Table working_group{
  id uuid [primary key]
  type enum('sew', 'cut')
  name varchar
}

Table cutting_tasks{
  id uuid [primary key]
  start_time timestamp
  end_time timestamp
  working_group_id uuid
  order_product_id uuid
  planned_number integer
  completed_number integer
  is_started bool
}


Table sewing_tasks{
  id uuid [primary key]
  start_time timestamp
  end_time timestamp
  working_group_id uuid
  order_product_id uuid
  planned_number integer
  completed_number integer
  is_started bool
}

Table cutting_material_allocation{
  id uuid [primary key]
  warehouse_material_id uuid
  cutting_task_id uuid
  allocated_num integer
  is_allocated bool
}

Table sewing_material_allocation{
  id uuid [primary key]
  warehouse_material_id uuid
  sewing_task_id uuid
  allocated_num integer
  is_allocated bool
}

Table warehouse{
  id uuid [primary key]
  name varchar
}

Table warehouse_product{
  id uuid [primary key]
  warehouse_id uuid
  product_id uuid
  left_number integer
}

Table warehouse_material{
  id uuid [primary key]
  warehouse_id uuid
  material_id uuid
  left_number integer
}

Ref: orders.user_id > customers.customer_id // many-to-one



// Ref: users.id < follows.following_user_id

// Ref: users.id < follows.followed_user_id


Ref: "products_types"."id" < "products"."products_type_id"

Ref: "orders"."id" < "order_product"."order_id"

Ref: "products"."id" < "order_product"."product_id"




Ref: "warehouse"."id" < "warehouse_product"."warehouse_id"

Ref: "warehouse"."id" < "warehouse_material"."warehouse_id"

Ref: "materials"."id" < "warehouse_material"."material_id"

Ref: "working_group"."id" < "sewing_tasks"."working_group_id"

Ref: "working_group"."id" < "cutting_tasks"."working_group_id"

Ref: "order_product"."id" < "cutting_tasks"."order_product_id"


Ref: "products"."id" < "warehouse_product"."product_id"

Ref: "sewing_tasks"."id" < "sewing_material_allocation"."sewing_task_id"

Ref: "cutting_tasks"."id" < "cutting_material_allocation"."cutting_task_id"

Ref: "warehouse_material"."id" < "cutting_material_allocation"."warehouse_material_id"

Ref: "warehouse_material"."id" < "sewing_material_allocation"."warehouse_material_id"

Ref: "order_product"."id" < "sewing_tasks"."order_product_id"
```

