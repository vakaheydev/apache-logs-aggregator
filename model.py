import datetime
import sqlite3

from db.db import get_connection
from domain.log import Log
from logparser import LogParser

VALUES = "ip, datetime, action, status"


class Model:
    """Model to perform operations with persistent storage"""
    def insert_all(self, logs: list):
        """Insert all logs from list into the DB"""
        log_parser = LogParser()
        for log in logs:
            self.insert(log_parser.parse_log(log))

    def insert(self, log: Log):
        """Insert a single log into the DB"""
        with get_connection() as con:
            cursor = con.cursor()
            try:
                cursor.execute(f"insert into Log({VALUES}) values (?, ?, ?, ?)",
                               (log.ip, log.date_time, log.action, log.status))
                con.commit()
            except sqlite3.IntegrityError:
                pass
            except sqlite3.DatabaseError as ex:
                print(f"Непредвиденная ошибка в БД из-за лога {log}: {ex}")

    def find_all(self):
        """Retrieve all logs from the DB"""
        return self.__execute_select(f"select {VALUES} from Log")

    def find_by_ip(self, ip: str):
        """Retrieve logs filtered by IP address from DB"""
        return self.__execute_select(f"select {VALUES} from Log where ip = ?", (ip,))

    def find_by_date(self, date: datetime.date):
        """Retrieve logs filtered by date from DB"""
        return self.__execute_select(f"select {VALUES} from Log where date(datetime) = ?", (date,))

    def find_by_interval(self, start_date: datetime.date, end_date: datetime.date):
        """Retrieve logs filtered by interval from DB"""
        return self.__execute_select(f"select {VALUES} from Log where date(datetime) between ? and ?",
                                     (start_date, end_date))

    def __execute_select(self, query: str, params: tuple = ()):
        """Execute a select query with specified params (if any)"""
        with get_connection() as con:
            cursor = con.cursor()
            try:
                return cursor.execute(query, params).fetchall()
            except sqlite3.DatabaseError as ex:
                print(f"Database error executing select query {query} with params {params}: {ex}")
