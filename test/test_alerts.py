import unittest

from monitor.alert import Alert, AlertType


class TestAlert(unittest.TestCase):
    def setUp(self) -> None:
        self.website_alert = Alert('example.com')

    def test_threshold_crosses_should_produce_proper_availability_alerts(self):
        availabilities = [84, 79, 75, 81, 77, 82]

        for availability in availabilities:
            self.website_alert.refresh_availability_alerts(availability)

        expected_result = [AlertType.DOWN, AlertType.RECOVER, AlertType.DOWN, AlertType.RECOVER]
        result = [entry.alert_type for entry in self.website_alert.availability_alerts]
        self.assertListEqual(expected_result, result)

    def test_continuous_high_availability_should_not_produce_any_message(self):
        availabilities = [80, 85, 90, 95, 100, 100]

        for availability in availabilities:
            self.website_alert.refresh_availability_alerts(availability)

        self.assertListEqual([], self.website_alert.availability_alerts)

    def test_continuous_low_availability_should_produce_single_message(self):
        availabilities = [80, 70, 60, 50, 40, 30]

        for availability in availabilities:
            self.website_alert.refresh_availability_alerts(availability)

        self.assertEqual(AlertType.DOWN, self.website_alert.availability_alerts[0].alert_type)
        self.assertEqual(1, len(self.website_alert.availability_alerts))

    def test_website_should_recover_after_threshold_cross(self):
        availabilities = [100, 60, 80, 90]

        for availability in availabilities:
            self.website_alert.refresh_availability_alerts(availability)

        expected_result = [AlertType.DOWN, AlertType.RECOVER]
        result = [entry.alert_type for entry in self.website_alert.availability_alerts]
        self.assertListEqual(expected_result, result)

    def test_high_availability_should_not_change_alert_state(self):
        availabilities = [100, 97, 98, 100]

        for availability in availabilities:
            self.website_alert.refresh_availability_alerts(availability)

        self.assertListEqual([], self.website_alert.availability_alerts)
