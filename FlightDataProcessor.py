import datetime
import glob
import os
import pprint
import shutil
import time
import traceback

from Lib import Config
from Lib import ProcessBay
from Lib import ProcessCallsign
from Lib import ProcessDirection
from Lib import ProcessFlightMap
from Lib import ProcessFlightTime
from Lib import ProcessRunway
from Lib import Util


def initial_flight(config):
    flight = {}
    try:
        # TODO Use file pattern to filter only active files(having _ file) by joe
        list_date_from_flight_info = os.listdir(config['runtime_flight_info'])
        print("list_date_from_flight_info:", list_date_from_flight_info)
        if list_date_from_flight_info:
            last_update_date = sorted(list_date_from_flight_info, reverse=True)[0]
            if not last_update_date.endswith('_'):
                print("last_update_date:", last_update_date)
                date = datetime.datetime.strptime(str(last_update_date), '%Y%m%d')
                print("date:", date)
                filename = config['runtime_flight_info'] + "\\" + last_update_date
                buffer_size = 2 ** 16
                with open(filename) as f:
                    flight_info_by_date = {'date': last_update_date, 'flight_info': {}}
                    while True:
                        lines_buffer = f.readlines(buffer_size)
                        if not lines_buffer:
                            break
                        for line in lines_buffer:
                            data = Util.json_load(line)
                            flight_info_by_date['flight_info']['ac_id'] = data
                    flight = flight_info_by_date
        else:
            print("No Old Data")
    except Exception as error:
        print("Cannot load old data " + repr(error))
    return flight


def check_flight(flight, date):
    if flight == {} or flight['date'] != date:
        flight['date'] = date
        flight['flight_info'] = {}


def process_by_line(config, flight_info, content):
    ProcessCallsign.process_by_line(config, flight_info, content)
    ProcessDirection.process_by_line(config, flight_info, content)
    ProcessBay.process_by_line(config, flight_info, content)
    ProcessRunway.process_by_line(config, flight_info, content)


def get_flight_movement(flight_movement_at_date, flight_info):
    if 'callsign' in flight_info:
        if 'callsign' in flight_info['callsign']:
            if flight_info['callsign']['callsign'] in flight_movement_at_date:
                temp = flight_movement_at_date[flight_info['callsign']['callsign']]
                if len(temp) == 1:
                    return temp[0]
                # TODO Use direction by project
                # if flight_info["direction"]["direction"] == "arrival":
                # if arrival use end time compare to ATA/ETA.
                # if flight_info["direction"]["direction"] == "departure":
                # if departure use start time compare to ATD/ETD.
                else:
                    return temp[0]
    return None


def summary(config, flight_info):
    if "flight_movement" in flight_info:
        print("flight_movement", flight_info["flight_movement"])
    if "direction" in flight_info:
        print("direction", flight_info["direction"]["direction"])
    if "bay" in flight_info:
        print("bay_zone", flight_info["bay"]["bay"])
        flight_info["bay"].pop("bay_layout")
    if "runway" in flight_info:
        print("runway", flight_info["runway"]["runway"])
        flight_info["runway"].pop("runway_layout")
        if flight_info["runway"]["runway"] != "unknown":
            print("runway_time", flight_info["runway"]["runway_time"])
    if "callsign" in flight_info:
        print("callsign", flight_info["callsign"]["callsign"])


def process_final(config, flight_info, flight_movement_at_date):
    ProcessCallsign.process_final(config, flight_info)
    ProcessBay.process_final(config, flight_info)
    ProcessRunway.process_final(config, flight_info)
    flight_movement = get_flight_movement(flight_movement_at_date, flight_info)
    if flight_movement:
        flight_info['flight_movement'] = flight_movement
    summary(config, flight_info)


def process_flight(config, input_file, flight_movement_at_date):
    flight_info = {}
    a = open(input_file, 'r')
    first_line = a.readline()
    for line in a:
        last_line = line
    with open(input_file, "r") as f:
        for line in f:
            data = Util.json_load(line)
            process_by_line(config, flight_info, data)
        ProcessFlightTime.process_final(config, flight_info, first_line, last_line)
        process_final(config, flight_info, flight_movement_at_date)
    return flight_info


def archive_flight_data(config, runtime_file, date):
    archive_path = config['runtime_archived_flight_data'] + "\\" + date + "\\" + config['cat']
    try:
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        shutil.move(runtime_file, archive_path)
    except Exception as error:
        print(traceback.format_exc())
        print('archive_flight_data Caught this error: ' + repr(error))


def process_file(config, flight_at_date, flight_movement_at_date, filename):
    date = flight_at_date['date']
    runtime_input_file = config['runtime_flight_data_by_date'] + "\\" + date + "_\\" + config['cat'] + "\\" + filename
    flight_info = process_flight(config, runtime_input_file, flight_movement_at_date)
    ProcessFlightMap.process_plot(config, runtime_input_file, filename, date, flight_info)
    if flight_info:
        if filename in flight_at_date['flight_info']:
            if config['replace'] == 'true':
                flight_at_date['flight_info'][filename] = flight_info
                Util.dump_flight_info(config['runtime_flight_info'], date, flight_at_date['flight_info'])
            else:
                print('duplicate data ' + filename + ":\n" + Util.json_dump(flight_info))
        else:
            flight_at_date['flight_info'][filename] = flight_info
            Util.append_filename(config['runtime_flight_info'], date, Util.json_dump(flight_info))
    else:
        print('no summary for ' + filename)
    archive_flight_data(config, runtime_input_file, date)


def add_flight_movement(flight_movement_at_date, data):
    callsign = data['CS']  #fixed
    if callsign in flight_movement_at_date:
        flight_movement_at_date[callsign].append(data)
    else:
        flight_movement_at_date[callsign] = [data]


def load_flight_movement(config, date):
    # ? should use pattern to get file
    f_input_file = config['input_flight_movement_by_date'] + "\\FLIGHT_" + date + ".txt"
    flight_movement_at_date = {}
    with open(f_input_file, "r") as f:
        first_line = f.readline()
        for line in f:
            data = Util.extract_flight_movement(line)
            add_flight_movement(flight_movement_at_date, data)
    return flight_movement_at_date


def process_folder(config, flight, date):
    path = config['runtime_flight_data_by_date'] + "\\" + date + "_"
    input_folder = path + "\\" + config['cat']
    list_flight_data_by_date = os.listdir(input_folder)
    if list_flight_data_by_date:
        check_flight(flight, date)
        flight_movement_at_date = load_flight_movement(config, date)
        for filename in list_flight_data_by_date:
            process_file(config, flight, flight_movement_at_date, filename)
            print(filename + 'is finished')
    # after work
    list_flight_data_by_date = os.listdir(input_folder)
    # delete folder
    if list_flight_data_by_date == "":
        os.removedirs(input_folder)
        os.removedirs(path)
    # copy runtime to output and make unchange
    runtime_file = config['runtime_flight_info'] + "\\" + date
    output_path = config["output_flight_info"]
    if os.path.exists(path):
        shutil.copy(runtime_file, output_path)
        os.rename(runtime_file, runtime_file + "_")


def main_process(config, flight):
    print("Start main process\n")
    os.chdir(config['runtime_flight_data_by_date'])
    running_process = True
    while running_process:
        try:
            folder_list = glob.glob(config['input_folder_pattern'])
            if folder_list:
                for folder_name in sorted(folder_list):
                    process_folder(config, flight, folder_name[0: 8])
                    print(folder_name + 'is finished')
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

# initial flight
flight_dict = initial_flight(all_config)
print("flight:")
pp.pprint(flight_dict)

# Loop Process
main_process(all_config, flight_dict)
