import sqlite3
import re
from prettytable import PrettyTable


def sql_result_to_table_str(sql_result):
    if not sql_result:
        return ""
    table = PrettyTable()
    table.field_names = sql_result[0].keys()
    for row in sql_result:
        table.add_row(row.values())
    table.float_format = ".2"
    return str(table)


def _rows_to_dicts(cursor, rows):
    if rows is None:
        return []
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in rows]


def _adapt_sql(sql):
    """Convert common MySQL-specific syntax to SQLite-compatible syntax."""
    # Remove MySQL character set / engine clauses (for CREATE TABLE if any)
    sql = re.sub(r"ENGINE\s*=\s*\w+", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"CHARACTER SET\s+\w+", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"COLLATE\s+\w+", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"DEFAULT CHARSET\s*=\s*\w+", "", sql, flags=re.IGNORECASE)
    # AUTO_INCREMENT → AUTOINCREMENT handled in schema; queries usually don't have it
    return sql.strip()


class SQLiteDB(object):
    def __init__(self, db_path="fashion.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_sql(self, sql, raise_err=False):
        sql = _adapt_sql(sql)
        try:
            self.connect()
            last_result = None
            last_is_insert = False
            for sub_sql in sql.split(";"):
                sub_sql = sub_sql.strip()
                if not sub_sql:
                    continue
                self.cursor.execute(sub_sql)
                last_result = self.cursor.fetchall()
                if re.search(r"^\s*INSERT", sub_sql, re.IGNORECASE):
                    last_is_insert = True
            self.conn.commit()

            result = _rows_to_dicts(self.cursor, last_result)

            if last_is_insert:
                result = [{"auto_increment_id": self.cursor.lastrowid}]

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            error_message = f"SQL error: {str(e)}"
            if raise_err:
                raise e
            else:
                return e, error_message
        finally:
            self.disconnect()

        if result:
            out_str = sql_result_to_table_str(result)
        else:
            lower = sql.lower()
            if "create" in lower:
                out_str = "create table successfully."
            elif "insert" in lower:
                out_str = "insert data successfully."
            elif "delete" in lower:
                out_str = "delete data successfully."
            elif "update" in lower:
                out_str = "update data successfully."
            else:
                out_str = "no results found."

        return result, out_str

    def select(self, table, columns="*", condition=None):
        sql = f"SELECT {columns} FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        return self.execute_sql(sql)

    def insert(self, table, data):
        keys = ",".join(data.keys())
        values = ",".join([f"'{v}'" for v in data.values()])
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        return self.execute_sql(sql)

    def update(self, table, data, condition):
        set_values = ",".join([f"{k}='{v}'" for k, v in data.items()])
        sql = f"UPDATE {table} SET {set_values} WHERE {condition}"
        return self.execute_sql(sql)

    def delete(self, table, condition):
        sql = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_sql(sql)

    def last_insert_row_id(self):
        return self.cursor.lastrowid if self.cursor else None
