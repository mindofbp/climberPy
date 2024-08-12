import classes
import utils


def test_calculate_gradient_same_point():
    # Arrange
    point1 = classes.CoordinatePoint(0, 0, 0)
    point2 = classes.CoordinatePoint(0, 0, 0)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    # Assert
    assert result == 0


def test_calculate_gradient_downhill():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 48)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == -2 / dis * 100


def test_calculate_gradient_downhill_10_meter_drop():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 40)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == -10 / dis * 100


def test_calculate_gradient_downhill_20_meter_drop():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 30)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == -20 / dis * 100


def test_calculate_gradient_downhill_positive_to_negative_elevation():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 5)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, -2)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == -7 / dis * 100


def test_calculate_gradient_uphill():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 52)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == 2 / dis * 100


def test_calculate_gradient_uphill_10_meter_rise():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 60)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == 10 / dis * 100


def test_calculate_gradient_uphill_20_meter_rise():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 70)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == 20 / dis * 100


def test_calculate_gradient_uphill_negative_to_positive_elevation():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, -5)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 2)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    dis = 2.68186

    # Assert
    assert result == 7 / dis * 100


def test_calculate_gradient_same_elevation():
    # Arrange
    point1 = classes.CoordinatePoint(47.62436, -122.30113, 50)
    point2 = classes.CoordinatePoint(47.62438, -122.30111, 50)

    # Act
    result = utils.calculate_percent_gradient(point1, point2)

    # Assert
    assert result == 0


def test_calculate_avg_gradient():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 51),
        classes.CoordinatePoint(47.62438, -122.30111, 52),
        classes.CoordinatePoint(47.62440, -122.30109, 53),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = utils.calculate_distance(points[0], points[1]) + utils.calculate_distance(
        points[1], points[2]
    )

    # Assert
    assert result == 2 / dis * 100


def test_calculate_avg_gradient_same_elevation():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 50),
        classes.CoordinatePoint(47.62440, -122.30109, 50),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    # Assert
    assert result == 0


def test_calculate_avg_gradient_start_end_same_elevation():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 51),
        classes.CoordinatePoint(47.62440, -122.30109, 50),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    # Assert
    assert result == 0


def test_calculate_avg_gradient_uphill_downhill_net_positive():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 52),
        classes.CoordinatePoint(47.62440, -122.30109, 51),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = utils.calculate_distance(points[0], points[1]) + utils.calculate_distance(
        points[1], points[2]
    )

    # Assert
    assert result == 1 / dis * 100


def test_calculate_avg_gradient_uphill_downhill_net_negative():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 51),
        classes.CoordinatePoint(47.62440, -122.30109, 49),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = utils.calculate_distance(points[0], points[1]) + utils.calculate_distance(
        points[1], points[2]
    )

    # Assert
    assert result == -1 / dis * 100


def test_calculate_avg_gradient_downhill_uphill_net_positive():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 49),
        classes.CoordinatePoint(47.62440, -122.30109, 51),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = utils.calculate_distance(points[0], points[1]) + utils.calculate_distance(
        points[1], points[2]
    )

    # Assert
    assert result == 1 / dis * 100


def test_calculate_avg_gradient_downhill_uphill_net_negative():
    # Arrange
    points = [
        classes.CoordinatePoint(47.62436, -122.30113, 50),
        classes.CoordinatePoint(47.62438, -122.30111, 48),
        classes.CoordinatePoint(47.62440, -122.30109, 49),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = utils.calculate_distance(points[0], points[1]) + utils.calculate_distance(
        points[1], points[2]
    )

    # Assert
    assert result == -1 / dis * 100


def test_calculate_avg_gradient_s_curve():
    # Arrange
    points = [
        classes.CoordinatePoint(47.621669, -122.283650, 50),
        classes.CoordinatePoint(47.622127, -122.283865, 50),
        classes.CoordinatePoint(47.622124, -122.284112, 51),
        classes.CoordinatePoint(47.621755, -122.284254, 52),
        classes.CoordinatePoint(47.621594, -122.284504, 54),
        classes.CoordinatePoint(47.621668, -122.284673, 56),
        classes.CoordinatePoint(47.621863, -122.284439, 57),
        classes.CoordinatePoint(47.622109, -122.284297, 59),
    ]

    # Act
    result = utils.calculate_avg_gradient(points)

    dis = 212.5775

    # Assert
    assert result == 9 / dis * 100
