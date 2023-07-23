from canvas import Canvas
import numpy as np


class ArrowSpan(Canvas):
    def __init__(self, size=(1210, 1210), mode="RGBA", background_color=(255, 255, 255, 255), name="arrow_span"):
        super(ArrowSpan, self).__init__(mode, size, background_color, name)

    @staticmethod
    def create_config(lengths=None, angles=None, image_size=(1210, 1210), background_color=(255, 255, 255, 255),
                      arrow_color=(0, 0, 0, 255), line_thickness=None, arrow_tip_width=None, arrow_tip_length=None):

        if not lengths:
            short = min(image_size[0], image_size[1]) / 5
            lengths = (short, 2 * short)

        if not angles:
            angles = (0, 45, 90, 135, 180, 225, 270, 315)

        return {"lengths": lengths, "angles": angles, "image_size": image_size, "background_color": background_color,
                "arrow_color": arrow_color, "line_thickness": line_thickness, "arrow_tip_width": arrow_tip_width,
                "arrow_tip_length": arrow_tip_length}

    @classmethod
    def create_all_arrows(cls, config=None):
        if not config:
            config = cls.create_config()

        arrows = []
        for length in config["lengths"]:
            for angle in config["angles"]:
                new_arrow = cls(size=config["image_size"], background_color=config["background_color"],
                                name=f"arrow_{length}_{angle}")
                new_arrow.draw_radial_arrow(angle=angle, length=length, color=config["arrow_color"],
                                            line_thickness=config["line_thickness"],
                                            tip_width=config["arrow_tip_width"],
                                            tip_length=config["arrow_tip_length"])
                arrows.append(new_arrow)

        return np.array(arrows)

    @classmethod
    def create_set(cls, arrows, set_size=6, name="set"):
        arrow_set = np.random.choice(arrows, set_size)

        for i, arrow in enumerate(arrow_set):
            arrow.name = f"{name}_{i}"

        return arrow_set

    @classmethod
    def create_batch(cls, batch_size=15, set_size=6, folder="arrow_span/", config=None):
        arrows = cls.create_all_arrows(config)
        for i in range(batch_size):
            new_set = cls.create_set(arrows, set_size, name=f"set{i}")
            for arrow in new_set:
                arrow.save(path=folder)
