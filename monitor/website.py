from collections import deque
from itertools import islice, chain
from typing import Tuple, List, Iterator

import requests

from monitor.alert import Alert, AlertType
from monitor.constants import SECONDS_IN_HOUR
from monitor.metrics import ResponseTimeMetric, HTTPStatusMetric, MetricEntry


class MonitoredWebsite:
    AVAILABILITY_TIMEOUT = 5
    METRICS = [ResponseTimeMetric, HTTPStatusMetric]

    def __init__(self, website_url: str, interval: int):
        self.website_url = website_url
        self.interval = interval
        self._alert = Alert(website_url)
        self._metrics = [metric() for metric in self.METRICS]
        self._data_store = deque(maxlen=SECONDS_IN_HOUR // interval)

    def refresh_stats(self, time_frame: int) -> None:
        window_len = max(time_frame // self.interval - self._data_store.maxlen, 0)
        metric_data = list(islice(self._data_store, window_len, self._data_store.maxlen))

        for metric in self._metrics:
            metric.compute_metrics(time_frame, metric_data)

        self._alert.refresh_availability_alerts(self._metrics[-1].website_availability)

    def perform_availability_check(self) -> None:
        try:
            response = requests.head(self.website_url, timeout=self.AVAILABILITY_TIMEOUT)
        except requests.exceptions.Timeout:
            self._data_store.append(MetricEntry(self.AVAILABILITY_TIMEOUT, requests.codes.timeout))
        except requests.exceptions.ConnectionError:
            self._data_store.append(MetricEntry(0.0, requests.codes.server_error))
        else:
            self._data_store.append(MetricEntry(response.elapsed.total_seconds(), response.status_code))

    def get_alerts(self) -> List[Tuple[str, AlertType]]:
        return self._alert.availability_alerts

    def get_stats_by_timeframe(self, time_frame: int) -> Iterator[float]:
        return chain.from_iterable([metric.to_list_by_timeframe(time_frame) for metric in self._metrics])

    @classmethod
    def get_metric_names(cls) -> Iterator[str]:
        return chain.from_iterable([metric.metric_names for metric in cls.METRICS])
