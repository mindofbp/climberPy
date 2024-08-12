from classes import ClimbSegment, CoordinatePoint
import utils

from typing import List


class ClimbIdentifierSettings:
    def __init__(
        self,
        gradient_threshold: float,
        allowed_distance_below_climb_threshold: float,
        allowed_distance_downhill: float,
    ):
        self.gradient_threshold = self._verify_gradient_threshold(gradient_threshold)
        self.allowed_distance_below_climb_threshold = (
            self._verify_allowed_distance_below_climb_threshold(
                allowed_distance_below_climb_threshold
            )
        )
        self.allowed_distance_downhill = self._verify_allowed_distance_downhill(
            allowed_distance_downhill
        )

    @staticmethod
    def _verify_gradient_threshold(gradient_threshold: float) -> float:
        if gradient_threshold < 0 or gradient_threshold > 100:
            raise ValueError("Invalid gradient threshold")
        return gradient_threshold

    @staticmethod
    def _verify_allowed_distance_below_climb_threshold(
        allowed_distance_below_climb_threshold: float,
    ) -> float:
        if allowed_distance_below_climb_threshold < 0:
            raise ValueError("Invalid allowed distance below climb threshold")
        return allowed_distance_below_climb_threshold

    @staticmethod
    def _verify_allowed_distance_downhill(allowed_distance_downhill: float) -> float:
        if allowed_distance_downhill < 0:
            raise ValueError("Invalid allowed distance downhill")
        return allowed_distance_downhill


class Identifier:
    def __init__(self, cordPoints: List[CoordinatePoint]):
        self.cordPoints: List[CoordinatePoint] = cordPoints


class ClimbIdentifier(Identifier):
    def __init__(
        self,
        cordPoints: List[CoordinatePoint],
        gradient_threshold: float = 3.5,
        allowed_distance_below_climb_threshold: float = 800,
        allowed_distance_downhill: float = 200,
    ):
        super().__init__(cordPoints)
        self.identifier_settings = ClimbIdentifierSettings(
            gradient_threshold,
            allowed_distance_below_climb_threshold,
            allowed_distance_downhill,
        )

    def _point_gradient_below_threshold(
        self, point1: CoordinatePoint, point2: CoordinatePoint
    ) -> bool:
        """Check if the gradient between two points is above the threshold"""
        return (
            utils.calculate_percent_gradient(point1, point2)
            < self.identifier_settings.gradient_threshold
        )

    def _seg_avg_gradient_above_threshold(self, segment: List[CoordinatePoint]) -> bool:
        """Check if the average gradient of a segment is above the threshold"""
        return (
            utils.calculate_avg_gradient(segment)
            >= self.identifier_settings.gradient_threshold
        )

    def _find_climb_start_index(self) -> int:
        """Find the index of the first point in a climb segment"""
        for i in range(len(self.cordPoints) - 1):
            if self._point_gradient_above_threshold(
                self.cordPoints[i], self.cordPoints[i + 1]
            ):
                return i
        return -1

    def _find_climb_peak_index(self, climb: List[CoordinatePoint]) -> int:
        return max(enumerate(climb), key=lambda x: x[1].elevation)[0]

    def _trim_climb_to_peak(
        self, climb: List[CoordinatePoint]
    ) -> List[CoordinatePoint]:
        return climb[: self._find_climb_peak_index(climb) + 1]

    def identify_climbs(self) -> List[ClimbSegment]:
        """Identify climb segments in the list of coordinate points"""
        climbs: List[ClimbSegment] = []
        current_climb: List[CoordinatePoint] = []
        distance_below_climb_threshold: float = 0.0
        distance_downhill: float = 0.0

        ptr1: int = 0
        ptr2: int = 1

        while ptr1 < len(self.cordPoints) - 1:
            if not self._point_gradient_below_threshold(
                self.cordPoints[ptr1], self.cordPoints[ptr2]
            ):
                current_climb.append(self.cordPoints[ptr1])
                current_climb.append(self.cordPoints[ptr2])
                # TODO: breakup req into smaller functions
                # one for checking total distance below threshold
                # one for checking total distance downhill
                while ptr2 < len(
                    self.cordPoints
                ) and self._seg_avg_gradient_above_threshold(current_climb):
                    if self._point_gradient_below_threshold(
                        self.cordPoints[ptr2 - 1], self.cordPoints[ptr2]
                    ):
                        distance_below_climb_threshold += utils.calculate_distance(
                            self.cordPoints[ptr2 - 1], self.cordPoints[ptr2]
                        )
                        if (
                            distance_below_climb_threshold
                            >= self.identifier_settings.allowed_distance_below_climb_threshold
                        ):
                            current_climb.append(self.cordPoints[ptr2])
                            break
                    else:
                        distance_below_climb_threshold = 0
                    if (
                        utils.calculate_percent_gradient(
                            self.cordPoints[ptr2 - 1], self.cordPoints[ptr2]
                        )
                        < 0
                    ):
                        distance_downhill += utils.calculate_distance(
                            self.cordPoints[ptr2 - 1], self.cordPoints[ptr2]
                        )
                        if (
                            distance_downhill
                            >= self.identifier_settings.allowed_distance_downhill
                        ):
                            current_climb.append(self.cordPoints[ptr2])
                            break
                    else:
                        distance_downhill = 0
                    current_climb.append(self.cordPoints[ptr2])
                    ptr2 += 1
                current_climb = self._trim_climb_to_peak(current_climb)
                climbs.append(ClimbSegment(current_climb))
                current_climb = []
                ptr1 = ptr2
                ptr2 += 1
            ptr1 += 1
            ptr2 += 1

        return climbs
