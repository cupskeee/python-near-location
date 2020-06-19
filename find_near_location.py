import os
import csv
import json
from math import radians, cos, sin, asin, sqrt

from config import *
from data import location_data


def haversine(current_long, current_lat, location):
    lon1, lat1, lon2, lat2 = map(radians, [current_long, current_lat, float(location["long"]), float(location["lat"])])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    if RESULT_MEASUREMENT_SYSTEM:
        r = EARTH_RADIUS_IN_MILES
    else:
        r = EARTH_RADIUS_IN_KM

    return round(c * r, 2)


def nearloc_from_variable(current_lat, current_long):
    nearloc = []

    for location in location_data:
        location["distance"] = haversine(current_long, current_lat, location)
        if RESULT_TYPE:
            if location["distance"] <= MAX_RADIUS:
                print("'{}' is {} {} away from you.".format(location["name"],
                                                            location["distance"],
                                                            "mi" if RESULT_MEASUREMENT_SYSTEM else "km"))
                nearloc.append(location)
        else:
            print("'{}' is {} {} away from you.".format(location["name"],
                                                        location["distance"],
                                                        "mi" if RESULT_MEASUREMENT_SYSTEM else "km"))
            nearloc.append(location)
    nearloc = sorted(nearloc, key=lambda k: k["distance"])
    with open('result.json', 'w') as file:
        json.dump(nearloc, file)

    return nearloc


def nearloc_from_xlsx(current_lat, current_long):
    nearloc = []

    with open('data.csv', mode='r') as csv_file:
        location_data = csv.DictReader(csv_file)
        for location in location_data:
            location["distance"] = haversine(current_long, current_lat, location)
            if RESULT_TYPE == 0:
                print("'{}' is {} {} away from you.".format(location["name"],
                                                            location["distance"],
                                                            "mi" if RESULT_MEASUREMENT_SYSTEM else "km"))
                nearloc.append(location)
            else:
                if location["distance"] <= MAX_RADIUS:
                    print("'{}' is {} {} away from you.".format(location["name"],
                                                                location["distance"],
                                                                "mi" if RESULT_MEASUREMENT_SYSTEM else "km"))
                    nearloc.append(location)
    nearloc = sorted(nearloc, key=lambda k: k["distance"])
    with open('result.json', 'w') as file:
        json.dump(nearloc, file)
    return nearloc


if __name__ == "__main__":
    while True:
        try:
            current_lat = float(input("Your latitude : "))
        except ValueError:
            print("\nInvalid value, please insert a Float number !\n")
        else:
            if not (-90 < current_lat < 90):
                print("\nInvalid latitude, please insert a valid latitude (e.g. between -90.0 and 90.0)\n")
            else:
                break
    while True:
        try:
            current_long = float(input("Your longitude : "))
        except ValueError:
            print("\nInvalid value, please insert a Float number !\n")
        else:
            if not (-180 < current_long < 180):
                print("\nInvalid longitude, please insert a valid longitude (e.g. between -180.0 and 180.0)\n")
            else:
                break
    while True:
        choice = int(input("Which data source would you like to check ?\n"
                           "[0] : from data.py location_data variable\n"
                           "[1] : from data.xlsx (follow the format)\n"
                           "Choose from 0 or 1 : "))
        if choice == 0:
            result = nearloc_from_variable(current_lat, current_long)
            break
        elif choice == 1:
            result = nearloc_from_xlsx(current_lat, current_long)
            break
        else:
            print("\nInvalid option !\n")
    print("\nResult has been saved to result.json")
