import math

from shapely import geometry


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
    runway_point1 = geometry.Point(13.92649670244764, 100.6121817115145)
    runway_point2 = geometry.Point(13.91454494713619, 100.6054260689291)
    runway_point3 = geometry.Point(13.89716600000000, 100.5956400000000)
    runway_point4 = geometry.Point(13.92611504798200, 100.6127341377071)
    runway_point5 = geometry.Point(13.91428248723653, 100.6059061290093)
    runway_point6 = geometry.Point(13.89688100000000, 100.5962420000000)
    runway_point7 = geometry.Point(13.92737285374881, 100.6169742061147)
    runway_point8 = geometry.Point(13.91281787813946, 100.6087793256608)
    runway_point9 = geometry.Point(13.89956716145793, 100.6013471916915)
    runway_point10 = geometry.Point(13.92711706145504, 100.6173677765666)
    runway_point11 = geometry.Point(13.91252191775162, 100.6091176116703)
    runway_point12 = geometry.Point(13.89938636326239, 100.6017624507612)

    point_list_runway1 = [runway_point1, runway_point2, runway_point5, runway_point4, runway_point1]  # 21R
    point_list_runway2 = [runway_point2, runway_point3, runway_point6, runway_point5, runway_point2]  # 03L
    point_list_runway3 = [runway_point7, runway_point8, runway_point11, runway_point10, runway_point7]  # 21L
    point_list_runway4 = [runway_point8, runway_point9, runway_point12, runway_point11, runway_point8]  # 03R

    polygon_runway1 = geometry.Polygon([[p.x, p.y] for p in point_list_runway1])
    polygon_runway2 = geometry.Polygon([[p.x, p.y] for p in point_list_runway2])
    polygon_runway3 = geometry.Polygon([[p.x, p.y] for p in point_list_runway3])
    polygon_runway4 = geometry.Polygon([[p.x, p.y] for p in point_list_runway4])

    runway_dict = {"rwy21R": polygon_runway1,
                   "rwy21L": polygon_runway3,
                   "rwy03R": polygon_runway4,
                   "rwy03L": polygon_runway2}
    return runway_dict


def process_final(config, flight):
    if "runway" not in flight:
        print('cannot process runway summary')
    else:
        runway_dict = flight["runway"]["runway_dict"]
        print("runway_dict", runway_dict)
        runway_order = get_runway_order(runway_dict)
        runway_layout = flight["runway"]["runway_layout"]
        if len(runway_dict) == 3:
            flight["runway"]["runway"] = runway_order[1]
            flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[1], "in",
                                                                         runway_dict[runway_order[1]])
            flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[2], "out",
                                                                       runway_dict[runway_order[2]])
            flight["runway"]["runway_time"] = (
                    flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
        elif len(runway_dict) == 2:
            flight["runway"]["runway"] = runway_order[0]
            flight["runway"]["runway_start_dt"] = get_time_across_runway(runway_layout, runway_order[0], "in",
                                                                         runway_dict[runway_order[0]])
            flight["runway"]["runway_end_dt"] = get_time_across_runway(runway_layout, runway_order[1], "out",
                                                                       runway_dict[runway_order[1]])
            flight["runway"]["runway_time"] = (
                    flight["runway"]["runway_end_dt"] - flight["runway"]["runway_start_dt"]).seconds
        else:
            flight["runway"]["runway"] = "unknown"


def get_time_across_runway(runway_layout, condition, runway_name, runway):
    if condition in runway:
        p1_lat = runway[condition]["first_1"]["lat"]
        p1_lon = runway[condition]["first_1"]["lon"]
        p2_lat = runway[condition]["first_2"]["lat"]
        p2_lon = runway[condition]["first_2"]["lon"]
        t1 = runway[condition]["first_1"]["data_time"]
        t2 = runway[condition]["first_2"]["data_time"]
        x = find_intersection_point(p1_lat, p1_lon, p2_lat, p2_lon, runway_layout[runway_name])
        tx = intersect_runway_time(t1, t2, p1_lat, p1_lon, p2_lat, p2_lon, x[0], x[1])
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
    tx = (d1(t2 - t1)) / d2
    return tx


def find_intersection_point(p1_lat, p1_lon, p2_lat, p2_lon, polygon):
    line = [(p1_lat, p1_lon), (p2_lat, p2_lon)]
    shapely_line = geometry.LineString(line)
    intersection_line = list(polygon.intersection(shapely_line).coords)
    return intersection_line[1]
