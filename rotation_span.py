from canvas import Canvas
import numpy as np


class RotationSpan(Canvas):
    def __init__(self, size=(1210, 1210), mode="RGBA", background=(255, 255, 255, 255), name="arrow_span"):
        super(RotationSpan, self).__init__(mode, size, background, name)
