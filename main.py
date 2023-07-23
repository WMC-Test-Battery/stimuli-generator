from PIL import Image, ImageDraw
from geometry import Vector, Point
from symmetry_span import SymmetrySpan
from arrow_span import ArrowSpan


if __name__ == "__main__":
    SymmetrySpan.create_batch()
    config = ArrowSpan.create_config(background_color=(255, 255, 255, 255))
    ArrowSpan.create_batch(batch_size=1, set_size=16, config=config)
