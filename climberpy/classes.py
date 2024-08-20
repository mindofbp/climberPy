import math
import os
from typing import List, Optional
from uuid import uuid4

import utils as utils
import cairo
import cairosvg


class CoordinatePoint:
    def __init__(self, lat, long, elevation):
        self.lat = lat
        self.long = long
        self.elevation = elevation

    def __str__(self):
        return f"({self.lat}, {self.long}, {self.elevation})"


class Segment:
    def __init__(self, cordPoints: List[CoordinatePoint]):
        self.cordPoints: list[CoordinatePoint] = cordPoints
        self.distance: float = self.__calculate_segment_distance()

    def __calculate_segment_distance(self):
        distance = 0.0
        for i in range(len(self.cordPoints) - 1):
            distance += utils.calculate_distance(
                self.cordPoints[i], self.cordPoints[i + 1]
            )
        return distance


class ClimbSegmentPlotSettings:
    def __init__(self):
        self._font_size = 12
        self._text_line_width = 1
        self._font_color = [0, 0, 0]
        self._dash_sequence = [5.0]
        self._line_width = 2
        self._plot_width = 440
        self._plot_height = 400

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value

    @property
    def text_line_width(self):
        return self._text_line_width

    @text_line_width.setter
    def text_line_width(self, value):
        self._text_line_width = value

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, value):
        self._font_color = value

    @property
    def dash_sequence(self):
        return self._dash_sequence

    @dash_sequence.setter
    def dash_sequence(self, value):
        self._dash_sequence = value

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value


class ClimbSegment(Segment):
    def __init__(self, cordPoints: List[CoordinatePoint]):
        super().__init__(cordPoints)
        self.avgGradient: float = self.__calculate_segment_gradient()
        self.maxGradient: float = self.__calculate_max_gradient()
        self.category: int = self.__calculate_category()
        self.difficulty: float = self.__calculate_difficulty()
        self.gain: float = self.__calculate_gain()

    def __calculate_segment_gradient(self) -> float:
        """Calculate the average gradient of the climb segment"""
        if self.distance == 0:
            return 0

        return (
            (self.cordPoints[-1].elevation - self.cordPoints[0].elevation)
            / self.distance
            * 100
        )

    def __calculate_max_gradient(self) -> float:
        """Calculate the maximum gradient of the climb segment"""
        maxGradient = 0.0
        for i in range(len(self.cordPoints) - 1):
            gradient = utils.calculate_percent_gradient(
                self.cordPoints[i], self.cordPoints[i + 1]
            )
            if (
                gradient > maxGradient
                and utils.verify_gradient(gradient)
                and utils.verify_gradient_delta(
                    gradient,
                    utils.calculate_percent_gradient(
                        self.cordPoints[i - 1], self.cordPoints[i]
                    ),
                )
            ):
                maxGradient = gradient

        return maxGradient

    def __calculate_category(self):
        pass

    def __calculate_difficulty(self):
        pass

    def __calculate_gain(self):
        return self.cordPoints[-1].elevation - self.cordPoints[0].elevation

    def __grad_color(self, gradient: float) -> List[float]:
        """Match the gradient to a color for visualization"""
        if gradient <= 4:
            return [88.0, 201.0, 25.0]
        elif gradient <= 6:
            return [3.0, 90.0, 144.0]
        elif gradient <= 9:
            return [230.0, 16.0, 40.0]
        else:
            return [6.0, 6.0, 8.0]

    def __sub_segment_length(self) -> int:
        if self.distance < 5000:
            return 500

        return 1000

    def __build_sub_segments(self, segment_length: int = 400):
        """Partition segment into smaller segments of equal length"""
        sub_segments = []
        current_sub_segment_length = 0
        current_sub_segment = []

        # Begin build sub segments
        for i in range(len(self.cordPoints) - 1):
            distance = utils.calculate_distance(
                self.cordPoints[i], self.cordPoints[i + 1]
            )
            if current_sub_segment_length + distance < segment_length:
                current_sub_segment.append(self.cordPoints[i])
                current_sub_segment_length += distance
            else:
                current_sub_segment.append(self.cordPoints[i])
                current_sub_segment.append(self.cordPoints[i + 1])
                sub_segments.append(current_sub_segment)
                current_sub_segment = []
                current_sub_segment_length = 0

        if current_sub_segment:
            sub_segments.append(current_sub_segment)
        # End build sub segments

        return sub_segments

    def plot(
        self,
        minimum_distance: Optional[int] = 1000,
        sub_segment_length: Optional[int] = None,
        climb_index: Optional[int] = None,
        settings: ClimbSegmentPlotSettings = ClimbSegmentPlotSettings(),
    ) -> str:
        """Visualize the climb segment in a PNG file"""
        if self.distance < minimum_distance:
            return

        # Split the segment into smaller segments of sub_segment_length, calculate the
        # percentage gradient of each segment and plot it
        climb_index = climb_index if climb_index is not None else uuid4()
        sub_segment_length = sub_segment_length if sub_segment_length else self.__sub_segment_length()
        with cairo.SVGSurface(f"climb_{climb_index}.svg", settings._plot_width, settings._plot_height) as surface:
            context = cairo.Context(surface)
            sub_segments = self.__build_sub_segments(sub_segment_length)

            # Paint the background white
            context.save()
            context.set_source_rgb(1, 1, 1)
            context.paint()
            context.restore()

            # Begin write segment metadata
            context.set_line_width(settings.text_line_width)
            context.set_font_size(settings.font_size)
            context.move_to(2, 10)
            context.text_path(f"{round(self.gain, 1)}m")
            context.move_to(2, 25)
            context.text_path(
                f"{round(self.distance / 1000, 1)}km at {round(self.avgGradient, 1)}%"
            )
            context.stroke()
            # End write segment metadata

            # Begin plot sub segments
            context.move_to(0, settings._plot_height)
            previous_x = 20
            previous_y = settings._plot_height - 25

            # Shade in the area at the base/start of the plot
            context.set_source_rgb(0.5, 0.5, 0.5)
            context.move_to(20, settings._plot_height - 10)
            context.line_to(20, settings._plot_height - 25)
            context.line_to(
                20 - 7.5 * math.sqrt(3),
                settings._plot_height - 25 - 7.5,
            )
            context.line_to(
                20 - 7.5 * math.sqrt(3),
                settings._plot_height - 10 - 7.5,
            )
            context.line_to(20, settings._plot_height - 10)
            context.fill()
            context.set_source_rgb(*settings.font_color)

            # Draw the dashed vertical lines to start the plot
            context.move_to(previous_x, settings._plot_height - 10)
            context.set_dash(settings.dash_sequence)
            context.line_to(previous_x, previous_y)
            context.stroke()
            context.set_dash([])

            context.move_to(previous_x - 7.5 * math.sqrt(3), settings._plot_height - 10 - 7.5)
            context.set_dash(settings.dash_sequence)
            context.line_to(previous_x - 7.5 * math.sqrt(3), previous_y - 7.5)
            context.stroke()
            context.set_dash([])

            for index, sub_segment in enumerate(sub_segments):
                distance = 0
                total_gradient = 0
                for i in range(len(sub_segment) - 1):
                    distance += utils.calculate_distance(
                        sub_segment[i], sub_segment[i + 1]
                    )
                    total_gradient += utils.calculate_percent_gradient(
                        sub_segment[i], sub_segment[i + 1]
                    )

                sub_segment_avg_gradient = (
                    (sub_segment[-1].elevation - sub_segment[0].elevation)
                    / distance
                    * 100
                )

                rescaled_distance = utils.rescale(distance, self.distance, settings._plot_height)
                rescaled_rise = utils.find_rise(
                    rescaled_distance,
                    sub_segment_avg_gradient,
                ) * 10

                # Draw the colored gradient road
                context.move_to(previous_x, previous_y)
                color = self.__grad_color(sub_segment_avg_gradient)
                context.set_line_width(settings.line_width)
                context.set_source_rgb(color[0] / 255, color[1] / 255, color[2] / 255)
                context.line_to(
                    previous_x + rescaled_distance, previous_y - rescaled_rise
                )
                context.line_to(
                    previous_x + rescaled_distance - 7.5 * math.sqrt(3),
                    previous_y - rescaled_rise - 7.5,
                )
                context.line_to(
                    previous_x - 7.5 * math.sqrt(3),
                    previous_y - 7.5,
                )
                context.line_to(
                    previous_x,
                    previous_y,
                )
                context.fill()
                context.stroke()

                # Draw the lines around the gradient road
                context.move_to(previous_x, previous_y)
                context.set_line_width(settings.line_width)
                context.set_source_rgb(*settings.font_color)
                context.line_to(
                    previous_x + rescaled_distance, previous_y - rescaled_rise
                )
                context.line_to(
                    previous_x + rescaled_distance - 7.5 * math.sqrt(3),
                    previous_y - rescaled_rise - 7.5,
                )
                context.line_to(
                    previous_x - 7.5 * math.sqrt(3),
                    previous_y - 7.5,
                )
                context.line_to(
                    previous_x,
                    previous_y,
                )
                context.stroke()

                # Draw the dashed line up the middle of the gradient road
                context.move_to(
                    previous_x - 7.5 * math.sqrt(3) / 2,
                    previous_y - (7.5 / 2),
                )
                context.set_dash(settings.dash_sequence)
                context.line_to(
                    previous_x + rescaled_distance - (7.5 * math.sqrt(3) / 2),
                    previous_y - rescaled_rise - (7.5 / 2),
                )
                context.stroke()
                context.set_dash([])

                # Draw the gradient percentage text if segment is longer than 250m
                if distance > 100:
                    context.set_source_rgb(*settings.font_color)
                    context.move_to(
                        previous_x + rescaled_distance - 35, previous_y - rescaled_rise - 15
                    )
                    context.set_line_width(settings.text_line_width)
                    context.set_font_size(settings.font_size)
                    context.text_path(
                        str(
                            round(
                                sub_segment_avg_gradient,
                                1,
                            )
                        )
                        + "%"
                    )
                    context.stroke()

                # Draw the sub segment distance text
                if index != len(sub_segments) - 1:
                    context.move_to(previous_x + rescaled_distance - 4, settings._plot_height - ((30 / settings._plot_height) * (previous_x + rescaled_distance) - 4))
                    accum_distance = ((index + 1) * sub_segment_length) / 1000
                    if int(accum_distance) != accum_distance:
                        context.text_path(str(accum_distance))
                    else:
                        context.text_path(str(int(accum_distance)))
                    context.stroke()

                # Shade in the area under the gradient road
                context.move_to(previous_x, previous_y)
                context.set_source_rgb(0.9, 0.9, 0.9)
                context.line_to(
                    previous_x + rescaled_distance, previous_y - rescaled_rise
                )
                context.line_to(
                    previous_x + rescaled_distance, settings._plot_height - ((30 / settings._plot_height) * (previous_x + rescaled_distance) + 10)
                )
                context.line_to(
                    previous_x, settings._plot_height - ((30 / settings._plot_height) * (previous_x) + 10)
                )
                context.fill()

                # Draw the dashed vertical line
                context.set_source_rgb(*settings.font_color)
                context.move_to(previous_x + rescaled_distance, settings._plot_height - ((30 / settings._plot_height) * (previous_x + rescaled_distance) + 10))
                context.set_dash(settings.dash_sequence)
                context.line_to(
                    previous_x + rescaled_distance, previous_y - rescaled_rise
                )
                context.stroke()
                context.set_dash([])

                previous_x += rescaled_distance
                previous_y -= rescaled_rise
            # End plot sub segments

            # Draw the solid lines on the bottom of the plot
            context.move_to(20, settings._plot_height - 10)
            context.set_line_width(settings.line_width)
            context.set_source_rgb(*settings.font_color)
            context.line_to(settings._plot_width - 20, settings._plot_height - 40)

            context.move_to(20, settings._plot_height - 10)
            context.line_to(20 - 7.5 * math.sqrt(3), settings._plot_height - 10 - 7.5)

            context.stroke()

        cairosvg.svg2png(
            url=f"climb_{climb_index}.svg", write_to=f"climb_{climb_index}.png"
        )

        os.remove(f"climb_{climb_index}.svg")

        return f"climb_{climb_index}.png"
