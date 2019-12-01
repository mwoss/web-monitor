from os import name, system
from typing import Dict, List

from monitor.constants import TIME_FRAMES
from monitor.metrics import MonitoredWebsite

COLUMNS = [
    'TimeFrame', "UpdateRate", "Availability", "AvgResponseTime",
    "MaxResponseTime", "Status 2xx", "Status 4xx", "Status 5xx"
]


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BWHITE = "\033[97m"
    END = "\033[0m"
    BOLD = "\033[1m"


def clear_console():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def row_format(row_size: int) -> str:
    return "{:<20}" * row_size


def render_metrics(monitored_websited: List[MonitoredWebsite]):
    clear_console()  # its not working in intelij terminal, note this

    for website in monitored_websited:
        print(row_format(len(COLUMNS)).format(*COLUMNS))

        for time_frame, meta in TIME_FRAMES.items():
            stats = website.stats[meta['window']]
            print(row_format(len(COLUMNS)).format(
                time_frame, meta['rate'], stats.availability, stats.avg_response_time, stats.max_response_time,
                stats.http_success_count, stats.http_client_error_count, stats.http_server_error_count, 'ok')
            )