import math


class Unit:
    def __init__(self, measure_unit: str):
        self.measure_unit = self.__verify_unit(measure_unit)

    def __verify_unit(self, measure_unit: str):
        if measure_unit not in ["m", "km", "mi", "ft"]:
            raise ValueError("Invalid unit")
        return measure_unit

    @property
    def conversion_factor_from_km(self):
        if self.measure_unit == "m":
            return 1000
        elif self.measure_unit == "km":
            return 1
        elif self.measure_unit == "mi":
            return 0.621371
        elif self.measure_unit == "ft":
            return 3280.84


def calculate_distance(
    point1, point2, unit: Unit = Unit("m"), accuracy: int = 5
) -> float:
    """
    Calculate distance between two points using the haversine formula and converting
    to given units
    """
    distance = haversine(point1.lat, point1.long, point2.lat, point2.long)

    return round(distance * unit.conversion_factor_from_km, accuracy)


def calculate_percent_gradient(point1, point2) -> float:
    """Calculate the percent gradient between two points"""
    if point1.elevation == point2.elevation:
        return 0
    return (
        (point2.elevation - point1.elevation) / calculate_distance(point1, point2) * 100
    )


def calculate_avg_gradient(points) -> float:
    """Calculate the average percent gradient of a segment"""
    total_distance = 0
    for i in range(len(points) - 1):
        total_distance += calculate_distance(points[i], points[i + 1])

    return (points[-1].elevation - points[0].elevation) / total_distance * 100


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points using the haversine formula"""
    EARTH_RADIUS = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    dis = (
        math.sin(d_lat * 0.5) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon * 0.5) ** 2
    )

    return 2 * EARTH_RADIUS * math.asin(math.sqrt(dis))


def verify_gradient_delta(gradient1: float, gradient2: float) -> bool:
    # TODO: make this better, it does not work well for small gradients
    # where a jump from 4% to 18% is feasible
    """Verify that the change in gradient between two points is feasible"""
    PERCENT_DIFFERENCE_THRESHOLD = 45  # Roads can ramp up quickly

    if gradient1 == 0:
        gradient1 = 0.001
    if gradient2 == 0:
        gradient2 = 0.001

    return (
        abs(gradient1 - gradient2) / gradient1
    ) * 100 <= PERCENT_DIFFERENCE_THRESHOLD


def verify_gradient(gradient: float) -> bool:
    """Verify that the gradient is feasible"""
    GRADIENT_THRESHOLD = 45  # Roads can't be too steep

    return abs(gradient) <= GRADIENT_THRESHOLD


def rescale(value: float, old_max: float, new_max: float) -> float:
    """Rescale a value from an old range to a new range"""
    return (value / old_max) * new_max


def find_rise(run: float, gradient: float) -> float:
    """Find the rise of a segment given the run and gradient"""
    return run * (gradient / 100)
