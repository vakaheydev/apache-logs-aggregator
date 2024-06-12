import re
from datetime import datetime

import yaml

import domain.log


def load_config(config_file: str = 'resources/config.yml'):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config


config = load_config()


class LogParser:
    field_patterns = {
        '%h': r'(?P<ip>\S+)',
        '%l': r'(?P<log_name>\S+)',
        '%u': r'(?P<user>\S+)',
        '%t': r'(?P<time>\[(?:.*) .*])',
        '%r': r'(?P<request>[\S ]+)',
        '%>s': r'(?P<status>\d{3})',
        '%b': r'(?P<byte>\S+)'
    }

    regex_pattern = None

    def build_regex_pattern(self):
        log_format = config['logs']['format']

        pattern = re.compile(r'%\w|%>s')
        fields = pattern.findall(log_format)

        regex_pattern = log_format

        for field in fields:
            regex_pattern = regex_pattern.replace(field, self.field_patterns[field])

        self.regex_pattern = re.compile(regex_pattern)

    def parse_log(self, log: str) -> domain.log.Log | None:
        if self.regex_pattern is None:
            self.build_regex_pattern()

        match = self.regex_pattern.match(log)
        if not match:
            raise RuntimeError(f"Формат логов не соответствует действительности для записи: {log}")
        else:
            groups_dict = match.groupdict()
            return domain.log.Log(
                groups_dict['ip'],
                datetime.strptime(groups_dict['time'], '[%d/%b/%Y:%H:%M:%S %z]'),
                groups_dict['request'],
                groups_dict['status']
            )

    def set_logging_format(self, field_patterns: dict):
        self.field_patterns = field_patterns
