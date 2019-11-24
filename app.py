import argparse
import urllib.parse
import urllib.request

from monitor.task import PerformanceMonitor


def url_check(value: str):
    parsed = urllib.parse.urlparse(value)
    if not all([parsed.scheme, parsed.netloc, parsed.path]):
        raise argparse.ArgumentTypeError("Incorrect URL address. The URL parameter is probably missing a protocol part")
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="by default ")
    parser.add_argument('-w', '--websites', type=url_check, nargs='+', help="")
    parser.add_argument('-i', '--intervals', type=int, nargs='+', help="in sec")
    parser.add_argument('-sl', '--save-log', action='store_true', help="")

    args = parser.parse_args()

    test_config = {
        # "https://www.datadoghq.com": 5,
        "https://www.wykop.pl": 5
    }

    monitor = PerformanceMonitor(test_config)
    monitor.start()
