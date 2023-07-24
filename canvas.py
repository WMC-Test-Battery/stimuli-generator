from PIL import Image, ImageDraw, ImageFont, ImageOps
from geometry import Vector, Point


class Canvas:
    def __init__(self, size=(1210, 1210), mode="RGBA", background_color=(255, 255, 255, 255), name="canvas"):
        self.width = int(size[0])
        self.height = int(size[1])
        self.size = (self.width, self.height)
        self.mode = mode
        self.background_color = background_color
        self.name = name

        self.center = Point(self.width / 2, self.height / 2)

        # Create a new blank image
        self.image = Image.new(mode, self.size, background_color)

        # Create a drawing object
        self.draw = ImageDraw.Draw(self.image, mode=mode)

    def draw_grid(self, rows=8, cols=8, color=(0, 0, 0, 255), line_thickness=None):
        # draw lines between the rows and columns
        if not line_thickness:
            line_thickness = max(1, max(self.width, self.height) // 400) * 2

        line_offset = Vector(line_thickness // 2, line_thickness // 2)

        # how many pixels high/wide the rows/columns are
        col_step = self.width / cols
        row_step = self.height / rows

        for row in range(rows + 1):
            y = row * row_step
            start = Point(0, y) - line_offset
            end = Point(self.width + line_thickness, y) - line_offset
            self.draw.line([start, end], fill=color, width=line_thickness)

        for col in range(cols + 1):
            x = col * col_step
            start = Point(x, 0) - line_offset
            end = Point(x, self.height + line_thickness) - line_offset
            self.draw.line([start, end], fill=color, width=line_thickness)

    def draw_arrow(self, start, end, color=(0, 0, 0, 255), line_thickness=None, tip_width=None, tip_length=None):
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

        # Calculate default values
        if not line_thickness:
            line_thickness = max(1, max(self.width, self.height) // 100) * 2
        if not tip_width:
            tip_width = 6 * line_thickness
        if not tip_length:
            tip_length = tip_width*0.6

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

        # Calculate the endpoint of the arrow
        direction = Vector(1, 0).rotate(angle)
        end = self.center + length * direction

        self.draw_arrow(start=self.center, end=end, color=color, line_thickness=line_thickness,
                        tip_width=tip_width, tip_length=tip_length)

    def draw_dot(self, center=None, radius=None, color=(0, 0, 0, 255)):
        if not center:
            center = self.center
        else:
            center = Point(*center)
        if not radius:
            radius = min(self.width, self.height) / 4

        top_left = center + radius*Vector.up() + radius*Vector.left()
        bottom_right = center + radius*Vector.down() + radius*Vector.right()

        self.draw.ellipse([top_left, bottom_right], fill=color, outline=None, width=0)

    def draw_square(self, position=None, side_length=None, color=(0, 0, 0, 255)):
        if not position:
            position = self.center
        else:
            position = Point(*position)
        if not side_length:
            side_length = min(self.width, self.height) / 4

        top_left = position + (side_length / 2) * Vector.up() + (side_length / 2) * Vector.left()
        bottom_right = position + (side_length / 2) * Vector.down() + (side_length / 2) * Vector.right()

        self.draw.rectangle([top_left, bottom_right], fill=color, width=0)

    def draw_letter(self, letter="A", location=None, color=(0, 0, 0, 255), mirror=False, angle=0, font=None, size=None):
        if not location:
            location = self.center
        if not size:
            size = min(self.width, self.height) // 3
        if not font:
            font = ImageFont.truetype("fonts/ARIAL.TTF", size)

        letter_image = Image.new(mode="RGBA", size=self.size, color=(255, 255, 255, 0))
        letter_draw = ImageDraw.Draw(letter_image)
        letter_draw.text(location, letter, fill=color, font=font, anchor="mm")

        if mirror:
            letter_image = ImageOps.mirror(letter_image)
        letter_image = letter_image.rotate(angle)

        self.image = Image.alpha_composite(self.image, letter_image)

    def save(self, path="", name_overwrite=None, extension="png"):
        """
        Saves the image using the name and the given filename extension.

        :param path: Path where the file should be saved
        :param extension: Filename extension.
        :param name_overwrite: Filename to use instead of the name of the canvas.
        :returns: None
        """

        if not name_overwrite:
            name = self.name
        else:
            name = name_overwrite

        self.image.save(f"{path}{name}.{extension}")

    def show(self):
        """
        Shows the image.

        :returns: None
        """

        self.image.show()

    def draw_checker_pattern(self, color=(100, 100, 100, 100)):
        """
        Draws a transparent checkerboard pattern over the image.
        """

        checker_image = Image.new(mode="RGBA", size=self.size, color=(255, 255, 255, 0))
        checker_draw = ImageDraw.Draw(checker_image)

        for x in range(self.width):
            for y in range(self.height):
                if x % 2 == 0 and y % 2 == 0:
                    checker_draw.point((x, y), fill=color)
                elif x % 2 == 1 and y % 2 == 1:
                    checker_draw.point((x, y), fill=color)

        self.image = Image.alpha_composite(self.image, checker_image)

    def __repr__(self):
        return f"{self.name}({type(self)})"
