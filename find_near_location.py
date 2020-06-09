import json

from config import *
from math import radians, cos, sin, asin, sqrt
from data import location_data


def nearloc_from_variable(current_latitude, current_longitude):
    nearloc = []

    for location in location_data:
        lon1, lat1, lon2, lat2 = map(radians, [current_longitude, current_latitude, location["long"], location["lat"]])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        if RESULT_MEASUREMENT_SYSTEM == 0:
            r = EARTH_RADIUS_IN_KM
        else:
            r = EARTH_RADIUS_IN_MILES

        location["distance"] = round(c * r, 2)
        if RESULT_TYPE == 0:
            nearloc.append(location)
        else:
            if location["distance"] <= MAX_RADIUS:
                nearloc.append(location)
    nearloc = sorted(nearloc, key=lambda k: k["distance"])
    with open('result.json','w') as file:
        json.dump(nearloc, file)

    return nearloc

def nearloc_from_xlsx(current_lat, current_long):
    print("\nThis feature is not available yet!!\n")
    return []


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
    print(result)
    print("\nResult has been saved to result.json")
    
