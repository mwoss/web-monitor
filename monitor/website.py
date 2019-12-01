from collections import deque
from itertools import islice, chain
from typing import List, Iterator

import requests

from monitor.alert import Alert, AlertMessage
from monitor.constants import SECONDS_IN_HOUR
from monitor.metrics import ResponseTimeMetric, HTTPStatusMetric, MetricEntry


class MonitoredWebsite:
    """
    Class responsible for performing all operations on metrics and storing data
    """
    AVAILABILITY_TIMEOUT = 5
    METRICS = [ResponseTimeMetric, HTTPStatusMetric]

    def __init__(self, website_url: str, interval: int):
        self.website_url = website_url
        self.interval = interval
        self._alert = Alert(website_url)
        self._metrics = [metric() for metric in self.METRICS]
        self._data_store = deque(maxlen=SECONDS_IN_HOUR // interval)

    def refresh_stats(self, timeframe: int) -> None:
        """
        Refresh metrics and alerting data in given timeframe
        :param timeframe: metric's timeframe which must be refreshed
        """
        window_len = max(len(self._data_store) - timeframe // self.interval, 0)
        metric_data = list(islice(self._data_store, window_len, self._data_store.maxlen))

        for metric in self._metrics:
            metric.compute_metrics(timeframe, metric_data)

        self._alert.refresh_availability_alerts(self._metrics[-1].website_availability)

    def perform_availability_check(self) -> None:
        """
        Perform HTTP call to given website and retrieve all necessary data.
        If requests timeouts after AVAILABILITY_TIMEOUT seconds and data_store is
        appended with MetricEntry(AVAILABILITY_TIMEOUT. 408) entry.
        If requests failed with connection error data_store .
        is appended with MetricEntry(0.0, requests.codes.server_error).
        Otherwise, Response object data is used to create MetricEntry object.
        """
        try:
            response = requests.head(self.website_url, timeout=self.AVAILABILITY_TIMEOUT)
        except requests.exceptions.Timeout:
            self._data_store.append(MetricEntry(self.AVAILABILITY_TIMEOUT, requests.codes.timeout))
        except requests.exceptions.ConnectionError:
            self._data_store.append(MetricEntry(0.0, requests.codes.server_error))
        else:
            self._data_store.append(MetricEntry(response.elapsed.total_seconds(), response.status_code))

    def get_alerts(self) -> List[AlertMessage]:
        return self._alert.availability_alerts

    def get_stats_by_timeframe(self, timeframe: int, display_format: bool = False) -> Iterator[float]:
        """
`       Retrieve all statistic data from every metric specified in METRICS class attribute
        :param timeframe: timeframe from which data is obtained
        :param display_format: flag, if set statistics are formatted for displaying in console
        :return: all stats (form every metric) as a list
        """
        return chain.from_iterable([metric.to_list_by_timeframe(timeframe, display_format) for metric in self._metrics])

    @classmethod
    def get_metric_names(cls) -> Iterator[str]:
        """
        Retrieve all metric names from every metric specified in METRICS class attribute
        :return: list of all metric names
        """
        return chain.from_iterable([metric.metric_names for metric in cls.METRICS])
