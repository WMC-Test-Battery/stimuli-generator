from PIL import Image, ImageDraw
from geometry import Vector, Point


class Canvas:
    def __init__(self, mode="RGBA", size=(1210, 1210), background=(255, 255, 255, 0), name="canvas"):
        self.name = name
        self.width = int(size[0])
        self.height = int(size[1])

        self.center = Point(self.width / 2, self.height / 2)

        # Create a new blank image
        self.image = Image.new(mode, size, background)

        # Create a drawing object
        self.draw = ImageDraw.Draw(self.image, mode=mode)

    def draw_arrow(self, start, end, color=(0, 0, 0, 255), line_thickness=1, tip_width=20, tip_length=20):
        """
        Draws an arrow from start to end.

        :param start: Point where the arrow starts
        :param end: Point where the arrow ends
        :param color: Color of the arrow
        :param line_thickness: Thickness of the arrow's line
        :param tip_width: Width of the base of the triangular tip
        :param tip_length: Distance from the base of the triangular tip to the end of the arrow
        :returns: None
        """

        start = Point(*start)
        tip = Point(*end)
        direction = (tip - start).normalize()
        line_end = tip - tip_length * direction

        left = direction.perpendicular_counterclockwise()
        right = direction.perpendicular_clockwise()

        left_corner = line_end + (tip_width / 2) * left
        right_corner = line_end + (tip_width / 2) * right

        self.draw.polygon([left_corner, tip, right_corner], fill=color, outline=None, width=0)
        self.draw.line([start, line_end], fill=color, width=line_thickness)

    def draw_radial_arrow(self, angle=0, length=None, color=(0, 0, 0, 255), line_thickness=None, tip_width=None,
                          tip_length=None):
        """
        Draws an arrow originating at the center of the image, pointing outwards with the given angle and length.

        :param angle: Angle of the arrow (counterclockwise, relative to a horizontal vector pointing to the right)
        :param length: Length of the arrow
        :param color: Color of the arrow
        :param line_thickness: Thickness of the arrow's line
        :param tip_width: Width of the base of the triangular tip
        :param tip_length: Distance from the base of the triangular tip to the top of the triangular tip
        :returns: None
        """

        # Calculate default values
        if not length:
            length = min(self.width, self.height) / 4
        if not line_thickness:
            line_thickness = max(1, max(self.width, self.height) // 100) * 2
        if not tip_width:
            tip_width = 6 * line_thickness
        if not tip_length:
            tip_length = tip_width*0.6

        # Calculate the endpoint of the arrow
        direction = Vector(1, 0).rotate(angle)
        end = self.center + length * direction

        self.draw_arrow(start=self.center, end=end, color=color, line_thickness=line_thickness,
                        tip_width=tip_width, tip_length=tip_length)

    def save(self, path="", extension="png"):
        """
        Saves the image using the name and the given filename extension.

        :param path: Path where the file should be saved
        :param extension: Filename extension.
        :returns: None
        """

        self.image.save(f"{path}{self.name}.{extension}")

    def show(self):
        """
        Shows the image.

        :returns: None
        """

        self.image.show()

    def draw_checker_pattern(self, color=(220, 220, 220, 255)):
        """
        Draws a checkerboard pattern over the image.
        """
        for x in range(self.width):
            for y in range(self.height):
                if x % 2 == 0 and y % 2 == 0:
                    self.draw.point((x, y), fill=color)
                elif x % 2 == 1 and y % 2 == 1:
                    self.draw.point((x, y), fill=color)

    def __repr__(self):
        return f"{self.name}({type(self)})"
