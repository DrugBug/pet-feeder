MAX_DB_ROWS = 28
MIN_DB_ROWS = 14
FEEDING_INTERVAL_IN_HOURS = 8
INITIAL_LAST_FEEDING_STRING = 'Never'
DATETIME_FORMAT = "%d-%m-%Y %H:%M"
FEED_TIMELINE_FILE_PATH = 'feeding_timeline.txt'
FEEDING_OPTIONS = [
    {'en': '45g', 'he': 'מנה רגילה (45 גרם)', 'default': True},
    {'en': '55g', 'he': 'מנה מוגברת (55 גרם)', 'default': False}
]
FEEDING_MAP = {
    '45g': 1,
    '55g': 4
}
WEBSERVER_PORT = 8012
