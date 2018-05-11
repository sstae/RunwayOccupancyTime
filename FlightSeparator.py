import datetime
import glob
import os
import pprint
import re
import shutil
import time
import traceback

from Lib import Config
from Lib import Util


def read_last_line_for_each_flight(cat, runtime_flight_data_by_date_path, last_update_date):
    last_flight = []
    last_line = []
    path = runtime_flight_data_by_date_path + "\\" + str(last_update_date) + "\\" + cat
    list_file_in_last_update = os.listdir(path)
    for eachFlightInLastUpdate in list_file_in_last_update:
        file = open(path + "\\" + eachFlightInLastUpdate, 'r')
        last_line_of_file = file.readlines()[-1]
        last_flight.append(eachFlightInLastUpdate)
        # print(last_line_of_file)
        last_line.append(last_line_of_file)
    return dict(zip(last_flight, last_line))


def assign_filename(aircraft, filename, data_datetime_on_last_line):
    elements = filename.split('_')
    ac_id = elements[0]
    no = elements[1]
    if ac_id in aircraft:
        aircraft_record = aircraft[ac_id]
        if int(no) > aircraft_record['no']:
            aircraft_record['no'] = int(no)
            aircraft_record['last_date_time'] = data_datetime_on_last_line
    else:
        aircraft[ac_id] = {'no': int(no), 'last_date_time': data_datetime_on_last_line}


def initial_aircraft(config):
    aircraft = {}
    try:
        list_date_from_flight_data_by_date = os.listdir(config['runtime_flight_data_by_date'])
        print("list_date_from_flight_data_by_date:", list_date_from_flight_data_by_date)
        if list_date_from_flight_data_by_date:
            last_update_date = sorted(list_date_from_flight_data_by_date, reverse=True)[0]
            print("last_update_date:", last_update_date)
            date = datetime.datetime.strptime(str(last_update_date), '%Y%m%d')
            print("date:", date)
            last_line_dict = read_last_line_for_each_flight(config['cat'], config['runtime_flight_data_by_date'],
                                                            last_update_date)
            # print(last_line_dict)
            for filename in last_line_dict:
                line = last_line_dict[filename]
                data = Util.json_load(line)
                data_time = data['data_time']
                assign_filename(aircraft, filename, data_time)
        else:
            print("No Old Data")
    except Exception as error:
        print(traceback.format_exc())
        print("Cannot load old data " + repr(error))
    return aircraft


def extract_data(aircraft, date_of_flight, line, separated_flight_time_gap):
    elements = line.split('|')
    if (elements[1] == 'CAT20') and (elements[2] == '1.1'):
        return Util.extract_cat20_v1_1(aircraft, date_of_flight, line, separated_flight_time_gap)
    else:
        raise ValueError('Cat not support')


def process_line(config, aircraft, lines_seen, line, date_of_flight):
    raw_data = line.split('|', 1)[1]  # cut line to rawdata by ignore the first column.
    data = {}
    if raw_data not in lines_seen:  # do only not duplicated lines.
        lines_seen.append(raw_data)
        # print("processLine:" + line)
        if raw_data.startswith(config['cat']):
            try:
                data = extract_data(aircraft, date_of_flight, line, int(config['separated_flight_time_gap']))
            except Exception as error:
                print(traceback.format_exc())
                print('process_line ' + line + '\nCaught this error: ' + repr(error))
    return data


def after_process(config, data):
    date = str(data["assign_date"].strftime("%Y%m%d"))
    output_path = config["runtime_flight_data_by_date"] + "\\" + date + "\\" + config['cat']
    Util.append_filename(output_path, data['filename'], Util.json_dump(data))


def process_file(config, aircraft, filename):
    lines_seen = Util.CircularBuffer(size=int(config['lines_seen_size']))
    print("process_file: " + filename)
    # ? need to be change according to config['input_filename_pattern']
    temp = re.findall(r'data[\s.]csv[\s.](\d{8})(\d{2})', filename)
    date_from_filename = temp[0][0]
    hour = temp[0][1]
    date_of_flight = datetime.datetime.strptime(date_from_filename, "%Y%m%d")
    buffer_size = 2 ** 16
    with open(filename) as f:
        while True:
            lines_buffer = f.readlines(buffer_size)
            if not lines_buffer:
                break
            for line in lines_buffer:
                data = process_line(config, aircraft, lines_seen, line, date_of_flight)
                if data != {}:
                    after_process(config, data)
    shutil.move(filename, config['runtime_archived_raw_data'])
    if hour == config['time_to_make_unchanged_folder']:
        target_date_of_flight = date_of_flight - datetime.timedelta(days=1)
        path = config["runtime_flight_data_by_date"] + "\\" + target_date_of_flight.strftime("%Y%m%d")
        output_path = config["output_flight_data_by_date"] + "\\" + target_date_of_flight.strftime("%Y%m%d")
        if os.path.exists(path):
            shutil.copytree(path, output_path, symlinks=False, ignore=None)
            os.renames(path, path + "_")


def main_process(config, aircraft):
    print("Start main process\n")
    os.chdir(config['input_raw_data'])
    running_process = True
    while running_process:
        try:
            file_list = glob.glob(config['input_filename_pattern'])
            if file_list:
                for fileName in sorted(file_list):
                    input_file = os.path.join(config['input_raw_data'], fileName)
                    process_file(config, aircraft, input_file)
                    print('finished: ' + input_file)
            time.sleep(2)
        except Exception as error:
            print(traceback.format_exc())
            print('main_process Caught this error: ' + repr(error))
            break


current_path = os.path.dirname(os.path.abspath(__file__))
pp = pprint.PrettyPrinter(indent=4)

# initial config
all_config = Config.initial_config(current_path, 'config.txt')
print("config:")
pp.pprint(all_config)

# initial aircraft
aircraft_dict = initial_aircraft(all_config)
print("aircraft:")
pp.pprint(aircraft_dict)

# Loop Process
main_process(all_config, aircraft_dict)
