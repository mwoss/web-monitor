from abc import abstractmethod, ABCMeta
from collections import Counter
from dataclasses import dataclass
from typing import List

from monitor.constants import TIME_FRAMES, ALERT_TIME_FRAME


class MetricEntry:
    __slots__ = ('response_time', 'status_code_family')

    def __init__(self, response_time: float, status_code: int):
        self.response_time = response_time
        self.status_code_family = status_code - status_code % 100


@dataclass
class StatusStats:
    __slots__ = ('availability', 'http_success_count', 'http_client_error_count', 'http_server_error_count')

    availability: float
    http_success_count: int
    http_client_error_count: int
    http_server_error_count: int


@dataclass
class ResponseTimeStats:
    __slots__ = ('avg_response_time', 'max_response_time')

    avg_response_time: float
    max_response_time: float


class Metric(metaclass=ABCMeta):
    metric_names = []

    def __init__(self):
        self._stats = {tf: None for tf in TIME_FRAMES}

    @abstractmethod
    def compute_metrics(self, time_frame: int, metric_data: List[MetricEntry]) -> None:
        raise NotImplementedError("Metric must implement compute_metrics functionality")

    @abstractmethod
    def to_list_by_timeframe(self, time_frame: int) -> List[float]:
        raise NotImplementedError("Metric must implement to_list_by_timeframe functionality")


class ResponseTimeMetric(Metric):
    metric_names = ["AvgResponseTime[s]", "MaxResponseTime[s]"]

    def compute_metrics(self, time_frame: int, metric_data: List[MetricEntry]) -> None:
        responses = [entry.response_time for entry in metric_data]
        avg_time, max_time = round(sum(responses) / len(responses), 4), round(max(responses), 4)

        self._stats[time_frame] = ResponseTimeStats(avg_time, max_time)

    def to_list_by_timeframe(self, time_frame: int) -> List[float]:
        stats: ResponseTimeStats = self._stats[time_frame]
        return [
            stats.avg_response_time,
            stats.max_response_time
        ]


class HTTPStatusMetric(Metric):
    metric_names = ["Availability", "Status 2xx", "Status 4xx", "Status 5xx"]

    @property
    def website_availability(self):
        return self._stats[ALERT_TIME_FRAME].availability

    def compute_metrics(self, time_frame: int, metric_data: List[MetricEntry]) -> None:
        codes = [entry.status_code_family for entry in metric_data]
        code_counter = Counter(codes)
        availability = round(len(codes) / code_counter[200], 2) * 100

        self._stats[time_frame] = StatusStats(availability, code_counter[200], code_counter[400], code_counter[500])

    def to_list_by_timeframe(self, time_frame: int) -> List[float]:
        stats: StatusStats = self._stats[time_frame]
        return [
            stats.availability,
            stats.http_success_count,
            stats.http_client_error_count,
            stats.http_server_error_count
        ]
