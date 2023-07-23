from canvas import Canvas
import numpy as np

from geometry import Point


class DotSpan(Canvas):
    def __init__(self, size=(1210, 1210), mode="RGBA", background_color=(255, 255, 255, 255), name="arrow_span"):
        super(DotSpan, self).__init__(mode, size, background_color, name)

        self.dots = None
        self.rows = None
        self.cols = None

    def configure_dots(self, rows=10, cols=10, n=6, subgrid=None, exclude_corners=True):
        self.rows = rows
        self.cols = cols
        self.dots = np.zeros((rows, cols))

        if not subgrid:
            subgrid = (rows, cols)
            start = (0, 0)
        elif subgrid[0] <= rows and subgrid[1] <= cols:
            max_row_idx = rows - subgrid[0] + 1
            max_col_idx = cols - subgrid[1] + 1
            start = (np.random.randint(0, max_col_idx), np.random.randint(0, max_row_idx))
        else:
            raise ValueError("Subgrid is too big!")

        if exclude_corners:
            exclude = [(0, 0), (rows - 1, 0), (0, cols - 1), (rows - 1, cols - 1)]
        else:
            exclude = None

        coords = self.generate_random_coords(n=n, rows=subgrid[0], cols=subgrid[1], start=start, exclude=exclude)

        for coord in coords:
            self.dots[coord[0]][coord[1]] = 1

    @staticmethod
    def generate_random_coords(n, rows, cols, start=(0, 0), exclude=None):
        coords = []

        if not exclude:
            exclude = []

        row_low = start[0]
        row_high = start[0] + cols
        col_low = start[1]
        col_high = start[1] + rows

        max_iter = (rows * cols) * 100
        for i in range(n):
            row, col = np.random.randint(row_low, row_high), np.random.randint(col_low, col_high)
            i = 0
            while (row, col) in coords or (row, col) in exclude:
                i += 1
                if i > max_iter:
                    raise StopIteration("Maximum number of iterations exceeded.")
                row, col = np.random.randint(row_low, row_high), np.random.randint(col_low, col_high)

            coords.append((row, col))

        return coords

    def draw_dots(self, color=(0, 0, 0, 255)):
        # how many pixels high/wide the rows/columns are
        col_step = self.width / self.cols
        row_step = self.height / self.rows

        for row in range(self.rows):
            for col in range(self.cols):
                if self.dots[row][col] == 1:
                    center = Point((col * col_step) + (col_step / 2), (row * row_step) + (row_step / 2))
                    radius = row_step / 2
                    self.draw_dot(center=center, radius=radius, color=color)

    def draw_dots_one_by_one(self, color=(0, 0, 0, 255), line_color=None, path="", name=None, keep_dots=False):
        if not name:
            name = self.name

        # how many pixels high/wide the rows/columns are
        col_step = self.width / self.cols
        row_step = self.height / self.rows

        if not line_color:
            line_color = color
        self.draw_grid(color=line_color)

        i = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.dots[row][col] == 1:
                    center = Point((col * col_step) + (col_step / 2), (row * row_step) + (row_step / 2))
                    radius = row_step / 2
                    self.draw_dot(center=center, radius=radius, color=color)
                    self.save(path=path, name_overwrite=f"{name}_dot{i}")
                    if not keep_dots:
                        self.draw_square(position=center, side_length=radius*2, color=self.background_color)
                        self.draw_grid(color=line_color)
                    i += 1

    def draw_grid(self, rows=None, cols=None, color=(0, 0, 0, 255), line_thickness=None):
        super(DotSpan, self).draw_grid(rows=self.rows, cols=self.cols, color=color)

    @classmethod
    def create_batch(cls, batch_size=30, set_sizes=(2, 3, 4, 5, 6), rows=10, cols=10, subgrid=(5, 5),
                     folder="dot_span/", image_size=(1210, 1210),
                     background_color=(255, 255, 255, 255), dot_color=(0, 0, 0, 255), line_color=(0, 0, 0, 255)):
        for i in range(batch_size):
            use_subgrid = np.random.randint(0, 2)
            if use_subgrid:
                _subgrid = subgrid
            else:
                _subgrid = None

            set_size = set_sizes[i % len(set_sizes)]

            stimulus = cls(size=image_size, background_color=background_color, name=f"pattern{i}")
            stimulus.configure_dots(rows=rows, cols=cols, n=set_size, subgrid=_subgrid)
            stimulus.draw_dots_one_by_one(color=dot_color, line_color=line_color, path=folder)
