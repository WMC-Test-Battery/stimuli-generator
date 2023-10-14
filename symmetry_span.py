import math

from geometry import Vector, Point
from canvas import Canvas
import numpy as np


class SymmetrySpan(Canvas):
    def __init__(self, size=(1210, 1210), mode="RGBA", background_color=(255, 255, 255, 255),
                 name="symmetry_span"):
        super(SymmetrySpan, self).__init__(size=size, mode=mode, background_color=background_color, name=name)

        self.squares = None
        self.rows = None
        self.cols = None

    def configure_squares(self, rows=8, cols=8, symmetric=True, noise=0.0):
        self.rows = rows
        self.cols = cols

        left_grid = np.random.binomial(1, 0.5, (self.rows, (self.cols + 1) // 2))

        if self.rows % 2 == 0:
            right_grid = np.fliplr(left_grid)
        else:
            right_grid = np.delete(np.fliplr(left_grid), 0, 1)

        if symmetric:
            self.squares = np.concatenate((left_grid, right_grid), axis=1)
        else:
            mask = np.random.rand(*right_grid.shape)
            rand = np.random.binomial(1, 0.5, right_grid.shape)
            noisy_right_grid = np.where(mask < noise, rand, right_grid)

            if np.array_equal(noisy_right_grid, right_grid):
                # to avoid accidental symmetric images, at least one square will be changed
                row = np.random.randint(0, right_grid.shape[0])
                col = np.random.randint(0, right_grid.shape[1])
                noisy_right_grid[row][col] = 1 - noisy_right_grid[row][col]

            self.squares = np.concatenate((left_grid, noisy_right_grid), axis=1)

    def draw_squares(self, color=(0, 0, 0, 255)):
        # how many pixels high/wide the rows/columns are
        col_step = self.width / self.cols
        row_step = self.height / self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                if self.squares[row][col] == 1:
                    position = Point((col * col_step) + (col_step / 2), (row * row_step) + (row_step / 2))
                    side_length = row_step
                    self.draw_square(position=position, side_length=side_length, color=color)

    def draw_grid(self, rows=None, cols=None, color=(0, 0, 0, 255), line_thickness=None):
        super(SymmetrySpan, self).draw_grid(rows=self.rows, cols=self.cols, color=color)

    @classmethod
    def create_batch(cls, n_symm=6, n_asymm=6, asym_noise=0.5, rows=8, cols=8, folder="symmetry_span/",
                     image_size=(1210, 1210), background_color=(255, 255, 255, 255), square_color=(0, 0, 0, 255),
                     line_color=(0, 0, 0, 255)):

        num_of_digits = len(str(n_symm + n_asymm - 1))
        for i in range(n_symm):
            name = f"symm{i:0>{num_of_digits}}"

            stimulus = cls(size=image_size, background_color=background_color, name=name)
            stimulus.configure_squares(rows=rows, cols=cols, symmetric=True)
            stimulus.draw_squares(color=square_color)
            stimulus.draw_grid(color=line_color)
            stimulus.save(path=folder)

        for i in range(n_asymm):
            name = f"asym{i:0>{num_of_digits}}"

            stimulus = cls(size=image_size, background_color=background_color, name=name)
            stimulus.configure_squares(rows=rows, cols=cols, symmetric=False, noise=asym_noise)
            stimulus.draw_squares(color=square_color)
            stimulus.draw_grid(color=line_color)
            stimulus.save(path=folder)
