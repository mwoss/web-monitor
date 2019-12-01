from datetime import datetime
from enum import Enum
from typing import List, Tuple


class AlertType(Enum):
    DOWN = 0
    RECOVER = 1


class Alert:
    AVAILABILITY_THRESHOLD = 80
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, website_url: str):
        self.website_url = website_url
        self.availability_alerts: List[Tuple[str, AlertType]] = []
        self._alert_state = AlertType.RECOVER

    def refresh_availability_alerts(self, availability: float) -> None:
        if availability < self.AVAILABILITY_THRESHOLD and self._alert_state == AlertType.RECOVER:
            self._alert_state = AlertType.DOWN
            self.availability_alerts.append((self._down_message(availability), AlertType.DOWN))
        elif availability >= self.AVAILABILITY_THRESHOLD and self._alert_state == AlertType.DOWN:
            self._alert_state = AlertType.RECOVER
            self.availability_alerts.append((self._recover_message(availability), AlertType.RECOVER))

    def _recover_message(self, availability: float) -> str:
        return f"Alert recovered. Website{self.website_url} is up. " \
               f"availability={availability}, time={datetime.now().strftime(self.TIME_FORMAT)}"

    def _down_message(self, availability: float) -> str:
        return f"Website {self.website_url} is down. " \
               f"availability={availability}, time={datetime.now().strftime(self.TIME_FORMAT)}"
