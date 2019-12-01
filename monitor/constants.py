CONFIG_FILE = "config.json"
SECONDS_IN_HOUR = 3600
ALERT_TIME_FRAME = 120
TIME_FRAMES = {
    120: {
        "ui_format": "2min",
        "refresh_rate": 1,
    },
    600: {
        "ui_format": "10min",
        "refresh_rate": 10,
    },
    3600: {
        "ui_format": "1h",
        "refresh_rate": 600,
    }
}
