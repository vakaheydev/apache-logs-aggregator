from datetime import date, datetime

from logparser import config

LOGS_PATH = config['logs']['path']
ACCESS_LOG_PATH = f"{LOGS_PATH}/{config['logs']['access_log']}"


class LogService:
    def __init__(self, model):
        self.model = model

    def __get_access_logs_from_file(self) -> list:
        """Return all logs from access_log file as list of pure strings"""
        with open(ACCESS_LOG_PATH, "r") as f:
            logs = f.readlines()

        return logs

    def filter_logs_by_ip(self, ip: str, logs: list) -> list:
        """Return new list contains only logs with specified id"""
        return list(filter(lambda log: True if log[0] == ip else False, logs))

    def filter_logs_by_date(self, date: date, logs: list) -> list:
        """Return new list contains only logs with specified date"""
        filtered_logs = []

        for log in logs:
            log_date = datetime.strptime(log[1], "%Y-%m-%d %H:%M:%S").date()
            if log_date == date:
                filtered_logs.append(log)

        return filtered_logs

    def filter_logs_by_interval(self, start_date: date, end_date: date, logs: list) -> list:
        """Return new list contains only logs with specified interval (between start_date and end_date)"""
        filtered_logs = []

        for log in logs:
            log_date = datetime.strptime(log[1], "%Y-%m-%d %H:%M:%S").date()
            if start_date <= log_date <= end_date:
                filtered_logs.append(log)

        return filtered_logs

    def aggregate_logs(self) -> None:
        """Collect logs from file (specified in config.yml) and store it in DB"""
        logs = self.__get_access_logs_from_file()
        self.model.insert_all(logs)

    def get_logs(self) -> list:
        """Get all logs from DB"""
        return self.model.find_all()

    def get_logs_by_ip(self, ip: str) -> list:
        """Get logs by id from DB"""
        return self.model.find_by_ip(ip)

    def get_logs_by_date(self, log_date: date) -> list:
        """Get logs by date from DB"""
        return self.model.find_by_date(log_date)

    def get_logs_by_interval(self, start_date: date, end_date: date) -> list:
        """Get logs by interval (between start_date and end_date) from DB"""
        return self.model.find_by_interval(start_date, end_date)

    def parse_date(self, date: str) -> datetime.date:
        if date is None:
            return None
        return datetime.strptime(date, "%Y-%m-%d").date()
