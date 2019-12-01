from collections import deque, Counter, defaultdict
from dataclasses import dataclass
from itertools import islice

import requests
from requests.exceptions import RequestException

from monitor.constants import SUPPORTED_TIMEFRAMES

HOURS_TO_SECOND = 3600


class MonitoredWebsite:
    AVAILABILITY_TIMEOUT = 5
    METRICS = []

    def __init__(self, website: str, interval: int):
        self.website = website
        self.interval = interval
        self.stats = {time_frame: None for time_frame in SUPPORTED_TIMEFRAMES}
        self._data_store = deque(maxlen=HOURS_TO_SECOND // interval)

    def refresh_stats(self, time_frame: int) -> None:
        window_len = max(time_frame // self.interval - self._data_store.maxlen, 0)
        t_data = list(islice(self._data_store, window_len, self._data_store.maxlen))
        codes = [e.status_code_family for e in t_data]
        c = Counter(codes)

        responses = [e.response_time for e in t_data]
        avg, max_r = round(sum(responses) / (self._data_store.maxlen - window_len), 4), round(max(responses), 4)
        availability = round(len(codes) / c[200], 2)

        self.stats[time_frame] = WebsiteStats(availability, avg, max_r, c[200], c[400], c[500])

    def perform_availability_check(self) -> None:
        try:
            response = requests.head(self.website, timeout=self.AVAILABILITY_TIMEOUT)
        except requests.exceptions.Timeout:
            self._data_store.append(MetricEntry(self.AVAILABILITY_TIMEOUT, requests.codes.timeout))
        except requests.exceptions.ConnectionError:
            self._data_store.append(MetricEntry(0.0, requests.codes.server_error))
        else:
            self._data_store.append(MetricEntry(response.elapsed.total_seconds(), response.status_code))

    # def _compute_availability(self):


@dataclass
class WebsiteStats:
    availability: float
    avg_response_time: float
    max_response_time: float
    http_success_count: int
    http_client_error_count: int
    http_server_error_count: int


class MetricEntry:
    __slots__ = ('response_time', 'status_code_family')

    def __init__(self, response_time: float, status_code: int):
        self.response_time = response_time
        self.status_code_family = status_code - status_code % 100
