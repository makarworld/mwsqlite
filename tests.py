import os
try: os.remove("file.db")
except Exception as e: pass

from mwsqlite import MWBase, Row, Where, Order, ASC, DESC

# create table
base = MWBase(
    filename="file.db",
    tables={
        "test": {
            "str": str,
            "int": int,
            "dict": dict,
            "bool": bool,
            "list": list
        },
        "users": {
            "first_name": str,
            "age": int,
            "admin": bool
        },
        "grades": {
            "user_id": int,
            "grade": int
        },
        "subjects": {
            "name": str,
            "teacher": str
        },
        "json_tests": {
            "key": str,
            "list_of_json": list,
            "json": dict
        }
    }
)

def test_base_add_to_test_table():
    # add user to database
    base.test.add(
        str="String value",
        int=123,
        dict={"This": "is", "my": "dictionary.", 1: 2, "_dict": {"i": "use", "my": "own", "struct": ""}, "": "empty string"},
        bool=True,
        list=["1", {}, [{"test": "test value in list column"}], 4, 5, 6, 7, 8, 9, 0]
    )

    # get from database
    test_value = base.test.get_one(Where(str="String value"))

    # user __str__ because mwsqlite use selfmade dict structure
    assert test_value.__str__() == "MWBase.test.Row({'id': 1, 'str': 'String value', 'int': 123, 'dict': {'This': 'is', 'my': 'dictionary.', '1': 2, '_dict': {'i': 'use', 'my': 'own', 'struct': ''}, '': 'empty string'}, 'bool': True, 'list': ['1', {}, [{'test': 'test value in list column'}], 4, 5, 6, 7, 8, 9, 0]})"
    assert test_value.str == "String value"
    assert test_value.int == 123
    assert test_value.dict.__str__() == "{'This': 'is', 'my': 'dictionary.', '1': 2, '_dict': {'i': 'use', 'my': 'own', 'struct': ''}, '': 'empty string'}"
    assert test_value.dict.This == "is"
    assert test_value.dict._dict.my == "own"
    assert test_value.bool == True
    assert test_value.list.__str__() == "['1', {}, [{'test': 'test value in list column'}], 4, 5, 6, 7, 8, 9, 0]"
    assert test_value.list[2][0].test == "test value in list column"

def test_add_user():
    # add user to database
    base.users.add(
        first_name="John",
        age=20,
        admin=False
    )

    # get from database
    user = base.users.get_one(first_name="John")

    # user __str__ because mwsqlite use selfmade dict structure
    assert user.__str__() == "MWBase.users.Row({'id': 1, 'first_name': 'John', 'age': 20, 'admin': False})"
    assert user.first_name == "John"
    assert user.age == 20
    assert user.admin == False

def test_update_user():
    # get from database
    user = base.users.get_one(first_name="John")

    # update user
    user.update(
        first_name="Jane",
        age=21,
        admin=True
    )

    # get from database
    user2 = base.users.get_one(first_name="Jane")

    # user __str__ because mwsqlite use selfmade dict structure
    assert user.__str__() == user2.__str__()
    assert user2.__str__() == "MWBase.users.Row({'id': 1, 'first_name': 'Jane', 'age': 21, 'admin': True})"
    assert user.first_name == "Jane"
    assert user.age == 21
    assert user.admin == True

def test_delete_user():
    # get from database
    user = base.users.get_one(first_name="Jane")

    # delete user
    user.delete()

    # get from database
    user2 = base.users.get_one(first_name="Jane")

    # user __str__ because mwsqlite use selfmade dict structure
    assert user2 == None

def test_add_grade():
    # add user to database
    base.grades.add(
        user_id=1,
        grade=5
    )

    # get from database
    grade = base.grades.get_one(user_id=1)

    # user __str__ because mwsqlite use selfmade dict structure
    assert grade.__str__() == "MWBase.grades.Row({'id': 1, 'user_id': 1, 'grade': 5})"
    assert grade.user_id == 1
    assert grade.grade == 5

def test_update_grade():
    # get from database
    grade = base.grades.get_one(user_id=1)

    # update user
    grade.update(
        user_id=1,
        grade=4
    )

    # get from database
    grade2 = base.grades.get_one(user_id=1)

    # user __str__ because mwsqlite use selfmade dict structure
    assert grade.__str__() == grade2.__str__()
    assert grade2.__str__() == "MWBase.grades.Row({'id': 1, 'user_id': 1, 'grade': 4})"
    assert grade.user_id == 1
    assert grade.grade == 4

def test_delete_grade():
    # get from database
    grade = base.grades.get_one(user_id=1)

    # delete user
    grade.delete()

    # get from database
    grade2 = base.grades.get_one(user_id=1)

    # user __str__ because mwsqlite use selfmade dict structure
    assert grade2 == None

def test_add_subject():
    # add user to database
    base.subjects.add(
        name="Math",
        teacher="John"
    )

    # get from database
    subject = base.subjects.get_one(name="Math")

    # user __str__ because mwsqlite use selfmade dict structure
    assert subject.__str__() == "MWBase.subjects.Row({'id': 1, 'name': 'Math', 'teacher': 'John'})"
    assert subject.name == "Math"
    assert subject.teacher == "John"

def test_update_subject():
    # get from database
    subject = base.subjects.get_one(name="Math")

    # update user
    subject.update(
        name="Math",
        teacher="Jane"
    )

    # get from database
    subject2 = base.subjects.get_one(name="Math")

    # user __str__ because mwsqlite use selfmade dict structure
    assert subject.__str__() == subject2.__str__()
    assert subject2.__str__() == "MWBase.subjects.Row({'id': 1, 'name': 'Math', 'teacher': 'Jane'})"
    assert subject.name == "Math"
    assert subject.teacher == "Jane"

def test_delete_subject():
    # get from database
    subject = base.subjects.get_one(name="Math")

    # delete user
    subject.delete()

    # get from database
    subject2 = base.subjects.get_one(name="Math")

    # user __str__ because mwsqlite use selfmade dict structure
    assert subject2 == None

def test_order_by():
    # add user to database
    base.users.add(
        first_name="John",
        age=20,
        admin=False
    )

    # add user to database
    base.users.add(
        first_name="Jane",
        age=21,
        admin=True
    )

    # get from database
    users = base.users.get(
        Order(age=DESC),
    )

    assert users[0].age == 21
    assert users[1].age == 20

def test_json():
    # add user to database
    base.json_tests.add(
        key = "test1",
        list_of_json = [
            {
                "test": "test value in list column"
            },
            {
                "test1": {"test2": "deep-json 1"}
            }
        ],
        json = {
            "test": {"test2": "deep-json 2"}
        }
    )

    # get from database
    row = base.json_tests.get_one(key="test1")

    # user __str__ because mwsqlite use selfmade dict structure
    assert row.key == "test1"
    assert isinstance(row.list_of_json, list)
    assert isinstance(row.list_of_json[0], dict)
    assert isinstance(row.json, dict)
    assert isinstance(row.json.test, dict)
    assert row.list_of_json[0].test == "test value in list column"
    assert row.list_of_json[1].test1.test2 == "deep-json 1"
    assert row.json.test.test2 == "deep-json 2"

    # update copy of dict
    row.json.update(test3 = {"test4": "deep-json 3"})
    # update dict in database
    row.update(json = row.json)

    # get from database
    row = base.json_tests.get_one(key="test1")

    assert row.json.test3.test4 == "deep-json 3"


test_json()

test_base_add_to_test_table()

test_add_user()
test_update_user()
test_delete_user()

test_add_grade()
test_update_grade()
test_delete_grade()

test_add_subject()
test_update_subject()
test_delete_subject()

test_order_by()

"""
users = base.users.get(
    Where(first_name="John"), 
    OrderBy("id", "DESC"), 
    OrderBy("coins", "DESC")
)

users = base.users.get(
    Where(first_name="John"), 
    OrderBy(id=DESC, coins=DESC),
)

"""

