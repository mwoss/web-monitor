from collections import deque
from itertools import islice

import requests
from requests.exceptions import RequestException

HOURS_TO_SECOND = 3600


class WebsiteMetric:
    def __init__(self, website: str, interval: int):
        self.website = website
        self.interval = interval
        self.data_store = deque(maxlen=HOURS_TO_SECOND // interval)

    # TODO: create slicable deque
    def compute_availability(self, time_frame: int):
        # time_frame in sec
        window_len = time_frame // self.interval
        t_data = list(islice(self.data_store, s_window, self.data_store.maxlen))
        codes = [e.status_code for e in t_data]
        try:
            return round(s_window / codes.count(200), 2)
        except ZeroDivisionError:
            return 0.0

    def compute_response_time(self, time_frame: int):
        # return avg and max
        s_window = time_frame // self.interval
        t_data = list(islice(self.data_store, s_window, self.data_store.maxlen))
        responses = [e.response_time for e in t_data]

        return sum(responses) / s_window, max(responses)


class MetricEntry:
    __slots__ = ('response_time', 'status_code')

    def __init__(self, response_time, status_code):
        self.response_time = response_time
        self.status_code = status_code


def store_metrics(website: str, website_feed):
    try:
        # TODO: timeout after interval
        response = requests.get(website)
        print("status code", website_feed.data_store)
        website_feed.data_store.append(MetricEntry(response.elapsed.total_seconds(), response.status_code))
    except RequestException:
        pass
