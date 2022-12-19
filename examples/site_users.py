from mwsqlite import MWBase, Order, DESC, ASC

# create database
base = MWBase(
    "users.db",
    tables={
        "users": {
            "ip": list,
            "username": str,
            "email": str,
            "password": str,
            "is_admin": bool,
            "access_token": str,
            "refresh_token": str,
            "token_expires": int
        }
    })

# add user to database
for i in range(100):
    base.users.add(
        ip=[f"1.2.3.{i}"],
        username=f"johndoe{i}",
        email=f"user{i}@gmail.com",
        password=f"123456-{i}",
        is_admin=False,
        access_token="XXXXX_TOKEN_XXXXX",
        refresh_token="XXXXX_REFRESH_TOKEN_XXXXX",
        token_expires=100_000_000 + i
    )

# get from database order by 
users = base.users.get(
    Order(token_expires=DESC, username=ASC)
)

print(users)

for user in users:
    print(user.ip[0])
    # 1.2.3.99
    # 1.2.3.98
    # ...
    # 1.2.3.1
    # 1.2.3.0