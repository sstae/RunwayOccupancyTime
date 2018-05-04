from shapely import geometry


def initial():
    # zone1
    bay_zone1_1 = geometry.Point(13.926808, 100.609471)
    bay_zone1_2 = geometry.Point(13.927743, 100.607687)
    bay_zone1_3 = geometry.Point(13.925472, 100.606641)
    bay_zone1_4 = geometry.Point(13.924613, 100.608238)
    # zone2
    bay_zone2_1 = geometry.Point(13.924613, 100.608238)
    bay_zone2_2 = geometry.Point(13.925472, 100.606641)
    bay_zone2_3 = geometry.Point(13.923419, 100.605120)
    bay_zone2_4 = geometry.Point(13.922369, 100.606968)
    # zone3
    bay_zone3_1 = geometry.Point(13.922369, 100.606968)
    bay_zone3_2 = geometry.Point(13.923419, 100.605120)
    bay_zone3_3 = geometry.Point(13.921070, 100.603781)
    bay_zone3_4 = geometry.Point(13.920063, 100.605743)
    # zone4
    bay_zone4_1 = geometry.Point(13.920063, 100.605743)
    bay_zone4_2 = geometry.Point(13.921070, 100.603781)
    bay_zone4_3 = geometry.Point(13.918835, 100.602524)
    bay_zone4_4 = geometry.Point(13.917866, 100.604453)
    # zone5
    bay_zone5_1 = geometry.Point(13.917866, 100.604453)
    bay_zone5_2 = geometry.Point(13.918835, 100.602524)
    bay_zone5_3 = geometry.Point(13.916601, 100.601254)
    bay_zone5_4 = geometry.Point(13.915643, 100.603213)
    # zone6
    bay_zone6_1 = geometry.Point(13.915643, 100.603213)
    bay_zone6_2 = geometry.Point(13.916601, 100.601254)
    bay_zone6_3 = geometry.Point(13.914438, 100.599945)
    bay_zone6_4 = geometry.Point(13.913377, 100.601880)
    # zone7
    bay_zone7_1 = geometry.Point(13.913377, 100.601880)
    bay_zone7_2 = geometry.Point(13.914438, 100.599945)
    bay_zone7_3 = geometry.Point(13.912146, 100.598606)
    bay_zone7_4 = geometry.Point(13.911122, 100.600543)
    # zone8
    bay_zone8_1 = geometry.Point(13.911122, 100.600543)
    bay_zone8_2 = geometry.Point(13.912146, 100.598606)
    bay_zone8_3 = geometry.Point(13.909612, 100.597208)
    bay_zone8_4 = geometry.Point(13.908859, 100.598804)
    # zone9
    bay_zone9_1 = geometry.Point(13.908135, 100.599961)
    bay_zone9_2 = geometry.Point(13.909612, 100.597208)
    bay_zone9_3 = geometry.Point(13.906434, 100.595616)
    bay_zone9_4 = geometry.Point(13.905193, 100.598112)
    # zone10
    bay_zone10_1 = geometry.Point(13.905193, 100.598112)
    bay_zone10_2 = geometry.Point(13.906434, 100.595616)
    bay_zone10_3 = geometry.Point(13.903057, 100.593441)
    bay_zone10_4 = geometry.Point(13.901458, 100.596293)
    # zone11
    bay_zone11_1 = geometry.Point(13.901458, 100.596293)
    bay_zone11_2 = geometry.Point(13.903057, 100.593441)
    bay_zone11_3 = geometry.Point(13.898988, 100.591297)
    bay_zone11_4 = geometry.Point(13.897836, 100.594156)

    # Create square from point lists
    point_list_zone1 = [bay_zone1_1, bay_zone1_2, bay_zone1_3, bay_zone1_4, bay_zone1_1]
    point_list_zone2 = [bay_zone2_1, bay_zone2_2, bay_zone2_3, bay_zone2_4, bay_zone2_1]
    point_list_zone3 = [bay_zone3_1, bay_zone3_2, bay_zone3_3, bay_zone3_4, bay_zone3_1]
    point_list_zone4 = [bay_zone4_1, bay_zone4_2, bay_zone4_3, bay_zone4_4, bay_zone4_1]
    point_list_zone5 = [bay_zone5_1, bay_zone5_2, bay_zone5_3, bay_zone5_4, bay_zone5_1]
    point_list_zone6 = [bay_zone6_1, bay_zone6_2, bay_zone6_3, bay_zone6_4, bay_zone6_1]
    point_list_zone7 = [bay_zone7_1, bay_zone7_2, bay_zone7_3, bay_zone7_4, bay_zone7_1]
    point_list_zone8 = [bay_zone8_1, bay_zone8_2, bay_zone8_3, bay_zone8_4, bay_zone8_1]
    point_list_zone9 = [bay_zone9_1, bay_zone9_2, bay_zone9_3, bay_zone9_4, bay_zone9_1]
    point_list_zone10 = [bay_zone10_1, bay_zone10_2, bay_zone10_3, bay_zone10_4, bay_zone10_1]
    point_list_zone11 = [bay_zone11_1, bay_zone11_2, bay_zone11_3, bay_zone11_4, bay_zone11_1]

    # Create Polygon
    polygon_bay1 = geometry.Polygon([[p.x, p.y] for p in point_list_zone1])
    polygon_bay2 = geometry.Polygon([[p.x, p.y] for p in point_list_zone2])
    polygon_bay3 = geometry.Polygon([[p.x, p.y] for p in point_list_zone3])
    polygon_bay4 = geometry.Polygon([[p.x, p.y] for p in point_list_zone4])
    polygon_bay5 = geometry.Polygon([[p.x, p.y] for p in point_list_zone5])
    polygon_bay6 = geometry.Polygon([[p.x, p.y] for p in point_list_zone6])
    polygon_bay7 = geometry.Polygon([[p.x, p.y] for p in point_list_zone7])
    polygon_bay8 = geometry.Polygon([[p.x, p.y] for p in point_list_zone8])
    polygon_bay9 = geometry.Polygon([[p.x, p.y] for p in point_list_zone9])
    polygon_bay10 = geometry.Polygon([[p.x, p.y] for p in point_list_zone10])
    polygon_bay11 = geometry.Polygon([[p.x, p.y] for p in point_list_zone11])

    # Put polygon into Dictionary
    bay_dict = {
        "zone1": polygon_bay1,
        "zone2": polygon_bay2,
        "zone3": polygon_bay3,
        "zone4": polygon_bay4,
        "zone5": polygon_bay5,
        "zone6": polygon_bay6,
        "zone7": polygon_bay7,
        "zone8": polygon_bay8,
        "zone9": polygon_bay9,
        "zone10": polygon_bay10,
        "zone11": polygon_bay11}
    return bay_dict


def process_by_line(config, flight_info, content):
    if "bay" not in flight_info:
        # first time
        flight_info["bay"] = {"bay": "unknown", "bay_layout": initial(), "bay_dict": {}}
    latitude = content['position']['lat']
    longitude = content['position']['lon']
    t1 = geometry.Point(latitude, longitude)
    bay_layout = flight_info["bay"]["bay_layout"]
    bay_dict = flight_info["bay"]["bay_dict"]
    # for loop since zone1 until zone11
    current_bay = "not_bay"
    for zone_name in bay_layout:
        if bay_layout[zone_name].intersects(t1):
            current_bay = zone_name
            break
    # if the first lat/lon is not in zone1, it will create "" for the first value in the listofBAY.
    if current_bay not in bay_dict:
        bay_dict[current_bay] = {"first": content["data_time"], "last": content["data_time"]}
    else:
        bay_dict[current_bay]["last"] = content["data_time"]


def process_final(config, flight_info):
    if ("bay" not in flight_info) or ("direction" not in flight_info):
        print('cannot process bay summary')
    else:
        bay_dict = flight_info["bay"]["bay_dict"]
        direction = flight_info["direction"]["direction"]
        if direction == "arrival":
            flight_info["bay"]["bay"] = get_last_bay(bay_dict)
        elif direction == "departure":
            flight_info["bay"]["bay"] = get_first_bay(bay_dict)
        else:
            flight_info["bay"]["bay"] = "unknown"


def get_last_bay(bay_dict):
    last_bay = ""
    last_datetime = None
    for key in bay_dict:
        if key != "not_bay":
            if (last_bay == "") or (bay_dict[key]["last"] > last_datetime):
                last_bay = key
                last_datetime = bay_dict[key]["last"]
    if last_bay == "":
        return "unknown"
    else:
        return last_bay


def get_first_bay(bay_dict):
    first_bay = ""
    first_datetime = None
    for key in bay_dict:
        if key != "not_bay":
            if (first_bay == "") or (bay_dict[key]["first"] < first_datetime):
                first_bay = key
                first_datetime = bay_dict[key]["first"]
    if first_bay == "":
        return "unknown"
    else:
        return first_bay
