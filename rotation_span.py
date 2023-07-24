from canvas import Canvas
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class RotationSpan(Canvas):
    def __init__(self, size=(1210, 1210), mode="RGBA", background_color=(255, 255, 255, 255), name="arrow_span"):
        super(RotationSpan, self).__init__(size=size, mode=mode, background_color=background_color, name=name)

    @staticmethod
    def create_config(letters=None, angles=None, image_size=(1210, 1210), background_color=(255, 255, 255, 255),
                      letter_location=None, letter_color=(0, 0, 0, 255), font_size=None, font=None):

        if not letters:
            letters = ["G", "F", "R"]

        if not angles:
            angles = (0, 45, 90, 135, 180, 225, 270, 315)

        return {"letters": letters, "angles": angles, "image_size": image_size, "background_color": background_color,
                "letter_location": letter_location, "letter_color": letter_color, "font_size": font_size,
                "font": font}

    @classmethod
    def create_all_letters(cls, config=None):
        if not config:
            config = cls.create_config()

        letters = []
        for letter in config["letters"]:
            for angle in config["angles"]:
                new_letter = cls(size=config["image_size"], background_color=config["background_color"],
                                 name=f"letter_{letter}_{angle}")
                new_letter.draw_letter(letter=letter, location=config["letter_location"], color=config["letter_color"],
                                       mirror=False, angle=angle, font=config["font"], size=config["font_size"])
                letters.append(new_letter)

                new_letter = cls(size=config["image_size"], background_color=config["background_color"],
                                 name=f"letter_{letter}_{angle}")
                new_letter.draw_letter(letter=letter, location=config["letter_location"], color=config["letter_color"],
                                       mirror=True, angle=angle, font=config["font"], size=config["font_size"])
                letters.append(new_letter)

        return np.array(letters)

    @classmethod
    def create_set(cls, letters, set_size=6, name="set"):
        letter_set = np.random.choice(letters, set_size)

        for i, letter in enumerate(letter_set):
            letter.name = f"{name}_{i}"

        return letter_set

    @classmethod
    def create_batch(cls, batch_size=12, set_sizes=(2, 3, 4, 5), folder="rotation_span/", config=None):
        letters = cls.create_all_letters(config)
        for i in range(batch_size):
            set_size = set_sizes[i % len(set_sizes)]

            new_set = cls.create_set(letters, set_size, name=f"set{i}")
            for arrow in new_set:
                arrow.save(path=folder)
