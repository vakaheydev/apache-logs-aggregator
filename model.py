import datetime
import sqlite3

from db.db import get_connection
from domain.log import Log
from logparser import LogParser

VALUES = "ip, datetime, action, status"


class Model:
    def insert_all(self, logs: list):
        log_parser = LogParser()
        for log in logs:
            self.insert(log_parser.parse_log(log))

    def insert(self, log: Log):
        with get_connection() as con:
            cursor = con.cursor()
            try:
                cursor.execute(f"INSERT INTO Log({VALUES}) values (?, ?, ?, ?)",
                               (log.ip, log.date_time, log.action, log.status))
            except sqlite3.IntegrityError:
                pass
            except sqlite3.DatabaseError as ex:
                print(f"Database error on {log}: {ex}")
            con.commit()

    def find_all(self):
        with get_connection() as con:
            cursor = con.cursor()
            logs = []
            try:
                query = f"select {VALUES} from Log"
                logs = cursor.execute(query).fetchall()
            except sqlite3.DatabaseError as ex:
                print(f"Database error executing select all: {ex}")
            return logs

    def find_by_ip(self, ip: str):
        with get_connection() as con:
            cursor = con.cursor()
            logs = []
            try:
                logs = cursor.execute(f"select {VALUES} from Log where ip = ?", (ip,)).fetchall()
            except sqlite3.DatabaseError as ex:
                print(f"Database error executing select by ip {ip}: {ex}")
            return logs

    def find_by_date(self, date: datetime.date):
        with get_connection() as con:
            cursor = con.cursor()
            logs = []
            try:
                logs = cursor.execute(f"select {VALUES} from Log where date(datetime) = ?", (date,)).fetchall()
            except sqlite3.DatabaseError as ex:
                print(f"Database error executing select by date {date}: {ex}")
            return logs

    def find_by_interval(self, start_date: datetime.date, end_date: datetime.date):
        with get_connection() as con:
            cursor = con.cursor()
            logs = []
            try:
                logs = cursor.execute(f"select {VALUES} from Log where date(datetime) between ? and ?",
                                      (start_date, end_date)).fetchall()
            except sqlite3.DatabaseError as ex:
                print(f"Database error executing select by interval {start_date} - {end_date}: {ex}")
            return logs
