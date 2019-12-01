import logging
from sched import scheduler
from time import time, sleep
from typing import Callable

from monitor.constants import TIME_FRAMES
from monitor.ui import ConsoleInterface
from monitor.website import MonitoredWebsite


class ScheduledExecutor:
    """
    Periodic scheduler for running all task over and over again with
    """
    def __init__(self):
        self._scheduler = scheduler(time, sleep)

    def schedule(self, interval: int, priority: int, action: Callable, *args):
        """
        Schedule task every given interval. After one execution next task is scheduled with identical parameters
        :param interval: specify how often task should be executed
        :param priority: priority of task
        :param action: task to run
        :param args: arguments of the scheduled task
        """
        try:
            action(*args)
        except Exception as exc:
            logging.exception(exc)
        finally:
            delay = interval - time() % interval
            self._scheduler.enter(delay, priority, self.schedule, (interval, priority, action, *args))

    def run(self):
        self._scheduler.run()


class HTTPMonitor:
    """
    Monitor object responsible for scheduling all actions and storing UI and MonitoredWebsite class instances
    """
    def __init__(self, config: dict, refresh_rate: int = 1):
        self.refresh_rate = refresh_rate
        self.monitored_websites = [MonitoredWebsite(website, interval) for website, interval in config.items()]
        self.console_interface = ConsoleInterface(MonitoredWebsite.get_metric_names())

    def start(self):
        """
        Schedule and start availability_check, refresh_stats and render metrics actions
        """
        executor = ScheduledExecutor()

        # schedule availability checks
        for website in self.monitored_websites:
            executor.schedule(website.interval, 1, website.perform_availability_check)

        # schedule metrics update
        for website in self.monitored_websites:
            for timeframe, meta in TIME_FRAMES.items():
                executor.schedule(meta["refresh_rate"], 1, website.refresh_stats, timeframe)

        executor.schedule(self.refresh_rate, 2, self.console_interface.render_metrics, self.monitored_websites)
        executor.run()
