import json
from argparse import ArgumentParser, RawTextHelpFormatter

from monitor.constants import CONFIG_FILE
from monitor.task import HTTPMonitor

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Web-monitor is a console application for website availability & performance monitoring. \n"
                    "Web-monitor provides few metrics: availability, max/avg response time and status code count \n"
                    "Application can be configured via config.json file",
        formatter_class=RawTextHelpFormatter
    )
    args = parser.parse_args()

    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)

    parsed_config = {website_config["website"]: website_config["interval"] for website_config in config["monitor"]}

    monitor = HTTPMonitor(parsed_config)
    monitor.start()
