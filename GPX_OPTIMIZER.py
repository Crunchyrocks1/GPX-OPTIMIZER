import sys
import math
import gpxpy
import gpxpy.gpx
import time


# basic script using haversine formula to get disantce and optimize the best.



pokestopRadius = 10  # Meters

logo = """
   _____ _______   __
  / ____|  __ \ \ / /
 | |  __| |__) \ V / 
 | | |_ |  ___/ > <  
 | |__| | |    / . \\ 
  \\_____|_|   /_/ \\_\\ By Crunchy \n\n Please Paste Coordinates Below!
  """


def haversine(coord1, coord2):
    R = 6371000
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def optimize_coordinates(coords, radius=40):
    optimized = []
    log = []
    coords = sorted(coords, key=lambda x: (x[0], x[1]))

    log.append("Trying rearranged from closest to farthest... [DONE]")

    for i, coord in enumerate(coords):
        for existing in optimized:
            distance = haversine(coord, existing)
            log.append(f"set {len(log)}: {coord} -> {existing} Distance: {distance:.2f}m")
        if all(haversine(coord, existing) > radius for existing in optimized):
            optimized.append(coord)

    return optimized, log


def main():
    print(logo)

    coords = []

    while True:
        try:
            line = input().strip()
            if not line:
                break
            lat, lon = map(float, line.split(","))
            coords.append((lat, lon))
        except ValueError:
            print("Invalid format. Please enter coordinates in the format: lat,lon")

    optimized_coords, log = optimize_coordinates(coords, pokestopRadius)

    print("\n [DONE] --> Optimized Coordinates: ")
    for coord in optimized_coords:
        print(f"{coord[0]},{coord[1]}")

    gpx = gpxpy.gpx.GPX()

    for coord in optimized_coords:
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(coord[0], coord[1]))

    with open('NewGpx.gpx', 'w') as gpx_file:
        gpx_file.write(gpx.to_xml())

    print("\n [LOG] --> GPX file saved.")

    with open('log.txt', 'w') as log_file:
        log_file.write("\n".join(log))

    print(" [LOG] --> Log saved to log.txt")
    time.sleep(5)


if __name__ == "__main__":
    main()
