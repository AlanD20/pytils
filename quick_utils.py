import json
import random
import struct
import socket
from datetime import datetime
from typing import Dict

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
        cursor = self.connection.cursor()
        result = cursor.execute(sql, params)
        cursor.close()
        self.connection.commit()

        return bool(result)

    def get(self, sql: str, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def select(self, sql: str, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
