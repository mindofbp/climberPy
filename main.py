from classes import *
import identifiers
import parsers

if __name__ == "__main__":
    # points = parsers.parse_gpx_file(
    #     "Triple_Zoo_Hill_Climb_-_Return_Mercer_Island_metric.gpx"
    # )
    points = parsers.parse_fit_file("upper_lake_loop.fit")
    climbs = identifiers.ClimbIdentifier(points).identify_climbs()
    for index, segment in enumerate(climbs):
        if segment.distance >= 1000:
            # If distance is less than 2k then we wil plot in 400m segments
            # If the distance is betwen 2k and 5k then we will plot in 800m segments
            # If the distance is greater than 5k then we will plot in 1k segments
            if segment.distance < 2000:
                segment.plot_segment(400, index)
            elif segment.distance < 5000:
                segment.plot_segment(800, index)
            else:
                segment.plot_segment(1000, index)
