A basic tool to create simple graphics of climbs from [FIT](https://developer.garmin.com/fit/overview/) files.


## Usage Example
Find and visualize climbs in a FIT file.
```python
import climberpy

points = climberpy.parsers.parse_fit_file(input_file)
climbs = climberpy.identifiers.ClimbIdentifier(points).identify_climbs()

for climb in climbs:
    climb.plot_segment()
```

The resulting PNG file(s) will be in the directory the method is called from

## Command Line Utilities
ClimberPy can be called from the command line to generate the PNG files

```shell
$ python main.py exampleActivity.fit
```

## Installation
climberPy is available on PyPI
```shell
$ pip install climberpy
```

It can also be installed from source
```shell
$ git clone git@github.com:mindofbp/climberpy.git
$ cd climberpy
```

## License
This project is distributed under the terms of the MIT license. See the [LICENSE](/LICENSE) file for more details.

## Credits
This project uses [fitdecode](https://github.com/polyvertex/fitdecode) to handle the parsing of the FIT files and [Pycairo](https://github.com/pygobject/pycairo) to generate the graphics.
