from PIL import Image, ImageDraw
from geometry import Vector, Point
from symmetry_span import SymmetrySpanStimulus


def create_symmetry_span_example_batch(trial_pairs=6):
    for i in range(trial_pairs):
        stimulus = SymmetrySpanStimulus(background=(255, 255, 255, 255), name=f"sym{i}")
        stimulus.configure_grid(symmetric=True)
        stimulus.draw_grid()
        stimulus.save(path=f"images/")

        stimulus = SymmetrySpanStimulus(background=(255, 255, 255, 255), name=f"nsym{i}")
        stimulus.configure_grid(symmetric=False, noise=0.5)
        stimulus.draw_grid()
        stimulus.save(path=f"images/")


if __name__ == "__main__":
    create_symmetry_span_example_batch()
