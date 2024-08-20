A basic tool to create simple graphics of climbs from [FIT](https://developer.garmin.com/fit/overview/) files that works with Python3 (`>=3.8`)

Inspired by the graphics you see on [procyclingstats.com](https://www.procyclingstats.com/)

## Installation
climberPy is available on PyPI
```shell
$ pip install climberpy
```

It can also be installed from source
```shell
$ git clone git@github.com:mindofbp/climberpy.git
$ cd climberpy
$ pip install .
```

## Usage Example
Find and visualize climbs in a FIT file.
```python
import climberpy

points = climberpy.parsers.parse_fit(input_file)
climbs = climberpy.identifiers.ClimbIdentifier(points).identify()

for climb in climbs:
    climb.plot()
```

The resulting PNG file(s) will be in the directory the method is called from

## Command Line Utilities
ClimberPy can be called from the command line to generate the PNG files

```shell
$ climberpy path/to/activity.fit
```

## Overview
This is a simple library to parse FIT file activities for subsegments matching certain characteristics. Currently this is exclusive to climbs.

The library was designed with cycling in mind and the default parameters were decided as such. But this is not exclusive and will work with any FIT file activity.

#### What is a climb?
As is default, a climb is any subsegment that meets the following:
1) An average gradient is greater than or equal to `3.5%`
2) Does not have a subsegment of itself which is between `0%` and `3.5%` gradient for more than `800 meters`
3) Does not have a subsegment of itself which is less than `0%` gradient for more than `200 meters`

These values are customizable by design.

## Ambitions
- Add category ratings to climbs
- Make climbs identifiable by real world names
- Expand the metadata of a segment to include at least GPX information about the start and end of a segment
- Expand CLI
- Add features for other sports (running, skiing)

Any and all feedback, suggestions, critiques, and criticism is welcomed.

## License
This project is distributed under the terms of the MIT license. See the [LICENSE](/LICENSE) file for more details.

## Credits
This project uses [fitdecode](https://github.com/polyvertex/fitdecode) to handle the parsing of the FIT files and [Pycairo](https://github.com/pygobject/pycairo) to generate the graphics.
