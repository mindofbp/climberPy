from climberpy.classes import *
import climberpy.identifiers as identifiers
import os
import climberpy.parsers as parsers
import sys

import click

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

@click.command()
@click.argument("input_file")
def cli(input_file):
    input_file = sys.argv[1]

    if input_file[-4:] != ".fit":
        raise ValueError("Invalid file type. Please provide a .fit")

    if os.path.isfile(input_file) == False:
        raise ValueError("File does not exist. Please provide a valid file")

    points = parsers.parse_fit(input_file)
    climbs = identifiers.ClimbIdentifier(points).identify()

    for climb in climbs:
        climb.plot()
