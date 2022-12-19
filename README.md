Library for interacting with the SQLite database.

Installation:

```bash
pip install mwsqlite
```

Example:

```python
from mwsqlite import MWBase, Where, Order, DESC, ASC

# create database object (1)
base = MWBase(
    filename="file.db",
    tables={
        "users": {
            "first_name": str,
            "last_name": str,
            "middle_name": str,
            "age": int,
            "info": dict,
            "is_admin": bool,
            "list_rewards": list,
        }
    }
)

# add user to database
base.users.add(
    first_name="John",
    last_name="Doe",
    middle_name="Smith",
    age=18,
    info={"description": "some info"},
    is_admin=False,
    list_rewards=[{"id": 1, "name": "reward1"}, {"id": 2, "name": "reward2"}],
)

# get one user from database
user = base.users.get_one(name="John", age=18)
print(user)
# MWBase.users.Row({'first_name': 'John', 'last_name': 'Doe', 'middle_name': 'Smith', 'age': 18, 'info': {'description': 'some info'}, 'is_admin': False, 'list_rewards': [{'id': 1, 'name': 'reward1'}, {'id': 2, 'name': 'reward2'}]})

base.users.update(
    Where(first_name="John"),
    first_name="Jane",
)

user = base.users.get_one(name="Jane", age=18)
print(user)
#  MWBase.users.Row({'first_name': 'Jane', 'last_name': 'Doe', 'middle_name': 'Smith', 'age': 18, 'info': {'description': 'some info'}, 'is_admin': False, 'list_rewards': [{'id': 1, 'name': 'reward1'}, {'id': 2, 'name': 'reward2'}]})

print(user.age)
# 18
user.update(age=19)
print(user.age)
# 19

user.delete()

user = base.users.get_one(name="Jane", age=18)
print(user)
# None

# get many users from database

for i in range(3):
    base.users.add(first_name="John", age=18 + i)

users = base.users.get(
    Order(age=DESC), 
    name="John"
)
print(len(users))
# 3

print(users)
# [{'first_name': 'Jane', 'last_name': '', 'age': 0, 'info': {}, 'is_admin': False, 'list_rewards': []}, ...]

for user in users:
    print(user.age)
    # 20
    # 19
    # 18

```

TODO:
- [x] add a way to specify the database name
- [x] Table class
- [x] Row class
- [x] add Table func
- [x] get Table func
- [x] update Table func
- [x] delete Table func
- [x] update Row func
- [x] delete Row func
- [x] get_first Table func
- [x] get_last Table func
- [x] get_all Table func
- [x] MWBase.table("name").get_one(...)
- [x] clear Table func
- [x] class Where
- [x] class Order (ASC, DESC)


