import requests
from lxml import html
import re
from collections import defaultdict
import math
from math import sin, cos


def to_decimal(deg_min: str) -> float:
    """
    Convert Lat and Long from degree, minute, second format to decimal format.
    :param deg_min: Lat or Long in degree, minute format.
    :return: Lat or Long in decimal format.
    """

    degree, minute, direction = re.findall(r"[0-9A-Z]+", deg_min)
    in_decimal = int(degree) + int(minute) / 60
    if direction in ["W", "S"]:
        in_decimal *= -1
    return in_decimal


def get_coordinates() -> list[tuple]:
    """
    Get list of coordinates from website.
    :return: list of (Location, Lat in decimal, Long in decimal).
    """

    link = "https://www.infoplease.com/world/geography/major-cities-latitude-longitude-and-corresponding-time-zones"
    path = "//*[@id ='A0001770']/tbody/tr"  # xpath to table in page

    response = requests.get(link)
    byte_string = response.content
    source_code = html.fromstring(byte_string)
    tree = source_code.xpath(path)
    table = [[thing.text_content() for thing in elem] for elem in tree[2:]]

    # formatting
    return [(elem[0].split(",")[0],
             to_decimal(elem[1] + "'" + elem[2]),
             to_decimal(elem[3] + "'" + elem[4])
             ) for elem in table]


def haversine(coordinate_1: tuple, coordinate_2: tuple) -> int:
    """
    Takes two coordinates in decimal format and calculate the distance between them.
    :param coordinate_1: Start location with lat and long in decimal format.
    :param coordinate_2: End location with lat and long in decimal format.
    :return: Distance between start and end in km.
    """

    if coordinate_1 == coordinate_2:
        return 0  # just to avoid unnecessary processing

    lat_1, long_1 = coordinate_1
    lat_2, long_2 = coordinate_2

    delta_lat = (abs(lat_1 - lat_2)) * math.pi / 180
    delta_long = (abs(long_1 - long_2)) * math.pi / 180

    lat_1, long_1, lat_2, long_2 = map(lambda x: x * math.pi / 180, (lat_1, long_1, lat_2, long_2))

    r = 6_371_000  # earths radius in metres

    a = math.pow(sin(delta_lat / 2), 2) + cos(lat_1) * cos(lat_2) * math.pow(sin(delta_long / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int((r * c) / 1_000)  # distance in km


def get_distances() -> defaultdict:
    """
    Part 3.2 of the assignment.
    Download coordinates and calculate distances between them.
    :return: Dict containing dicts containing distances. It's a distance matrix in dict form, if you will.
    """

    table = get_coordinates()  # get coordinated from website.
    distances = defaultdict(dict)

    for x in table:
        for y in table:
            distances[x[0]][y[0]] = haversine(x[1:], y[1:])  # convert coordinates to distances.
    return distances
