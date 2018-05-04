from Lib import Util


def process_final(config, flight_info, first_line, last_line):
    first_record = Util.json_load(first_line)
    last_record = Util.json_load(last_line)
    flight_info["flight_time"] = {"first_time": first_record["data_time"], "last_time": last_record["data_time"]}
