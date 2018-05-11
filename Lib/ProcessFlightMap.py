import os

import gmplot

from Lib import Util

filename = "C:\\Users\\Pipat_P\\Desktop\\RunwayOccupancyTime\\Runtime\\FlightDataByDate\\20180321_\\CAT20\\881b6a_00"


# Function for plotting in Google Map


def get_all_coordinates(input_filename):
    result = []
    with open(input_filename, "r") as f:
        for line in f:
            data = Util.json_load(line)
            lat_long = data['position']
            result.append(lat_long)
    return result


def prepare_data(flight_info):
    # TODO extract only some data for validation by joe
    return "test"


# take a string that is a pair of points, return an array of floats
def convert_to_float(my_coord):
    # my_coord = my_coord.split(',')
    # my_coord = [float(sc) for sc in my_coord]
    out_coord = []
    out_coord.append(float(my_coord['lat']))
    out_coord.append(float(my_coord['lon']))
    return out_coord



def inject_text_to_html(filename, flight_info):
    text = prepare_data(flight_info)
    # TODO open file by joe
    # TODO replace </body> with text + </body> by joe

def plot_google_map_to_file(config, filename, date, coordinates, flight_info):
    # define the map startingoutputdata\\20180322\\CAT20\\8a02ca_01
    first_float_coordinate = convert_to_float(coordinates[0])
    gmap = gmplot.GoogleMapPlotter(first_float_coordinate[0], first_float_coordinate[1], 13)
    # loop through all coordinates and grab lats/lons
    latitude_list = []
    longitude_list = []
    for c in coordinates:
        float_coordinate = convert_to_float(c)
        latitude_list.append(float_coordinate[0])
        longitude_list.append(float_coordinate[1])
    # add points to map
    gmap.scatter(latitude_list, longitude_list, 'red', size=7, marker=False)

    directory = config['output_flight_map'] + "\\" + date
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_filename = directory + "\\" + filename + ".html"
    # save to map
    gmap.draw(output_filename)
    inject_text_to_html(output_filename, flight_info)

def process_plot(config, input_filename, filename, date, flight_info):
    coordinates = get_all_coordinates(input_filename)
    plot_google_map_to_file(config, filename, date, coordinates, flight_info)
