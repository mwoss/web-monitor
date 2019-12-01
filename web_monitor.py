import argparse
import json
import urllib.parse
import urllib.request

from monitor.constants import CONFIG_FILE
from monitor.task import HTTPMonitor


def url_check(value: str):
    parsed = urllib.parse.urlparse(value)
    if not all([parsed.scheme, parsed.netloc, parsed.path]):
        raise ValueError("Incorrect URL address. The URL parameter is probably missing a protocol part")
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Web-monitor is a console application for website availability & performance monitoring. \n"
                    "Web-monitor provides few metrics: availability, max/avg response time and status code count \n"
                    "Application can be configured via config.json file",
        formatter_class=argparse.RawTextHelpFormatter
    )
    args = parser.parse_args()

    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)

    parsed_config = {website_config['website']: website_config['interval'] for website_config in config['monitor']}

    monitor = HTTPMonitor(parsed_config)
    monitor.start()
