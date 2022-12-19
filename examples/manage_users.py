from mwsqlite import MWBase

# create database
base = MWBase(
    "users.db",
    tables={
        "users": {
            "user_id": int,
            "first_name": str,
            "last_name": str,
            "username": str,
            "language_code": str,
            "is_bot": bool,
            "is_active": bool,
            "is_admin": bool,
        }
    })

# add user to database
base.users.add(
    user_id=1,
    first_name="John",
    last_name="Doe",
    username="johndoe",
    language_code="en",
    is_bot=False,
    is_active=True,
    is_admin=False
)

# get from database
user = base.users.get_one(user_id=1)

# update username
user.update(
    username="johndoe2"
)

# get from database
user2 = base.users.get_one(user_id=1)

print(user.username == user2.username)
# True

# delete user
user.delete()


