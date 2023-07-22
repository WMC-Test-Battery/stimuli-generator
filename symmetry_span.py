from PIL import Image, ImageDraw
from geometry import Vector, Point, Coord
from stimulus_image import StimulusImage
import numpy as np
import math


class SymmetrySpanStimulus(StimulusImage):
    def __init__(self, rows=8, cols=8, mode="RGBA", min_size=(1210, 1210), background=(255, 255, 255, 0),
                 name="symmetry_span_stimulus"):

        if isinstance(rows, int) and isinstance(cols, int):
            self.cols = cols
            self.rows = rows
        else:
            raise TypeError("Number of rows and columns should be integers")

        # how many pixels high/wide the rows/columns are
        col_step = math.ceil(min_size[0] / self.cols)
        row_step = math.ceil(min_size[1] / self.rows)

        self.step = max(col_step, row_step)

        width = cols * self.step
        height = rows * self.step

        # if not (width == min_size[0] and height == min_size[1]):
        #     print(f"WARNING: Image size has been changed to {(width, height)}!")

        size = (width, height)

        super(SymmetrySpanStimulus, self).__init__(mode, size, background, name)

        self.grid = None

    def configure_grid(self, symmetric=True, noise=0.0, debug=False):
        if debug:
            left_grid = np.zeros((self.rows, (self.cols + 1) // 2))
        else:
            left_grid = np.random.binomial(1, 0.5, (self.rows, (self.cols + 1) // 2))

        if self.rows % 2 == 0:
            right_grid = np.fliplr(left_grid)
        else:
            right_grid = np.delete(np.fliplr(left_grid), 0, 1)

        if symmetric:
            self.grid = np.concatenate((left_grid, right_grid), axis=1)
        else:
            mask = np.random.rand(*right_grid.shape)
            rand = np.random.binomial(1, 0.5, right_grid.shape)
            noisy_right_grid = np.where(mask < noise, rand, right_grid)

            if np.array_equal(noisy_right_grid, right_grid):
                # to avoid accidental symmetric images, at least one square will be changed
                row = np.random.randint(0, right_grid.shape[0])
                col = np.random.randint(0, right_grid.shape[1])
                noisy_right_grid[row][col] = 1 - noisy_right_grid[row][col]

            self.grid = np.concatenate((left_grid, noisy_right_grid), axis=1)

    def draw_grid(self, color=(0, 0, 0, 255), line_thickness=None):
        if self.grid is not None:
            # draw black squares
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] == 1:
                        top_left = Coord(col * self.step, row * self.step)
                        bottom_right = Coord((col + 1) * self.step - 1, (row + 1) * self.step - 1)
                        self._draw.rectangle([top_left, bottom_right], fill=color, width=0)

        # draw lines between the rows and columns
        if not line_thickness:
            line_thickness = max(1, max(self._width, self._height) // 400) * 2

        line_offset = Vector(line_thickness // 2, line_thickness // 2)

        for row in range(self.rows + 1):
            y = row * self.step
            start = Coord(0, y) - line_offset
            end = Coord(self._width + line_thickness, y) - line_offset
            self._draw.line([start, end], fill=color, width=line_thickness)

        for col in range(self.cols + 1):
            x = col * self.step
            start = Coord(x, 0) - line_offset
            end = Coord(x, self._height + line_thickness) - line_offset
            self._draw.line([start, end], fill=color, width=line_thickness)
