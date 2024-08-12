import classes

import xml.etree.ElementTree as ET
import fitdecode


def parse_gpx_file(filename: str) -> list:
    """Parse a GPX file and return a list of CoordinatePoints"""
    tree = ET.parse(filename)
    root = tree.getroot()
    points = []
    for element in root:
        if element.tag.endswith("trk"):
            for child in element:
                if child.tag.endswith("trkseg"):
                    for trkpt in child:
                        for trkpt_child in trkpt:
                            if trkpt_child.tag.endswith("ele"):
                                elevation = float(trkpt_child.text)
                        lat = float(trkpt.attrib["lat"])
                        long = float(trkpt.attrib["lon"])
                        points.append(classes.CoordinatePoint(lat, long, elevation))

    return points


def parse_fit_file(filename: str):
    with fitdecode.FitReader(filename) as fit:
        points = []
        lat = None
        long = None
        elevation = None
        try:
            for frame in fit:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    # Here, frame is a FitDataMessage object.
                    # A FitDataMessage object contains decoded values that
                    # are directly usable in your script logic.
                    print(frame.name)
                    for field in frame.fields:
                        lat = (
                            float(field.value) * (180 / 2**31)
                            if field.name == "position_lat"
                            else lat
                        )
                        long = (
                            float(field.value) * (180 / 2**31)
                            if field.name == "position_long"
                            else long
                        )
                        elevation = (
                            float(field.value)
                            if field.name == "altitude"
                            else elevation
                        )
                        if lat and long and elevation:
                            points.append(classes.CoordinatePoint(lat, long, elevation))
                            lat = None
                            long = None
                            elevation = None
                        print(f" - {field.name}: {field.value} {field.units}")

        except Exception as e:
            print(e)

        return points
