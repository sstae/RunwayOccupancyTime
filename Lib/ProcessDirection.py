
def process_by_line(config, flight_info, content):
    if "direction" not in flight_info:
        # first time
        flight_info["direction"] = {"direction": "unknown", "trend_count_threshold": 5, "last_flight_level": None,
                                    "trend": "unknown", "trend_count": 0}
    if flight_info["direction"]["direction"] == "unknown":
        # process if not assign the direction yet
        # determine trend
        current_trend = "unknown"
        if flight_info["direction"]["last_flight_level"] is not None and 'height' in content \
                and 'flight_level' in content['height'] and content['height']['flight_level'] is not None:
            # print(flight["direction"]["last_flight_level"])
            # print(content['height']['flight_level'])
            if int(flight_info["direction"]["last_flight_level"]) > int(content['height']['flight_level']):
                current_trend = "arrival"
            elif int(flight_info["direction"]["last_flight_level"]) < int(content['height']['flight_level']):
                current_trend = "departure"
            else:
                current_trend = "unknown"
        # process trend
        if current_trend == "unknown":
            flight_info["direction"]["trend"] == "unknown"
            flight_info["direction"]["trend_count"] = 0
        elif current_trend == flight_info["direction"]["trend"]:
            flight_info["direction"]["trend_count"] = flight_info["direction"]["trend_count"] + 1
        else:
            flight_info["direction"]["trend"] = current_trend
            flight_info["direction"]["trend_count"] = 1
        # assign direction if possible
        if flight_info["direction"]["trend_count"] > flight_info["direction"]["trend_count_threshold"]:
            flight_info["direction"]["direction"] = flight_info["direction"]["trend"]
        # update last_flight_level
        flight_info["direction"]["last_flight_level"] = content['height']['flight_level']
