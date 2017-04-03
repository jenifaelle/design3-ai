from mcu.protocol import ManchesterResultCode

from mcu.robotcontroller import RobotController

NORTH = "Nord"
SOUTH = "Sud"
EAST = "Est"
WEST = "West"

SCALING_FACTOR_FOUR = 1
SCALING_FACTOR_TWO = 0.5

ORIENTATION = {0: NORTH, 1: EAST, 2: SOUTH, 3: WEST}
MAGNIFICATION = {0: SCALING_FACTOR_TWO, 1: SCALING_FACTOR_FOUR}


class Decoder:
    def __init__(self, robot_controller: RobotController):
        self.robot_controler = robot_controller
        self.result = -1
        self.image_number = 0
        self.image_orientation = NORTH
        self.image_magnification = SCALING_FACTOR_TWO

    def decode_information(self):
        while self.result != ManchesterResultCode.SUCCESS.value:
            self.result, self.image_number, self.image_orientation, self.image_magnification\
                = self.robot_controler.decode_manchester()
            self.image_orientation = ORIENTATION[self.image_orientation]
            self.image_magnification = MAGNIFICATION[self.image_magnification]

    def get_image_number(self) -> int:
        return self.image_number

    def get_image_orientation(self) -> str:
        return self.image_orientation

    def get_image_magnification(self) -> int:
        return self.image_magnification
