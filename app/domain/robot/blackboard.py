from typing import Dict

from domain.gameboard.position import Position


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None
        self.images_position: Dict[int, Position] = {
            0: Position(1959, 366, 1.57),
            1: Position(2024, 305, 1.22),
            2: Position(1933, 267, 0.35),
            3: Position(1890, 360, 0.00),
            4: Position(1929, 615, 0),
            5: Position(1940, 750, -0.20),
            6: Position(2096, 551, -1.37),
            7: Position(2005, 580, -1.75)
        }

    def get_image_segments(self):
        self.segments_image += [self.segments_image[0]]
        return self.segments_image

    def get_image_id(self):
        return self.id_image
