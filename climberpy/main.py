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

    for climb in climbs:
        climb.plot_segment()
