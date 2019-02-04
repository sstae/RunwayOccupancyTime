import math

from shapely import geometry
from decimal import Decimal


def process_by_line(config, flight_info, content):
    if "runway" not in flight_info:
        # first time
        flight_info["runway"] = {"runway": "unknown", "runway_layout": initial(), "runway_dict": {},
                                 "prev_content": {}, "prev_runway": None}
    latitude = content['position']['lat']
    longitude = content['position']['lon']
    t1 = geometry.Point(latitude, longitude)
    runway_dict = flight_info["runway"]["runway_dict"]
    runway_layout = flight_info["runway"]["runway_layout"]
    current_runway = "not_runway"
    # for loop since polygon_runway1 until polygon_runway4
    for runway in runway_layout:
        if runway_layout[runway].intersects(t1):
            current_runway = runway
            break
    if flight_info["runway"]["prev_runway"] is not None:
        if flight_info["runway"]["prev_runway"] != current_runway:
            if flight_info["runway"]["prev_runway"] == "not_runway":
                # in runway
                set_runway("in", runway_dict, current_runway, flight_info["runway"]["prev_content"], content)
            elif current_runway == "not_runway":
                # out runway
                set_runway("out", runway_dict, flight_info["runway"]["prev_runway"],
                           flight_info["runway"]["prev_content"], content)
            else:
                set_runway("out", runway_dict, flight_info["runway"]["prev_runway"],
                           flight_info["runway"]["prev_content"], content)
                set_runway("in", runway_dict, current_runway, flight_info["runway"]["prev_content"], content)
    flight_info["runway"]["prev_runway"] = current_runway
    flight_info["runway"]["prev_content"] = content


def set_runway(condition, runway_dict, runway_name, prev_content, content):
    if runway_name not in runway_dict:
        runway_dict[runway_name] = {}
    if condition not in runway_dict[runway_name]:
        runway_dict[runway_name][condition] = {"first_1": prev_content,
                                               "first_2": content,
                                               "last_1": prev_content,
                                               "last_2": content}
    else:
        runway_dict[runway_name][condition]["last_1"] = prev_content
        runway_dict[runway_name][condition]["last_2"] = content


def initial():
    # runway_dict = {}
    # Stopway of R21
    stopway_R21_1  = geometry.Point(13.92767, 100.61278)
    R21_1          = geometry.Point(13.92663, 100.61221) #R21 Threshold
    stopway_R21_2  = geometry.Point(13.927413, 100.613330) ##R21 Threshold
    R21_2          = geometry.Point(13.92739, 100.61332)

    # Runway R
    R21_1 = geometry.Point(13.92663, 100.61221) #R21 Threshold
    R03_1 = geometry.Point(13.89697, 100.59556) #R03 Threshold
    R03_2 = geometry.Point(13.89667, 100.59611) #R03 Threshold
    R21_2 = geometry.Point(13.92634, 100.61274) #R21 Threshold

    # Stopway of R03
    R03_1 = geometry.Point(13.89697, 100.59556) #R03 Threshold
    stopway_R03_1 = geometry.Point(13.89597, 100.595)
    R03_2 = geometry.Point(13.89667, 100.59611)
    stopway_R03_2 = geometry.Point(13.895652, 100.595509) #R03 Threshold

    # Stopway of L21
    stopways_L21_1 = geometry.Point(13.92781, 100.61706)
    stopways_L21_2 = geometry.Point(13.92744, 100.61685)
    stopways_L21_3 = geometry.Point(13.92719, 100.61733)
    stopways_L21_4 = geometry.Point(13.92757, 100.61754)

    # Runway L
    L21_1 = geometry.Point(13.92443, 100.61518)
    L03_1 = geometry.Point(13.89957, 100.60123) #L03 Threshold
    L03_2 = geometry.Point(13.89930, 100.60170) #L03 Threshold
    L21_2 = geometry.Point(13.92417, 100.61564)

    # Stopway of L03
    L03_1 = geometry.Point(13.89957, 100.60123)
    stopway_L03_1 = geometry.Point(13.89886, 100.60082)
    stopway_L03_2 = geometry.Point(13.89859, 100.60131)
    L03_2 = geometry.Point(13.89930, 100.60170)


    # Point list
    point_rwy_R = [R21_1, R03_1, R03_2, R21_2, R21_1]
    point_rwy_L = [L21_1, L03_1, L03_2, L21_2, L21_1]
    point_stpwy_R21 = [stopway_R21_1, R21_1, R21_2, stopway_R21_2, stopway_R21_1]
    point_stpwy_L21 = [stopways_L21_1, L21_1, L21_2, stopways_L21_4]
    point_stpwy_R03 = [R03_1, stopway_R03_1, stopway_R03_2, R03_2, R03_1]
    point_stpwy_L03 = [L03_1, stopway_L03_1, stopway_L03_2, L03_2, L03_1]

    # Polygon list
    polygon_rwy_R = geometry.Polygon([[p.x, p.y] for p in point_rwy_R])
    polygon_rwy_L = geometry.Polygon([[p.x, p.y] for p in point_rwy_L])
    polygon_stpwy_R21 = geometry.Polygon([[p.x, p.y] for p in point_stpwy_R21])
    polygon_stpwy_L21 = geometry.Polygon([[p.x, p.y] for p in point_stpwy_L21])
    polygon_stpwy_R03 = geometry.Polygon([[p.x, p.y] for p in point_stpwy_R03])
    polygon_stpwy_L03 = geometry.Polygon([[p.x, p.y] for p in point_stpwy_L03])

    runway_dict = {"rwy21R": polygon_stpwy_R21,
                   "rwy21L": polygon_stpwy_L21,
                   "rwy03R": polygon_stpwy_R03,
                   "rwy03L": polygon_stpwy_L03,
                   "rwyR": polygon_rwy_R,
                   "rwyL": polygon_rwy_L}
    return runway_dict


def process_final(config, flight):
    if "runway" not in flight:
        print('cannot process runway summary')
    else:
        runway_dict = flight["runway"]["runway_dict"]
        print("runway_dict", runway_dict)
        runway_order = get_runway_order(runway_dict)
        runway_layout = flight["runway"]["runway_layout"]

        direction = flight["direction"]["direction"]
        if len(runway_dict) == 3 and direction == "arrival":
            flight["runway"]["runway"] = runway_order[0]
            if len(runway_dict[runway_order[1]]) == 2 and len(runway_dict[runway_order[2]]) == 2:
                flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[0], "in",
                                                                             runway_dict[runway_order[0]])
                flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[1], "out",
                                                                           runway_dict[runway_order[1]])
                flight["runway"]["runway_time"] = (
                        flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
            else:
                flight["runway"]["runway_start_dt"] = "unknown"
                flight["runway"]["runway_end_dt"] = "unknown"
                flight["runway"]["runway_time"] = "unknown"

        elif len(runway_dict) == 3 and direction == "departure":
            flight["runway"]["runway"] = runway_order[2]
            if len(runway_dict[runway_order[1]]) == 2 and len(runway_dict[runway_order[2]]) == 2:
                flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[1], "in",
                                                                             runway_dict[runway_order[1]])
                flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[2], "out",
                                                                           runway_dict[runway_order[2]])
                flight["runway"]["runway_time"] = (
                        flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
            else:
                flight["runway"]["runway_start_dt"] = "unknown"
                flight["runway"]["runway_end_dt"] = "unknown"
                flight["runway"]["runway_time"] = "unknown"

        elif len(runway_dict) == 2 and direction == "arrival":
            flight["runway"]["runway"] = runway_order[0]
            if len(runway_dict[runway_order[0]]) == 2 and len(runway_dict[runway_order[1]]) == 2:
                flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[0], "in",
                                                                             runway_dict[runway_order[0]])
                flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[1], "out",
                                                                           runway_dict[runway_order[1]])
                flight["runway"]["runway_time"] = (
                        flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
            else:
                flight["runway"]["runway_start_dt"] = "unknown"
                flight["runway"]["runway_end_dt"] = "unknown"
                flight["runway"]["runway_time"] = "unknown"

        elif len(runway_dict) == 2 and direction == "departure":
            flight["runway"]["runway"] = runway_order[1]
            if len(runway_dict[runway_order[0]]) == 2 and len(runway_dict[runway_order[1]]) == 2:
                flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[0], "in",
                                                                             runway_dict[runway_order[0]])
                flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[1], "out",
                                                                           runway_dict[runway_order[1]])
                flight["runway"]["runway_time"] = (
                        flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
            else:
                flight["runway"]["runway_start_dt"] = "unknown"
                flight["runway"]["runway_end_dt"] = "unknown"
                flight["runway"]["runway_time"] = "unknown"

        else:
            flight["runway"]["runway"] = "unknown"
            flight["runway"]["runway_start_dt"] = "unknown"
            flight["runway"]["runway_end_dt"] = "unknown"
            flight["runway"]["runway_time"] = "unknown"


def get_time_across_runway(runway_layout, runway_name, condition, runway): #fixed
    if condition in runway:
        print(runway)
        p1_lat = runway[condition]["first_1"]["position"]["lat"]
        p1_lon = runway[condition]["first_1"]["position"]["lon"]
        p2_lat = runway[condition]["first_2"]["position"]["lat"]
        p2_lon = runway[condition]["first_2"]["position"]["lon"]
        t1 = runway[condition]["first_1"]["data_time"]

        t2 = runway[condition]["first_2"]["data_time"]
        # use condition to identify p1 in runway
        # condition = in p2 , p1
        # condition = out p1 , p2
        if condition == "in":
            x = find_intersection_point(p2_lat, p2_lon, p1_lat, p1_lon, runway_layout[runway_name])
            print(Decimal(x[0]))
            print(Decimal(x[1]))
            tx = intersect_runway_time(t1, t2, p2_lat, p2_lon, p1_lat, p1_lon, Decimal(x[0]), Decimal(x[1]))
            return tx

        elif condition == "out":
            x = find_intersection_point(p1_lat, p1_lon, p2_lat, p2_lon, runway_layout[runway_name])
            print(Decimal(x[0]))
            print(Decimal(x[1]))
            tx = intersect_runway_time(t1, t2, p1_lat, p1_lon, p2_lat, p2_lon, Decimal(x[0]), Decimal(x[1]))
            return tx

    else:
        return None


def get_runway_order(runway_dict):
    runway = []
    for key in runway_dict:
        runway.append(key)
    print(runway)
    return runway


def intersect_runway_time(t1, t2, p1_lat, p1_lon, p2_lat, p2_lon, x_lat, x_lon):
    d1 = math.hypot(p1_lat - x_lat, p1_lon - x_lon)
    d2 = math.hypot(p1_lat - p2_lat, p1_lon - p2_lon)
    # delta_time = (t2 - t1)
    tdiff = (d1 * (t2 - t1)) / d2
    tx = t1 + tdiff
    return tx


def find_intersection_point(p1_lat, p1_lon, p2_lat, p2_lon, polygon):
    line = [(p1_lat, p1_lon), (p2_lat, p2_lon)]
    shapely_line = geometry.LineString(line)
    intersection_line = list(polygon.intersection(shapely_line).coords)
    return intersection_line[1]


