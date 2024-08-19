from classes import *
import identifiers as identifiers
import os
import parsers as parsers
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]

    if input_file[-4:] != ".fit":
        raise ValueError("Invalid file type. Please provide a .fit")

    if os.path.isfile(input_file) == False:
        raise ValueError("File does not exist. Please provide a valid file")

    points = parsers.parse_fit_file(input_file)
    climbs = identifiers.ClimbIdentifier(points).identify_climbs()
    # TODO: make the plotting done as a call on each climb
    # Example:
    # for climb in climbs:
    #     climb.plot_segment()
    for index, segment in enumerate(climbs):
        if segment.distance >= 1000:
            # TODO: Move this logic into the plot_segment method

            # If distance is less than 2k then we wil plot in 400m segments
            # If the distance is between 2k and 5k then we will plot in 800m segments
            # If the distance is greater than 5k then we will plot in 1k segments
            if segment.distance < 5000:
                segment.plot_segment(500, index)
            else:
                segment.plot_segment(1000, index)
