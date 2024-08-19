import climberpy.utils as utils
import climberpy.classes as classes

from pytest import approx


def test_calculate_distance_same_point():
    # Arrange
    point1 = classes.CoordinatePoint(0, 0, 0)
    point2 = classes.CoordinatePoint(0, 0, 0)

    # Act
    result = utils.calculate_distance(point1, point2)

    # Assert
    assert result == 0


def test_calculate_distance():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 0)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 0)

    # Act
    result = utils.calculate_distance(point1, point2)

    # Assert
    assert result == 2.68186


def test_calculate_distance_s_curve():
    # Arrange
    points = [
        classes.CoordinatePoint(47.621669, -122.283650, 0),
        classes.CoordinatePoint(47.622127, -122.283865, 0),
        classes.CoordinatePoint(47.622124, -122.284112, 0),
        classes.CoordinatePoint(47.621755, -122.284254, 0),
        classes.CoordinatePoint(47.621594, -122.284504, 0),
        classes.CoordinatePoint(47.621668, -122.284673, 0),
        classes.CoordinatePoint(47.621863, -122.284439, 0),
        classes.CoordinatePoint(47.622109, -122.284297, 0),
    ]

    # Act
    result = 0
    for i in range(len(points) - 1):
        result += utils.calculate_distance(points[i], points[i + 1])

    # Assert
    assert result == approx(215, 10)
