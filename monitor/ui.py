from os import name, system
from typing import Dict

from monitor.metrics import WebsiteMetric


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


def render_metrics(metrics_info: Dict[str, WebsiteMetric]):
    clear_console() # its not working in intelij terminal, note this
    for website, metric_data in metrics_info.items():
        print("#" * 80)
        print(f"Metrics for website: {Color.BLUE}{website}{Color.BWHITE} with interval: {Color.MAGENTA}{metric_data.interval}{Color.END} ")
        print("-" * 80)
        print("Time frame: 1 minute")
        print(f"Availability:{Color.GREEN}{metric_data.compute_availability(60)}{Color.END}") # in seconds
        avg_resp, max_resp = metric_data.compute_response_time(360)
        print(f"Average response time: {Color.GREEN}{avg_resp}{Color.END}")
        print(f"Max response time: {Color.GREEN}{max_resp}{Color.END}")
