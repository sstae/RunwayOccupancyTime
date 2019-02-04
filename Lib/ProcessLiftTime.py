def process_by_line(config, flight_info, content):
    if "lift" not in flight_info:
    # first time
        flight_info["lift"] = {"time": "unknown", "trend_count_threshold": 3, "last_flight_level": None,
                               "trend": "No Lift", "trend_count": 0}
    if flight_info["lift"]["time"] == "unknown":
        current_trend = "No Lift"
        if flight_info["lift"]["last_flight_level"] is not None and 'height' in content \
                and 'flight_level' in content['height'] and content['height']['flight_level'] is not None:
            if flight_info["lift"]["last_flight_level"] != content['height']['flight_level']:
                current_trend = "Lift"
            else:
                current_trend = "No Lift"
        if current_trend == "No Lift":
            flight_info["lift"]["trend_count"] = 0
        else:
            flight_info["lift"]["trend"] = "Lift"
            flight_info["lift"]["trend_count"] = flight_info["lift"]["trend_count"] + 1

        if flight_info["lift"]["trend_count"] > flight_info["lift"]["trend_count_threshold"]:
            flight_info["lift"]["time"] = content["data_time"]
        flight_info["lift"]["last_flight_level"] = content['height']['flight_level']











