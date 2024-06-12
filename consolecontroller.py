import re
from datetime import datetime

from logservice import LogService


class ConsoleController:
    def __init__(self, service, model):
        self.service = service
        self.model = model

    def console_input(self):
        self.__print_instruction()

        leave_keys = ["end", "q", "quit"]
        input_symbol = '> '

        try:
            user_input = input(input_symbol)
        except KeyboardInterrupt:
            return

        while user_input not in leave_keys:
            self.__resolve_parameters(user_input)

            try:
                user_input = input(input_symbol)
            except KeyboardInterrupt:
                break

    def __print_instruction(self):
        with open("resources/instruction.txt", "r", encoding='utf-8') as f:
            print(f.read())

    def __resolve_parameters(self, user_input: str) -> bool:
        method = user_input.split(" ")[0].lower()
        match method:
            case "get":
                if user_input.strip() == 'get':
                    self.__print_logs({})
                    return True

                matches = re.findall(r"(-\w+ \S*)", user_input)
                params = {}

                if matches:
                    for match in matches:
                        splitted = match.split(" ")
                        params[splitted[0][1:]] = splitted[1]
                    self.__print_logs(params)

                    return True
                else:
                    print("Неверно указаны параметры. Пожалуйста, ознакомьтесь с ними (help)")
                    return False

            case "parse":
                self.aggregate_logs()
                return True

            case "help":
                self.__print_instruction()
                return True

            case _:
                print("Неверный вид запроса. Пожалуйста, ознакомьтесь с ними (help)")
                return False

    def aggregate_logs(self):
        """Aggregate logs, printing the process status"""
        print("\n--------------------------------------")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Агрегация логов...")
        try:
            self.service.aggregate_logs()
            print("\nЛоги успешно загружены в БД")
        except Exception as ex:
            print(f"\nПри загрузке логов произошла непредвиденная ошибка: {ex}")
        print("--------------------------------------\n")

    def __print_logs(self, params: dict):
        """Print logs to console filtered by specified parameters.\n
        Possible combinations to be filtered by:\n
        - ip
        - date
        - ip, date
        - start_date, end_date (interval)
        - ip, start_date, end_date.
        Combination in inferred due to specified parameters"""
        service = LogService(self.model)

        try:
            ip = params.get('ip')
            date = service.parse_date(params.get('date'))
            start_date = service.parse_date(params.get('start_date'))
            end_date = service.parse_date(params.get('end_date'))
        except UnboundLocalError:
            print("Ошибка")
            return
        except ValueError:
            print("Дата указана в некорректном формате. Используйте: yyyy-mm-dd.\nПример: 2024-06-10")
            return
        if ip is not None:
            if ip == '':
                print("IP-адресс не может быть пустым")
                return
            elif len(ip) > 15:
                print("IP-адресс не может быть длиннее 15 символов")
                return
            elif str.isalpha(ip):
                print("IP-адресс указан в некорректном формате. Используйте: ddd.ddd.ddd.ddd\nПример: 127.0.0.1")
                return

        if None not in [ip, date]:
            logs_by_ip = service.get_logs_by_ip(ip)
            logs = service.filter_logs_by_date(date, logs_by_ip)
            printed_type = f"\n~ Printed logs with ip '{ip}' at {date}"
        elif None not in [ip, start_date, end_date]:
            logs_by_ip = service.get_logs_by_ip(ip)
            logs = service.filter_logs_by_interval(start_date, end_date, logs_by_ip)
            printed_type = f"\n~ Printed logs with ip '{ip}' between {start_date} and {end_date}"
        elif ip is not None:
            logs = service.get_logs_by_ip(ip)
            printed_type = f"\n~ Printed logs with ip '{ip}'"
        elif date is not None:
            logs = service.get_logs_by_date(date)
            printed_type = f"\n~ Printed logs at {date}"
        elif None not in [start_date, end_date]:
            logs = service.get_logs_by_interval(start_date, end_date)
            printed_type = f"\n~ Printed logs between {start_date} and {end_date}"
        else:
            logs = service.get_logs()
            printed_type = "\n~ Printed all logs"

        for log in logs:
            print(log)

        print(printed_type)
