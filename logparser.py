import re
from datetime import datetime

import yaml

import domain.log


def load_config(config_file: str = 'resources/config.yml'):
    """Load configuration from a YAML file"""
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


config = load_config()


class LogParser:
    """Log parser capable of building regex pattern based on logging format"""

    def __init__(self):
        self.field_patterns = {
            '%h': r'(?P<ip>\S+)',
            '%l': r'(?P<log_name>\S+)',
            '%u': r'(?P<user>\S+)',
            '%t': r'(?P<time>\[(?:.*) .*])',
            '%r': r'(?P<request>[\S ]+)',
            '%>s': r'(?P<status>\d{3})',
            '%b': r'(?P<byte>\S+)'
        }
        self.regex_pattern = self.__build_regex_pattern()

    def __build_regex_pattern(self):
        """Build a regex pattern based on the log format from configuration"""
        log_format = config['logs']['format']
        pattern = re.compile(r'%\w|%>s')
        fields = pattern.findall(log_format)

        regex_pattern = log_format

        for field in fields:
            regex_pattern = regex_pattern.replace(field, self.field_patterns[field])

        return re.compile(regex_pattern)

    def parse_log(self, log: str) -> domain.log.Log | None:
        """Parse a log entry and return a Log object"""
        match = self.regex_pattern.match(log)
        if not match:
            raise ValueError(f"Формат логов не соответствует действительности для записи: {log}")

        groups_dict = match.groupdict()

        # TODO: Решать проблему с часовым поясом

        return domain.log.Log(
            groups_dict['ip'],
            datetime.strptime(groups_dict['time'], '[%d/%b/%Y:%H:%M:%S %z]'),
            groups_dict['request'],
            groups_dict['status']
        )

    def set_logging_format(self, field_patterns: dict):
        """Set custom logging format"""
        self.field_patterns = field_patterns
