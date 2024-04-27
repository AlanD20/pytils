# Python Utilities

## Copy to existing project

Install required modules and copy the `quick_utils.py` to your project.

```bash
pip3 install -r requirements.txt
```

## Install via pip

```bash
pip3 install https://github.com/aland20/pytils/archive/main.zip
```

## Examples

#### MysqlConnect

```python
# Load json files as dictionary
config = LoadJsonFile('./mysql-config.json')

# MySQL Connector
conn = MysqlConnect(
    host=config["host"],
    db=config["database"],
    user=config["user"],
    password=config["password"],
    port=config["port"],
)


# GET query
result = conn.get("SELECT * FROM users WHERE id = %s", (4))
print(result)

# SELECT query
result = conn.select("SELECT * FROM posts WHERE user_id = %s", (12))
print(result)

# Execute statement
result = conn.statement("UPDATE users SET username = %s WHERE id = %s", ("test", 4))
if result is False:
    print("failed to execute statement")

```

### Utils


```python
import argparse
from quick_utils import LoadJsonFile, MysqlConnect, Utils


# New utils instance
_ = Utils()

ip = _.generate_ip()
private_ip = _.generate_private_ip()
mac = _.generate_mac()
mac_oui = _.generate_mac_oui(['ab:b8:ab'])
today = _.get_today_date()
serial_number = _.get_random_serial_number()

# Using Parser Arguments - Reference
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, action="store", default="config.json")
parser.add_argument("-u", "--user", type=str, action="store", default=None)
args = parser.parse_args()

# Load json files as dictionary
config = LoadJsonFile(args.config)

```

### CassandraConnect

```python
cass_conn = _.CassandraConnect(
    hosts=['127.0.0.1'],
    keyspace='dev',
    user='cassandra',
    password='cassandra',
    port=9042,
    consistency_level='QUORUM',
)

# CQL statements
cass_conn.statement(
    """
        CREATE TABLE IF NOT EXISTS users_by_roles (
            role text,
            name text,
            email text,
            PRIMARY KEY((role), name)
        );
    """
)

# Executing batches
batch = cass_conn.get_batch()

batch.add(
    "INSERT INTO users_by_roles (role, name, email) VALUES ('admin', 'aland20', 'aland20@pm.me');"
)
batch.add(
    "INSERT INTO users_by_roles (role, name, email) VALUES ('admin', 'john', 'john@example.com');"
)
batch.add(
    "INSERT INTO users_by_roles (role, name, email) VALUES ('admin', 'jack', 'jack@example.com');"
)
batch.add(
    "INSERT INTO users_by_roles (role, name, email) VALUES ('admin', 'johnny', 'johnny@example.com');"
)

cass_conn.statement(batch)


# Select query
users = cass_conn.select("SELECT * FROM users_by_roles;")
for role, name, email in users:
    print(f"Name: {name}, Role: {role}, Email: {email}")

# Get query
user = cass_conn.get("SELECT * FROM users_by_roles WHERE role = 'admin' AND name = 'aland20';")
```

## License

This repository is under [MIT](./LICENSE) license.
