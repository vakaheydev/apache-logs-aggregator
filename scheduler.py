import threading
import time

import schedule

from logparser import config


class Scheduler:
    @staticmethod
    def create_scheduler(controller) -> schedule.Scheduler | None:
        """Creates and returns a scheduler if schedule_update_logs_enabled is True, otherwise returns None"""
        schedule_update_logs_enabled = config['app']['schedule_update_logs_enabled']

        if not schedule_update_logs_enabled:
            print("Автоматическое агрегирование логов отключено\n")
            return None
        else:
            schedule_update_logs_delay = config['app']['schedule_update_logs_delay']
            print(
                f"Логи агрегируются автоматически каждые {schedule_update_logs_delay} секунд. Отключить это можно в config.yml: app/schedule_update_logs_enabled\n")
            scheduler = Scheduler(schedule_update_logs_delay, lambda: Scheduler.scheduler_aggregate_logs(controller))
            scheduler.start()
            return scheduler

    @staticmethod
    def scheduler_aggregate_logs(controller):
        controller.aggregate_logs()
        print("> ", end='')

    def __init__(self, seconds, job):
        self.seconds = seconds
        self.job = job
        self.scheduler = schedule.Scheduler()
        self.scheduler.every(self.seconds).seconds.do(self.job)
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        while True:
            self.scheduler.run_pending()
            time.sleep(1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()
