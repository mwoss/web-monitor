from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


class AlertType(Enum):
    DOWN = 0
    RECOVER = 1


@dataclass
class AlertMessage:
    alert_message: str
    alert_type: AlertType


class Alert:
    """
    Alerting object responsible for storing all website notifications
    """
    AVAILABILITY_THRESHOLD = 80
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, website_url: str):
        self.website_url = website_url
        self.availability_alerts: List[AlertMessage] = []
        self._alert_state = AlertType.RECOVER

    def refresh_availability_alerts(self, availability: float) -> None:
        """
        Refresh alerts using corresponding AVAILABILITY_THRESHOLD and previous alert message.
        Messages of the same type cannot be overwritten, only the oldest one is saved for historical reason.
        :param availability: website availability parameter
        """
        if availability < self.AVAILABILITY_THRESHOLD and self._alert_state == AlertType.RECOVER:
            self._alert_state = AlertType.DOWN
            self.availability_alerts.append(AlertMessage(self._get_down_message(availability), AlertType.DOWN))
        elif availability >= self.AVAILABILITY_THRESHOLD and self._alert_state == AlertType.DOWN:
            self._alert_state = AlertType.RECOVER
            self.availability_alerts.append(AlertMessage(self._get_recover_message(availability), AlertType.RECOVER))

    def _get_recover_message(self, availability: float) -> str:
        return f"Alert recovered. Website {self.website_url} is up. " \
               f"availability={availability}, time={datetime.now().strftime(self.TIME_FORMAT)}"

    def _get_down_message(self, availability: float) -> str:
        return f"Website {self.website_url} is down. " \
               f"availability={availability}, time={datetime.now().strftime(self.TIME_FORMAT)}"
