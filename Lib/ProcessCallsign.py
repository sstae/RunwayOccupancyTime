def process_by_line(config, flight_info, content):
    if "callsign" not in flight_info:
        # first time
        flight_info["callsign"] = {"callsign": "", "callsign_list":{}}
    callsign = content['callsign']
    if callsign in flight_info["callsign"]["callsign_list"]:
        flight_info["callsign"]["callsign_list"][callsign] = flight_info["callsign"]["callsign_list"][callsign] + 1
    else:
        flight_info["callsign"]["callsign_list"][callsign] = 1


def process_final(config, flight_info):
    if "callsign" not in flight_info:
        print('cannot process callsign summary')
    else:
        # find first max_count
        callsign_dict = flight_info["callsign"]["callsign_list"]
        max_count = 0
        callsign = ""
        for key in callsign_dict:
            if key != '' and callsign_dict[key] > max_count:
                callsign = key
                max_count = callsign_dict[key]
        if callsign != "":
            flight_info["callsign"]["callsign"] = callsign
