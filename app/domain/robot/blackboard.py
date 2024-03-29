from typing import Dict

from domain.gameboard.position import Position

POSITIONS = [Position(1895, 330, 1.52), Position(1910, 290, 1.00), Position(1910, 250, 0.37), Position(1895, 330, 0.00),
             Position(1900, 560, 0.00), Position(1910, 635, -0.50), Position(1910, 630, -1.05),
             Position(1910, 605, -1.54)]
ANTENNA_MARK_LENGTH = 8

class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None
        self.images_position: Dict[int, Position] = {0: POSITIONS[0],
                                                     1: POSITIONS[1],
                                                     2: POSITIONS[2],
                                                     3: POSITIONS[3],
                                                     4: POSITIONS[4],
                                                     5: POSITIONS[5],
                                                     6: POSITIONS[6],
                                                     7: POSITIONS[7]
                                                     }

    def get_image_segments(self):
        self.segments_image += [self.segments_image[0]]
        return self.segments_image

    def get_image_id(self):
        return self.id_image

    def get_image_position(self, image_id):
        return self.images_position[image_id]
      
    def has_antenna_position(self):
        if self.antenna_position:
            return True
        else:
            return False

    def set_image_segments(self, image_segments):
        self.segments_image = image_segments

    def get_antenna_position(self):
        return self.antenna_position

    def get_segment_image_list(self):
        return self.segments_image

    def get_mark_move(self, robot_position):
        return (robot_position + Position(0, -ANTENNA_MARK_LENGTH))