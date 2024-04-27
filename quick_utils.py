import json
import random
import struct
import socket
from datetime import datetime
from cassandra.cluster import (
    EXEC_PROFILE_DEFAULT,
    Cluster,
    ExecutionProfile,
    ConsistencyLevel,
)
from cassandra.query import BatchStatement, named_tuple_factory
from cassandra.auth import PlainTextAuthProvider
from typing import Dict

from pymysql import Connect
import pymysql.cursors


class LoadJsonFile:
    def __new__(cls, path: str) -> Dict:
        with open(path, "r") as file:
            return json.load(file)


class Utils:
    def generate_ip(self):
        ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
        # Join the numbers together with periods to form an IP address
        ip_address = ".".join(ip_parts)
        return ip_address

    def generate_private_ip(self):
        # Choose a random private IP address range
        private_ranges = [
            ("10.0.0.0", "10.255.255.255"),
            ("172.16.0.0", "172.31.255.255"),
            ("192.168.0.0", "192.168.255.255"),
        ]
        start_ip, end_ip = random.choice(private_ranges)

        # Convert IP addresses to integers
        start_int = struct.unpack("!I", socket.inet_aton(start_ip))[0]
        end_int = struct.unpack("!I", socket.inet_aton(end_ip))[0]

        # Generate a random IP address within the chosen range
        random_int = random.randint(start_int, end_int)
        random_ip = socket.inet_ntoa(struct.pack("!I", random_int))

        return random_ip

    def generate_mac(self):
        mac = [random.randint(0x00, 0xFF) for _ in range(6)]
        mac_address = ":".join(["{:02x}".format(byte) for byte in mac])
        return mac_address

    def generate_mac_oui(self, ouis=["ab:ab:ab"]):
        return str(
            random.choice(ouis)
            + ":%02x:%02x:%02x"
            % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ).upper()

    def get_today_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def get_random_serial_number(self):
        return str(random.randint(10000000, 999999999999999))

    def repeat_in_query_placeholders(self, queryList):
        return ", ".join(["%s"] * len(queryList))


class MysqlConnect:
    def __init__(
        self, host: str, db: str, user: str, password: str, port: int = 3306
    ) -> None:
        self.connection = pymysql.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def close(self) -> None:
        self.connection.close()

    def statement(self, sql: str, params=()) -> bool:
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(sql, params)
            cursor.close()
            self.connection.commit()

            return bool(result)
        except Exception as e:
            self.error = e
            return False

    def get(self, sql: str, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except Exception as e:
            self.error = e
            return False

    def select(self, sql: str, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            self.error = e
            return False

    def health_check(self, reconnect: bool = False) -> bool:
        try:
            self.connection.ping(reconnect)
            return True
        except Exception as e:
            self.error = e
            return False

    def get_last_error(self) -> Exception:
        return self.error

    def get_connection(self) -> Connect:
        return self.connection


class CassandraConnect:
    """
    Cassandra Driver Documentation:
    https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/
    """

    def __init__(
        self,
        hosts: list[str],
        keyspace: str,
        user: str,
        password: str,
        port: int = 9042,
        row_format=named_tuple_factory,
        consistency_level: str = "QUORUM",
        timeout=30,
    ) -> None:

        self.timeout = timeout

        auth = PlainTextAuthProvider(username=user, password=password)

        # Validate consistency level
        try:
            self.consistency_value = ConsistencyLevel.name_to_value[
                consistency_level.upper()
            ]
        except AttributeError:
            raise ValueError("invalid consistency level passed to Cassandra")

        profile = ExecutionProfile(
            consistency_level=self.consistency_value,
            request_timeout=self.timeout,
            row_factory=row_format,
        )

        self.cluster = Cluster(
            contact_points=hosts,
            port=port,
            auth_provider=auth,
            execution_profiles={EXEC_PROFILE_DEFAULT: profile},
        )

        self.keyspace = keyspace

        self.session = self.cluster.connect(keyspace=keyspace)

    def switch_keyspace(self, keyspace: str) -> None:
        self.keyspace = keyspace
        self.session.set_keyspace(keyspace)

    def close(self) -> None:
        self.session.shutdown()

    def statement(self, cql: str | BatchStatement, params=()) -> bool:
        result = self.session.execute(cql, params)
        return bool(result)

    def get_batch(
        self,
    ) -> BatchStatement:
        batch = BatchStatement(
            consistency_level=self.consistency_value, session=self.session
        )
        return batch

    def get(self, cql: str, params=()):
        """
        Rows are named tuples. Following are valid access

        rows = instance.get("SELECT name, age, email FROM users")

        for row in rows:
            print(row.name, row.age, row.email)

        for (name, age, email) in rows:
            print(row.name, row.age, row.email)

        for row in rows:
            print(row[0], row[1], row[2])
        """
        result = self.session.execute(cql, params)
        return result.one()

    def select(self, cql: str, params=()):
        """
        Rows are named tuples. Following are valid access

        rows = instance.get("SELECT name, age, email FROM users")

        for row in rows:
            print(row.name, row.age, row.email)

        for (name, age, email) in rows:
            print(row.name, row.age, row.email)

        for row in rows:
            print(row[0], row[1], row[2])
        """
        result = self.session.execute(cql, params)
        return result
