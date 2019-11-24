import logging
from collections import deque
from sched import scheduler
from time import time, sleep
from typing import Callable

from monitor.metrics import store_metrics, WebsiteMetric
from monitor.ui import render_metrics

HOURS_TO_SECOND = 3600


class ScheduledExecutor:
    def __init__(self):
        self._scheduler = scheduler(time, sleep)

    def schedule(self, interval: int, priority: int, action: Callable, *args):
        try:
            action(*args)
        except Exception as exc:
            logging.exception(exc)
        finally:
            delay = interval - time() % interval
            self._scheduler.enter(delay, priority, self.schedule, (interval, priority, action, *args))

    def run(self):
        self._scheduler.run()


class PerformanceMonitor:
    def __init__(self, config: dict):
        self.config = config
        self.metrics_store = {
            website: WebsiteMetric(website, interval) for website, interval in config.items()
        }

    def start(self):
        executor = ScheduledExecutor()
        refresh_rate = min(self.config.values())

        for website, interval in self.config.items():
            executor.schedule(interval, 1, store_metrics, website, self.metrics_store[website])

        executor.schedule(refresh_rate, 2, render_metrics, self.metrics_store)
        executor.run()
