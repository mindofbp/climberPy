from classes import *
import identifiers
import os
import parsers
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]

    if input_file[-4:] != ".fit":
        raise ValueError("Invalid file type. Please provide a .fit")

    if os.path.isfile(input_file) == False:
        raise ValueError("File does not exist. Please provide a valid file")

    points = parsers.parse_fit_file(input_file)
    climbs = identifiers.ClimbIdentifier(points).identify_climbs()
    for index, segment in enumerate(climbs):
        if segment.distance >= 1000:
            # If distance is less than 2k then we wil plot in 400m segments
            # If the distance is between 2k and 5k then we will plot in 800m segments
            # If the distance is greater than 5k then we will plot in 1k segments
            if segment.distance < 5000:
                segment.plot_segment(500, index)
            else:
                segment.plot_segment(1000, index)
