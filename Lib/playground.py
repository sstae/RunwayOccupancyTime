import os
import pprint

from Lib import Config
from Lib import Util

Util.test('Hello')
current_path = os.path.dirname(os.path.abspath(__file__))
pp = pprint.PrettyPrinter(indent=4)

# initial config
# all_config = Config.initial_config(current_path, '.\\..\\config.txt')
# print("config:")
# pp.pprint(all_config)

filename = "C:\\Users\\Pipat_P\\Documents\\GitHub\\RunwayOccupancyTime\\Input\\FlightMovementByDate\\FLIGHT_20180321.txt"
with open(filename, "r") as f:
    for data in f:
       # lastline = f.readlines()[0]
       # print(lastline)
       flight_movement = {}
       elements = data.split(";")
       flight_movement["STATUS"] = elements[0]
       flight_movement["DOF"] = elements[1]
       flight_movement["FlightType"] = elements[2]
       flight_movement["REG"] = elements[3]
       flight_movement["MessageType"] = elements[4]
       flight_movement["CS"] = elements[5]
       flight_movement["AcType"] = elements[6]
       flight_movement["DEP"] = elements[7]
       flight_movement["ETD"] = elements[8]
       flight_movement["ATD"] = elements[9]
       flight_movement["Route"] = elements[10]
       flight_movement["DEST"] = elements[11]
       flight_movement["ETA"] = elements[12]
       flight_movement["ATA"] = elements[13]
       flight_movement["No"] = elements[14]
       flight_movement["Squawk"] = elements[15]
       flight_movement["FRULE"] = elements[16]
       flight_movement["WTURB"] = elements[17]
       flight_movement["COMNAV"] = elements[18]
       flight_movement["SPEED"] = elements[19]
       flight_movement["FLEVEL"] = elements[20]
       flight_movement["EET"] = elements[21]
       flight_movement["INBOUND"] = elements[22]
       flight_movement["OUTBOUDN"] = elements[23]
       flight_movement["ALTDEST"] = elements[24]
       flight_movement["ALTDEST2"] = elements[25]
       flight_movement["DLA"] = elements[26]
       flight_movement["CHG"] = elements[27]
       flight_movement["CNL"] = elements[28]
       flight_movement["Item18"] = elements[29]



       print(flight_movement["DOF"],flight_movement["SPEED"], flight_movement["CS"], flight_movement["ATA"], flight_movement["ETA"],
             flight_movement["ATD"], flight_movement["ETD"])