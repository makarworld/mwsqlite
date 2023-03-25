from __future__ import annotations
import json
# This Python file uses the following encoding: utf-8
import sqlite3

from ._types import Struct, Where, Order, InvalidColumnNameError, DESC, ASC, Limit
from .utils import tuple_to_dict
from .sql_compile import SQLCompile

def ensure_connection(func):
    def inner(*args, **kwargs):
        if (isinstance(args[0], MWBase) or isinstance(args[0], Table)) and func.__name__ != "__init__": # take var in self if you use class methods
            file = args[0].filename

        elif kwargs.get("filename"): # take var in kwargs if you use __init__ function with kwarg "filename"
            file = kwargs.get("filename")

        else:
            file = args[1] # take var in args if you use __init__ function with first arg "filename"
            

        with sqlite3.connect(file) as connection:
            cursor = connection.cursor()
            res = func(cursor=cursor, *args, **kwargs)
            connection.commit()
        return res
           
    return inner
    
    
def check_list(lst: list):
    for i in range(len(lst)):
        if isinstance(lst[i], Row) or isinstance(lst[i], Struct):
            lst[i] = check_dict(lst[i].dict())
        elif isinstance(lst[i], list):
            lst[i] = check_list(lst[i])
    return lst

def check_dict(dct: dict):
    for k, v in dct.items():
        if isinstance(v, Row) or isinstance(v, Struct):
            dct[k] = check_dict(v.dict())
        elif isinstance(v, list):
            dct[k] = check_list(v)
    return dct

def check_kwargs(kwargs: dict):
    kwargs = check_dict(kwargs)

    for k, v in kwargs.items():
        if isinstance(v, list) or isinstance(v, dict):
            kwargs[k] = json.dumps(v)
    
    return kwargs
    
    
class MWBase():
    @ensure_connection
    def __init__(self, filename: str, tables: str, cursor=None):
        self.filename = filename
        self.tables = tables
        self.ensure_connection = ensure_connection

        for table in self.tables:
            if "id" in self.tables[table].keys():
                raise Exception("You can't use 'id' as column name")

            cmd = SQLCompile.create(table, self.tables[table].keys())
            cursor.execute(cmd)

            self.__setattr__(table, Table(table, self.tables[table], self))

    def table(self, table: str) -> Table:
        """
        Get table object.
        """
        return self.__getattribute__(table)



class Table:
    """
    Table class for working with sqlite3 databases.
    """
    def __init__(self, table: str, columns: dict, base: MWBase):
        self.filename = base.filename
        self.table = table
        self.columns = {'id': int}
        self.columns.update(columns)

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f"MWBase.{self.table}"

    @ensure_connection
    def add(self, cursor=None, **kwargs) -> None:
        """
        Add new row to table.
        """
        kwargs = check_kwargs(kwargs)

        cmd = SQLCompile.insert(self.table, kwargs.keys())
        values = tuple(map(str, kwargs.values()))
        cursor.execute(cmd, values)
    
    @ensure_connection
    def get_all(self, order: Order = Order(), cursor=None) -> list[Row]:
        """
        Get all rows from table.
        """
        if order:
            return self.get(order=order)

        cmd = SQLCompile.select(self.table)

        cursor.execute(cmd)
        items = cursor.fetchall()

        if not items: return []

        resp = []
        for item in items:
            resp.append(Row(self, **tuple_to_dict(item, self.columns)))

        return resp

    @ensure_connection
    def get(self, order: Order = Order(), where: Where = Where(), distinct: bool=False, cursor=None, **kwargs) -> list[Row]:
        """
        Get rows from table.
        ```python
        base.test_table.get(Order(id=DESC), Where(id=1, name="test"))
        ```

        or 

        ```python
        base.test_table.get(Order(id=ASC), id=1, name="test")
        ```
        """
        if isinstance(order, Where) and isinstance(where, Order):
            order, where = where, order

        elif isinstance(order, Where) and isinstance(where, Where): 
            where.update(order)
            order = Order()

        elif isinstance(order, Order) and isinstance(where, Order):
            order.update(where)
            where = Where()

        if where: kwargs.update(where)

        
        if not all([k in self.columns.keys() and v in [DESC, ASC] for k, v in order.items()]):
            raise InvalidColumnNameError("Order keys must be in columns keys and values must be DESC or ASC")

        if where:
            kwargs.update(where)

        cmd = SQLCompile.select(
            DISTINCT="DISTINCT" if distinct else "",
            table=self.table, 
            where=[
                f"{column} { (str(data)[0] if str(data)[0] in ['>', '<', '='] else '=') } ?" 
                for column, data in kwargs.items()] if kwargs else ["NONE"], 
            order=[
                f'{column} {data}' 
            for column, data in order.items()] if order else ["NONE"],
        )
        values = tuple(map(str, [
            # Where(id=">1") -> "1"
            # Where(id = 1) -> 1
            x if str(x)[0] not in ['>', '<', '='] else x[1:] 
            for x in list(kwargs.values())
        ]))

        cursor.execute(cmd, values)
        items = cursor.fetchall()

        if not items: return []

        resp = []
        for item in items:
            resp.append(Row(self, **tuple_to_dict(item, self.columns)))

        return resp

    @ensure_connection
    def get_one(self, where: Where = Where(), order: Order = Order(), default_index: int=0, distinct: bool=False, cursor=None, **kwargs, ) -> Row | None:
        """
        Get one row from table.
        """
        if isinstance(order, Where) and isinstance(where, Order):
            order, where = where, order

        elif isinstance(order, Where) and isinstance(where, Where): 
            where.update(order)
            order = Order()

        elif isinstance(order, Order) and isinstance(where, Order):
            order.update(where)
            where = Where()

        if where: kwargs.update(where)

        
        if not all([k in self.columns.keys() and v in [DESC, ASC] for k, v in order.items()]):
            raise InvalidColumnNameError("Order keys must be in columns keys and values must be DESC or ASC")

        if where:
            kwargs.update(where)

        cmd = SQLCompile.select(
            DISTINCT="DISTINCT" if distinct else "",
            table=self.table, 
            where=[
                f"{column} { (str(data)[0] if str(data)[0] in ['>', '<', '='] else '=') } ?" 
                for column, data in kwargs.items()] if kwargs else ["NONE"], 
            order=[
                f'{column} {data}' 
            for column, data in order.items()] if order else ["NONE"],
        )
        values = tuple(map(str, [
            # Where(id=">1") -> "1"
            # Where(id = 1) -> 1
            x if str(x)[0] not in ['>', '<', '='] else x[1:] 
            for x in list(kwargs.values())
        ]))

        cursor.execute(cmd, values)
        item = cursor.fetchall()

        if not item: return None

        resp = tuple_to_dict(item[default_index], self.columns)

        return Row(self, **resp)

    @ensure_connection
    def get_first(self, cursor=None, **kwargs) -> Row | None:
        """
        Get first row with parameters from table.
        """
        return self.get_one(default_index=0, **kwargs)
    
    @ensure_connection
    def get_last(self, cursor=None, **kwargs) -> Row | None:
        """
        Get last row with parameters from table.
        """
        return self.get_one(default_index=-1, **kwargs)


    @ensure_connection
    def update(self, where: Where, cursor=None, **kwargs) -> None:
        """
        Update rows in table.
        """
        kwargs = check_kwargs(kwargs)

        cmd = SQLCompile.update(
            table = self.table, 
            fields = [f'{column} = ?' for column in kwargs], 
            # Where(id=">1") -> id > 1
            # Where(id = 1) -> id = 1
            where = [f'{column}' + (str(data)[0] if str(data)[0] in ['>', '<', '='] else '=') + '?' for column, data in where.items()]
        )

        values = tuple(map(str, 
            list(kwargs.values()) + [
            # Where(id=">1") -> "1"
            # Where(id = 1) -> 1
            x if str(x)[0] not in ['>', '<', '='] else x[1:] 
            for x in list(where.values())
        ]))

        cursor.execute(cmd, values)

    @ensure_connection
    def delete(self, cursor=None, **kwargs) -> None:
        """
        Delete rows from table.
        """
        cmd = SQLCompile.delete(
            table = self.table,
            where = [f'{column}' + (str(data)[0] if str(data)[0] in ['>', '<', '='] else '=') + '?' for column, data in kwargs.items()]
        )
        values = tuple(map(str, [
            # Where(id=">1") -> "1"
            # Where(id = 1) -> 1
            x if str(x)[0] not in ['>', '<', '='] else x[1:] 
            for x in list(kwargs.values())
        ]))

        cursor.execute(cmd, values)
    
    @ensure_connection
    def delete_all(self, cursor=None) -> None:
        """
        Delete all rows from table.
        """
        cmd = SQLCompile.delete(table=self.table)

        cursor.execute(cmd)
    

class Row(Struct):
    """
    Row class for working with sqlite3 databases.
    """
    def __init__(self, tclass: Table, **entries):
        self.table = tclass

        self.__dict__.update(entries)
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(**v)

            if isinstance(v, list):
                self.__dict__[k] = []
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        self.__dict__[k].append(Struct(**v[i]))

                    elif isinstance(v[i], list):
                        self.__dict__[k].append([Struct(**x) if isinstance(x, dict) else x for x in v[i]])

                    else:
                        self.__dict__[k].append(v[i])

    def __repr__(self):
        return f"MWBase.{self.table.table}.Row({str({k: v for k,v in self.__dict__.items() if k != 'table'})})"

    def __str__(self):
        return self.__repr__()
    
    def dict(self) -> dict:
        """
        Return dict of row.
        """
        return {k: v for k,v in self.__dict__.items() if k != 'table'}

    def update(self, **kwargs):
        """
        Update row in table.
        """
        self.__dict__.update(kwargs)
        kwargs = check_kwargs(kwargs)
        
        self.table.update(Where(id = self.id), **kwargs)
    
    def delete(self):
        """
        Delete row from table.
        """
        self.table.delete(id=self.id)
        self = None
    
    def save(self):
        """
        Update row in table.
        """
        self.update(**self.dict())


if __name__ == "__main__":

    base = MWBase(
        filename="file.db",
        tables={
            "users": {
                "first_name": str,
                "age": int
            }
        }
    )

    base.users.add(first_name="John", age=20)

    user = base.users.get_one(first_name="John")
    user.update(first_name="Jack", age=21)

    user2 = base.users.get_one(first_name="Jack")
    
    print(user) # user and user2 are the same object
    print(user2)

    user.delete()

    # UPDATE test SET test1 = ?, test2 = ? WHERE test1 = ? AND test2 = ? ['name2', 'name3', 'name1', 'name3']


