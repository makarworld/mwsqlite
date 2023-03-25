# encoding: utf-8
# Version: 1.1.0
# Path: mwsqlite\sql_compile.py

class SQLRequest:
    CREATE = "CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {fields})"
    INSERT = "INSERT INTO {table} ({fields}) VALUES ({questions})"
    SELECT = "SELECT {DISTINCT} * FROM {table} WHERE {where} ORDER BY {order} LIMIT {limit} OFFSET {offset}"
    UPDATE = "UPDATE {table} SET {fields} WHERE {where}"
    DELETE = "DELETE FROM {table} WHERE {where}"

    @staticmethod
    def create(table, fields):
        return SQLRequest.CREATE.format(
            table=table, fields=fields)
    
    @staticmethod
    def insert(table, fields, questions):
        return SQLRequest.INSERT.format(
            table=table, fields=fields, questions=questions)
    
    @staticmethod
    def select(DISTINCT, table, where, order, limit, offset):
        return SQLRequest.SELECT.format(
            DISTINCT=DISTINCT, table=table, where=where, order=order, limit=limit, offset=offset)
    
    @staticmethod
    def update(table, fields, where):
        return SQLRequest.UPDATE.format(
            table=table, fields=fields, where=where)
    
    @staticmethod
    def delete(table, where):
        return SQLRequest.DELETE.format(
            table=table, where=where)

class SQLCompile:
    @staticmethod
    def create(table: str, fields: list):
        # fields = ["name", "age", ...]
        cmd = SQLRequest.create(
            table = table, 
            fields = ' TEXT, '.join(fields) + ' TEXT'
        )

        return cmd

    @staticmethod
    def insert(table: str, fields: list):
        cmd = SQLRequest.insert(
            table = table, 
            fields = ', '.join(fields), 
            questions = ', '.join(list( '?' * len(fields) ))
        )

        return cmd
    
    @staticmethod
    def select(table: str, where: list=["NONE"], order: list=["NONE"], limit: int="NONE", offset: int="NONE", DISTINCT: str=""):
        # where = ["name = ?", "age > ?", "kwarg < ?"]
        # order = ["name ASC", "age DESC", ...]
        cmd = SQLRequest.select(
            DISTINCT = DISTINCT,
            table = table, 
            where = ' AND '.join(where), 
            order = ', '.join(order), 
            limit = limit, 
            offset = offset
        )
        # replace if args is not specified
        cmd = cmd.replace("WHERE NONE", "")
        cmd = cmd.replace("ORDER BY NONE", "")
        cmd = cmd.replace("LIMIT NONE", "")
        cmd = cmd.replace("OFFSET NONE", "")
        cmd = cmd.replace("  ", " ")

        return cmd
    
    @staticmethod
    def update(table: str, fields: list, where=["NONE"]):
        # fields = ["name = ?", "age = ?", ...]
        cmd = SQLRequest.update(
            table = table, 
            fields = ', '.join(fields), 
            where = ' AND '.join(where)
        )
        # replace if args is not specified
        cmd = cmd.replace("WHERE NONE", "")
        cmd = cmd.replace("  ", " ")

        return cmd
    
    @staticmethod
    def delete(table: str, where: list=["NONE"]):
        cmd = SQLRequest.delete(
            table = table, 
            where = ' AND '.join(where)
        )
        # replace if args is not specified
        cmd = cmd.replace("WHERE NONE", "")

        return cmd
