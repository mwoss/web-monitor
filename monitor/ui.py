from os import name, system
from typing import List, Iterator

from monitor.alert import AlertType
from monitor.constants import TIME_FRAMES
from monitor.website import MonitoredWebsite


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    END = "\033[0m"
    BOLD = "\033[1m"


class ConsoleInterface:
    COMMON_COLUMNS = ['TimeFrame', "UpdateRate[s]"]

    def __init__(self, metric_names: Iterator[str]):
        self.metric_names = [*self.COMMON_COLUMNS, *metric_names]

    def render_metrics(self, monitored_website: List[MonitoredWebsite]) -> None:
        self._clear_console()

        for website in monitored_website:
            print("-" * 100)

            print(f"Website: {Color.YELLOW}{website.website_url}{Color.END} | "
                  f"CheckInterval: {Color.CYAN}{website.interval} seconds{Color.END}")
            print(f"{Color.BOLD}{self._row_format().format(*self.metric_names)}{Color.END}")

            for timeframe, meta in TIME_FRAMES.items():
                stats = website.get_stats_by_timeframe(timeframe)
                print(self._row_format().format(*meta.values(), *stats))

            print(f"{Color.BOLD}Notifications:{Color.END}")
            for alert in website.get_alerts():
                self._print_alert(alert.alert_message, alert.alert_type)

            print("-" * 100)

    def _row_format(self) -> str:
        return "{:<20}" * len(self.metric_names)

    @staticmethod
    def _print_alert(message: str, alert_type: AlertType):
        if alert_type == AlertType.DOWN:
            print(f"{Color.RED}{message}{Color.END}")
        else:
            print(f"{Color.GREEN}{message}{Color.END}")

    @staticmethod
    def _clear_console() -> None:
        if name == 'nt':
            system('cls')
        else:
            system('clear')
