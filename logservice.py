from datetime import date, datetime

from logparser import config

LOGS_PATH = config['logs']['path']
ACCESS_LOG_PATH = f"{LOGS_PATH}/{config['logs']['access_log']}"


class LogService:
    """Service for performing operations on log file and interacting with Model"""

    def __init__(self, model):
        self.model = model

    def __get_access_logs_from_file(self) -> list:
        """Return all logs from access_log file as list of pure strings"""
        try:
            with open(ACCESS_LOG_PATH, "r") as f:
                logs = f.readlines()
                return logs
        except Exception as ex:
            print(f"Произошла непредвиденная ошибка во время парсинга файла с логами: {ex}")

    def filter_logs_by_ip(self, ip: str, logs: list) -> list:
        """Return new list containing only logs with the specified IP address"""
        return [log for log in logs if ip == log[0]]

    def filter_logs_by_date(self, log_date: date, logs: list) -> list:
        """Return new list containing only logs with the specified date"""
        return [log for log in logs if log_date == self.__extract_date_from_log(log)]

    def filter_logs_by_interval(self, start_date: date, end_date: date, logs: list) -> list:
        """Return new list containing only logs within the specified interval (between start_date and end_date)"""
        return [log for log in logs if start_date <= self.__extract_date_from_log(log) <= end_date]

    def __extract_date_from_log(self, log: str) -> date:
        try:
            return datetime.strptime(log[1], "%Y-%m-%d %H:%M:%S%z").date()
        except ValueError as ex:
            print(f"Произошла непредвиденная ошибка: {ex}")
            return None

    def aggregate_logs(self) -> None:
        """Collect logs from file and store them in the DB"""
        logs = self.__get_access_logs_from_file()
        self.model.insert_all(logs)

    def get_logs(self) -> list:
        """Get all logs from the DB"""
        return self.model.find_all()

    def get_logs_by_ip(self, ip: str) -> list:
        """Get logs by IP address from the DB"""
        return self.model.find_by_ip(ip)

    def get_logs_by_date(self, log_date: date) -> list:
        """Get logs by date from the DB"""
        return self.model.find_by_date(log_date)

    def get_logs_by_interval(self, start_date: date, end_date: date) -> list:
        """Get logs by interval (between start_date and end_date) from the DB"""
        return self.model.find_by_interval(start_date, end_date)

    def parse_date(self, date_str: str) -> datetime.date:
        """Parse a date string into a date object"""
        if date_str is None:
            return None
        return datetime.strptime(date_str, "%Y-%m-%d").date()
