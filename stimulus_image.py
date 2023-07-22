from PIL import Image, ImageDraw
from geometry import Vector, Point, Coord
from math import ceil, floor


class StimulusImage:
    def __init__(self, mode="RGBA", size=(1210, 1210), background=(255, 255, 255, 0), name="blank_stimulus_image"):
        self._mode = mode
        self._width = int(size[0])
        self._height = int(size[1])
        self._size = (self._width, self._height)
        self._background = background
        self._name = name

        self._center_point = Point(self._width / 2, self._height / 2)

        self._tl = Coord(0, 0)
        self._tr = Coord(self._width - 1, 0)
        self._bl = Coord(0, self._height - 1)
        self._br = Coord(self._width - 1, self._height - 1)

        self._center_tl = Coord((self._width - 1) // 2, (self._height - 1) // 2)
        self._center_tr = Coord(self._width // 2, (self._height - 1) // 2)
        self._center_bl = Coord((self._width - 1) // 2, self._height // 2)
        self._center_br = Coord(self._width // 2, self._height // 2)

        # Create a new blank image
        self._image = Image.new(mode, size, background)

        # Create a drawing object
        self._draw = ImageDraw.Draw(self._image)

    def save(self, path="", extension="png"):
        """
        Saves the image using the name and the given filename extension.

        :param path: Path where the file should be saved
        :param extension: Filename extension.
        :returns: None
        """

        self._image.save(f"{path}{self._name}.{extension}")

    def show(self):
        """
        Shows the image.

        :returns: None
        """

        self._image.show()

    def debug_checker(self):
        fill = (220, 220, 220, 255)
        for x in range(self._width):
            for y in range(self._height):
                if x % 2 == 0 and y % 2 == 0:
                    self._draw.point((x, y), fill=fill)
                elif x % 2 == 1 and y % 2 == 1:
                    self._draw.point((x, y), fill=fill)

    def __repr__(self):
        return self._name
