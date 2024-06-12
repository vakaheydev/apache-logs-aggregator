from datetime import datetime


class Log:
    """Domain object representing a log entry"""

    def __init__(self, ip: str = None, date_time: datetime = None, action: str = None, status: int = None):
        self.ip = ip
        self.date_time = date_time
        self.action = action
        self.status = status

    def __str__(self):
        return f"IP: {self.ip}, Date: {self.date_time}, Action: {self.action}, Status: {self.status}"
