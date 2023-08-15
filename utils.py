import os
from settings import *
from datetime import datetime
from time import sleep
from gpiozero import AngularServo


def db_write(feeding_type, ip_address):
    db_reduce_rows()
    now = f"{datetime.now().replace(microsecond=0):{DATETIME_FORMAT}}"
    with open(FEED_TIMELINE_FILE_PATH, 'a+') as f:
        f.write(f'{now}, {feeding_type}, {ip_address}\n')


def db_read():
    result = []
    if not os.path.exists(FEED_TIMELINE_FILE_PATH):
        return result
    
    with open(FEED_TIMELINE_FILE_PATH, 'r') as f:
        for feeding in f.readlines():
            feeding_time, feeding_type, feeder_ip = feeding.split(',')
            result.append({'time': feeding_time.strip(), 'type': feeding_type.strip(), 'feeder': feeder_ip.strip()})

    result.reverse()
    return result


def db_reduce_rows():
    if os.path.exists(FEED_TIMELINE_FILE_PATH):
        with open(FEED_TIMELINE_FILE_PATH, 'r') as read_f:
            lines = read_f.readlines()
            if len(lines) >= MAX_DB_ROWS:
                with open(FEED_TIMELINE_FILE_PATH, 'w') as write_f:
                    write_f.writelines(lines[len(lines) - MIN_DB_ROWS + 1:])


def hours_since_last_feeding(last_feeding_string):
    if last_feeding_string == INITIAL_LAST_FEEDING_STRING:
        hours_since = FEEDING_INTERVAL_IN_HOURS + 1
    else:
        last_feeding = datetime.strptime(last_feeding_string, DATETIME_FORMAT)
        now = datetime.now().replace(microsecond=0)
        hours_since = (now - last_feeding).seconds / 3600

    return hours_since


def move_servo(sleep_time):
    s = AngularServo(21, min_angle=-1.0, max_angle=1.0)
    s.max()
    sleep(sleep_time)
    s.min()
    sleep(0.1)


def open_feeding_lid(feeding_type):
    # TODO: actual motor movement code
    lid_open_time = FEEDING_MAP[feeding_type]
    move_servo(lid_open_time)
