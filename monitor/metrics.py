from abc import abstractmethod, ABCMeta
from collections import Counter
from dataclasses import dataclass
from typing import List

from monitor.constants import TIME_FRAMES, ALERT_TIME_FRAME


class MetricEntry:
    __slots__ = ("response_time", "status_code_family")

    def __init__(self, response_time: float, status_code: int):
        self.response_time = response_time
        self.status_code_family = status_code - status_code % 100


@dataclass
class StatusStats:
    __slots__ = ("availability", "http_success_count", "http_client_error_count", "http_server_error_count")

    availability: float
    http_success_count: int
    http_client_error_count: int
    http_server_error_count: int


@dataclass
class ResponseTimeStats:
    __slots__ = ("avg_response_time", "max_response_time")

    avg_response_time: float
    max_response_time: float


class Metric(metaclass=ABCMeta):
    """
    Abstract class existing as an interface for new Metrics.
    """
    metric_names = []

    def __init__(self):
        self._stats = {tf: None for tf in TIME_FRAMES}

    @abstractmethod
    def compute_metrics(self, timeframe: int, metric_data: List[MetricEntry]) -> None:
        """
        Compute metrics for given timeframe and store it inside metric instance
        :param timeframe: timeframe for which the metric should be calculated
        :param metric_data: list of MetricEntry used for computing metric stats
        """
        raise NotImplementedError("Metric must implement compute_metrics functionality")

    @abstractmethod
    def to_list_by_timeframe(self, timeframe: int, display_format: bool = False) -> List[float]:
        """
        Return all metric data in form of a list
        :param timeframe: timeframe from which data is obtained
        :param display_format: flag, if set statistics are formatted for displaying in console
        :return: all metrics as a list in exact same order as metric_names
        """
        raise NotImplementedError("Metric must implement to_list_by_timeframe functionality")


class ResponseTimeMetric(Metric):
    metric_names = ["AvgResponseTime[s]", "MaxResponseTime[s]"]

    def compute_metrics(self, timeframe: int, metric_data: List[MetricEntry]) -> None:
        responses = [entry.response_time for entry in metric_data]
        avg_time, max_time = sum(responses) / len(responses), max(responses)

        self._stats[timeframe] = ResponseTimeStats(avg_time, max_time)

    def to_list_by_timeframe(self, timeframe: int, display_format: bool = False) -> List[float]:
        stats: ResponseTimeStats = self._stats[timeframe]
        return [
            f"{stats.avg_response_time:.4f}" if display_format else stats.avg_response_time,
            f"{stats.max_response_time:.4f}" if display_format else stats.max_response_time
        ]


class HTTPStatusMetric(Metric):
    metric_names = ["Availability", "Status 2xx", "Status 4xx", "Status 5xx"]

    @property
    def website_availability(self):
        return self._stats[ALERT_TIME_FRAME].availability

    def compute_metrics(self, timeframe: int, metric_data: List[MetricEntry]) -> None:
        codes = [entry.status_code_family for entry in metric_data]
        code_counter = Counter(codes)
        availability = code_counter[200] / len(codes) * 100

        self._stats[timeframe] = StatusStats(availability, code_counter[200], code_counter[400], code_counter[500])

    def to_list_by_timeframe(self, timeframe: int, display_format: bool = False) -> List[float]:
        stats: StatusStats = self._stats[timeframe]
        return [
            f"{stats.availability:.2f}" if display_format else stats.availability,
            stats.http_success_count,
            stats.http_client_error_count,
            stats.http_server_error_count
        ]
