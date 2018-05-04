import configparser

from Lib import Util


def initial_config(current_path, filename):
    config_data = configparser.ConfigParser()
    config_data.read_file(open(filename, 'r'))
    config = {}
    config['input_raw_data'] = Util.check_current_path(config_data.get('Path', 'input_raw_data'), current_path)
    config['input_flight_movement_by_date'] = Util.check_current_path(
        config_data.get('Path', 'input_flight_movement_by_date'), current_path)
    config['runtime_archived_raw_data'] = Util.check_current_path(config_data.get('Path', 'runtime_archived_raw_data'),
                                                                  current_path)
    config['runtime_archived_flight_data'] = Util.check_current_path(
        config_data.get('Path', 'runtime_archived_flight_data'), current_path)
    config['runtime_flight_data_by_date'] = Util.check_current_path(
        config_data.get('Path', 'runtime_flight_data_by_date'), current_path)
    config['runtime_flight_info'] = Util.check_current_path(config_data.get('Path', 'runtime_flight_info'),
                                                            current_path)
    config['output_flight_data_by_date'] = Util.check_current_path(
        config_data.get('Path', 'output_flight_data_by_date'), current_path)
    config['output_flight_map'] = Util.check_current_path(config_data.get('Path', 'output_flight_map'), current_path)
    config['output_flight_info'] = Util.check_current_path(config_data.get('Path', 'output_flight_info'), current_path)

    config['cat'] = config_data.get('FlightSeparator', 'cat')
    config['server_time_type'] = config_data.get('FlightSeparator', 'server_time_type')
    config['input_filename_pattern'] = config_data.get('FlightSeparator', 'input_filename_pattern')
    config['separated_flight_time_gap'] = config_data.get('FlightSeparator', 'separated_flight_time_gap')
    config['time_to_make_unchanged_folder'] = config_data.get('FlightSeparator', 'time_to_make_unchanged_folder')
    config['lines_seen_size'] = config_data.get('FlightSeparator', 'lines_seen_size')

    config['input_folder_pattern'] = config_data.get('FlightDataProcessor', 'input_folder_pattern')
    config['replace'] = config_data.get('FlightDataProcessor', 'replace')
    return config
