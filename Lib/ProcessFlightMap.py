from Lib import Util
import gmplot
import os


filename = "C:\\Users\\Pipat_P\\Desktop\\RunwayOccupancyTime\\Runtime\\FlightDataByDate\\20180321_\\CAT20\\881b6a_00"


# Function for plotting in Google Map
def InitialProcessPlot(filename, config):
    print(filename)
    date = filename.split("\\")[-3]
    file = filename.split("\\")[-1]
    print(date)
    ProcessEachfile(filename, file, date, config)


def ProcessEachfile(filename, file, date, config):
    coords = []
    with open(filename, "r") as f:
        # for row in f:
        #     lat_long = row.split()[3]
        #     coords.append(lat_long)
        for line in f:
            data = Util.json_load(line)
            lat_long = data['position']
            coords.append(lat_long)
    PoltGoogleMap(coords, filename, file, date, config)


# take a string that is a pair of points, return an array of floats
def clean_coord(my_coord):
    # my_coord = my_coord.split(',')
    # my_coord = [float(sc) for sc in my_coord]
    out_coord = []
    out_coord.append(float(my_coord['lat']))
    out_coord.append(float(my_coord['lon']))
    return out_coord


def PoltGoogleMap(coords, filename, file, date, config):
    # define the map startingoutputdata\\20180322\\CAT20\\8a02ca_01
    gmap = gmplot.GoogleMapPlotter(clean_coord(coords[0])[0], clean_coord(coords[0])[1], 13)
    # loop through all coordinates and grab lats/lons
    lats = []
    lons = []
    for c in coords:
        gmap_coord = clean_coord(c)
        lats.append(gmap_coord[0])
        lons.append(gmap_coord[1])
    # add points to map
    gmap.scatter(lats, lons, 'red', size=7, marker=False)

    Directory = config['output_flight_map'] + "\\" + date + "\\" + "HTML"
    if not os.path.exists(Directory):
        os.makedirs(Directory)
    output_filename = Directory + "\\" + file + ".html"
    # save to map
    gmap.draw(output_filename)

