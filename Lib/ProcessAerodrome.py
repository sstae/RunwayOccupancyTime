import math
from shapely import geometry
from shapely.geometry.point import Point
# Center of the Donmuang airport
p = Point(13.912189, 100.605319)
# Radius for 4 NM from center
circle = p.buffer(0.068176)
list_point = circle.exterior.coords


def process_by_line(config, flight_info, content):
    if flight_info["direction"]["direction"] == "arrival":
        if "Aerodrome" not in flight_info:
            # first time
            flight_info["Aerodrome"] = {"Aerodrome_dict": {}}
        latitude = content['position']['lat']
        longitude = content['position']['lon']
        t1 = geometry.Point(latitude, longitude)
        Aerodrome_dict = flight_info["Aerodrome"]["Aerodrome_dict"]

        if "not_Aerodrome" not in Aerodrome_dict and not circle.intersects(t1):
            # if not circle.intersects(t1):
            Aerodrome_dict["not_Aerodrome"] = {"time_out": content["data_time"],
                                               "lat_out": content['position']['lat'],
                                               "lon_out": content['position']['lon']}

        elif not circle.intersects(t1):
            # if not circle.intersects(t1):
            Aerodrome_dict["not_Aerodrome"] = {"time_out": content["data_time"],
                                               "lat_out": content['position']['lat'],
                                               "lon_out": content['position']['lon']}

        elif "in_Aerodrome" not in Aerodrome_dict and circle.intersects(t1):
            Aerodrome_dict["in_Aerodrome"] = {"time_in": content["data_time"],
                                              "lat_in": content['position']['lat'],
                                              "lon_in": content['position']['lon']}


def process_final(config, flight_info):
    if flight_info["direction"]["direction"] == "arrival":
        Aerodrome_dict = flight_info["Aerodrome"]["Aerodrome_dict"]
        if len(Aerodrome_dict) == 1:
            print('cannot process summary time for Aerodrome ')
            flight_info["Aerodrome"]["time_diff"] = "unknown"
            flight_info["Aerodrome"]["velocity(NM./hr.)"] = "unknown"
            flight_info["Aerodrome"]["distance(km.)"] = "unknown"
            flight_info["Aerodrome"]["time_Aerodrome"] = "unknown"
        else:
            Aerodrome_dict = flight_info["Aerodrome"]["Aerodrome_dict"]
            if (Aerodrome_dict["in_Aerodrome"]["time_in"] - Aerodrome_dict["not_Aerodrome"]["time_out"]).seconds == 0:
                flight_info["Aerodrome"]["time_diff"] = (Aerodrome_dict["in_Aerodrome"]["time_in"] -
                                                         Aerodrome_dict["not_Aerodrome"]["time_out"]).microseconds
            elif (Aerodrome_dict["in_Aerodrome"]["time_in"] - Aerodrome_dict["not_Aerodrome"]["time_out"]).seconds >= 1:
                flight_info["Aerodrome"]["time_diff"] = (Aerodrome_dict["in_Aerodrome"]["time_in"] -
                                                         Aerodrome_dict["not_Aerodrome"]["time_out"]).seconds
            process_velocity(config, flight_info)


def process_velocity(config, flight_info):
    if flight_info["direction"]["direction"] == "arrival":
        Aerodrome_dict = flight_info["Aerodrome"]["Aerodrome_dict"]
        lat_out = Aerodrome_dict["not_Aerodrome"]["lat_out"]
        lon_out = Aerodrome_dict["not_Aerodrome"]["lon_out"]
        lat_in = Aerodrome_dict["in_Aerodrome"]["lat_in"]
        lon_in = Aerodrome_dict["in_Aerodrome"]["lon_in"]
        distance = math.hypot(lat_in - lat_out, lon_in - lon_out)
        if flight_info["Aerodrome"]["time_diff"] == "unknown":
            flight_info["Aerodrome"]["velocity(NM./hr.)"] = "unknown"
            flight_info["Aerodrome"]["distance(km.)"] = "unknown"
            flight_info["Aerodrome"]["time_Aerodrome"] = "unknown"
        else:
            if (Aerodrome_dict["in_Aerodrome"]["time_in"] - Aerodrome_dict["not_Aerodrome"]["time_out"]).seconds == 0:
                velocity = (distance * 100 * 3600) / (flight_info["Aerodrome"]["time_diff"] * float(1.852) * float(0.000001))
                flight_info["Aerodrome"]["distance(km.)"] = (distance * 100)
                flight_info["Aerodrome"]["velocity(NM./hr.)"] = velocity
                flight_info["Aerodrome"]["time_Aerodrome"] = Aerodrome_dict["in_Aerodrome"]["time_in"]

            elif (Aerodrome_dict["in_Aerodrome"]["time_in"] - Aerodrome_dict["not_Aerodrome"]["time_out"]).seconds >= 1:
                velocity = (distance * 100 * 3600) / (flight_info["Aerodrome"]["time_diff"] * float(1.852))
                flight_info["Aerodrome"]["distance(km.)"] = (distance * 100)
                flight_info["Aerodrome"]["velocity(NM./hr.)"] = velocity
                flight_info["Aerodrome"]["time_Aerodrome"] = Aerodrome_dict["in_Aerodrome"]["time_in"]



