import datetime
from decimal import Decimal
import json
import os
import re
import traceback

from collections import deque


class CircularBuffer(deque):
    def __init__(self, size=0):
        super(CircularBuffer, self).__init__(maxlen=size)

    @property
    def average(self): 
        return sum(self)/len(self)


def test(x):
    print(x)


# util for json to serialize datetime
class DatetimeDecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


def datetime_decimal_decoder(json_dict):
    for (key, value) in json_dict.items():
        if type(value) is str and re.match('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d*$', value):
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        elif type(value) is str and re.match('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$', value):
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        elif type(value) is str and re.match('^[+-]?\d+[\s.][+-]?\d+$', value):
            json_dict[key] = Decimal(value)
        else:
            pass
    return json_dict


def get_date(date, time, data_time, time_type):
    times = time.split(":")
    hour = int(times[0]) * 3600
    minute = int(times[1]) *60
    second = float(times[2])
    total = second + minute + hour
    if time_type == 'bkk':
        if total < 25200:  # system time less than 07:00 bkk time
            if float(data_time) > 3600:  # data_time more than 01:00 utc
                return date - datetime.timedelta(days=1)
            else: # data_time less than or equal 01:00 utc
                return date
        elif (total >= 25200) and (total <= 28800): # system time from 07:00 - 08:00 bkk time
            if float(data_time) > 3600 : # data_time more than 01:00 utc
                return date - datetime.timedelta(days=1)
            else:
                return date
        else:
            return date
    else:
        raise ValueError('time type not support')


def create_path_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def check_current_path(path, current_path):
    # check path is start with current path ?
    # create if not exist
    if path.startswith('.\\'):
        output_path = current_path + "\\"+ path
    else:
        output_path = path
    create_path_directory(output_path)
    return output_path


def json_dump(data):
    return json.dumps(data, cls=DatetimeDecimalEncoder)


def json_load(data):
    return json.loads(data, object_hook=datetime_decimal_decoder)


def get_position(data):
    elements = data.split(",")
    position = {'lat': Decimal(elements[0]), 'lon': Decimal(elements[1])}
    return position


def get_filename(aircraft, ac_id, data_datetime, separated_flight_time_gap):
    if ac_id in aircraft:
        aircraft_record = aircraft[ac_id]
        if ac_id != "unknown" and (data_datetime - aircraft_record['last_date_time']).seconds >= separated_flight_time_gap:
            if data_datetime.date() != aircraft_record['last_date_time'].date():
                aircraft_record['no'] = 0
            else:
                aircraft_record['no'] = aircraft_record['no'] + 1
        aircraft_record['last_date_time'] = data_datetime
    else:
        aircraft[ac_id] = {'no': 0, 'last_date_time': data_datetime}
    return ac_id + '_' + str(aircraft[ac_id]['no']).zfill(2)


def get_output_file(aircraft, ac_id, assign_date, data_time, separated_flight_time_gap):
    data_datetime = assign_date + datetime.timedelta(seconds=data_time)
    output_filename = get_filename(aircraft, ac_id, data_datetime, separated_flight_time_gap)
    return output_filename


def extract_cat20_v1_1(aircraft, date_of_flight, line, separated_flight_time_gap):
    elements = line.split('|')
    fields = {}
    time = elements[0]
    for i in range(3, len(elements) - 1):
        items = elements[i].split(':')
        fields[str(items[0])] = items[1]
    data_time = fields['3']
    if '12' in fields:
        ac_id = fields['12']
    else:
        ac_id = "unknown"
    date_type = 'bkk'
    assign_date = get_date(date_of_flight, time, float(data_time), date_type)
    output_filename = get_output_file(aircraft, ac_id, assign_date, float(data_time), separated_flight_time_gap)
    data_datetime = assign_date + datetime.timedelta(seconds=float(data_time))
    if '4' in fields:
        position = get_position(fields['4'])
    else:
        position = None
    if '14' in fields:
        flight_level = Decimal(fields['14'])
    else:
        flight_level = None
    if '10' in fields:
        height = Decimal(fields['10'])
    elif flight_level:
        height = flight_level * 100
    else:
        height = None
    if '13' in fields:
        callsign = fields['13'].split(',')[2]
    else:
        callsign = ""
    content = {
        "data_time": data_datetime,
        "id": ac_id,
        "position": position,
        "height": {"flight_level": flight_level, "height": height},
        "callsign": callsign,
        "filename": output_filename,
        "assign_date": assign_date}
    return content


def extract_flight_movement(data):
    flight_movement = {}
    elements = data.split(',')
    # ? under construction
    flight_movement['status'] = elements[0]
    return flight_movement


def dump_flight_info(path, filename, data):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        output_filename = path + "\\" + filename
        a = open(output_filename, "w")
        for element in data:
            a.write(json_dump(element) + '\n')
        a.close()
    except Exception as error:
        print(traceback.format_exc())
        print('dump_flight_info Caught this error: ' + repr(error))


def append_filename(path, filename, data):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        output_filename = path + "\\" + filename
        a = open(output_filename, "a")
        a.write(data + '\n')
        a.close()
    except Exception as error:
        print(traceback.format_exc())
        print('append_filename Caught this error: ' + repr(error))
