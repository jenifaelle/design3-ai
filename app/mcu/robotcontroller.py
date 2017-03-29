"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import enum

import serial
import time
import math

from domain.gameboard.position import Position
from mcu import protocol
from mcu import servos
from mcu.commands import regulator, correct_for_referential_frame, MoveCommand, DecodeManchesterCommand, GetManchesterPowerCommand
from mcu.protocol import PencilStatus
from service.globalinformation import GlobalInformation

if __name__ == "__main__":
    from mcu.protocol import Leds
    from mcu.commands import ICommand, LedCommand, MoveCommand
else:
    from mcu.protocol import Leds
    from .commands import ICommand, LedCommand

SERIAL_MCU_DEV_NAME = "ttySTM32"
SERIAL_POLULU_DEV_NAME = "ttyPololu"
REGULATOR_FREQUENCY = 0.1 # secondes


class RobotSpeed(enum.Enum):
    NORMAL_SPEED = (80, 25)
    DRAW_SPEED = (20, 4)


constants = [(0.027069, 0.040708, 0, 16),  # REAR X
             (0.0095292, 0.029466, 0, 13),  # FRONT Y
             (0.015431, 0.042286, 0, 15),  # FRONT X
             (0.030357, 0.02766, 0, 13)]  # REAR Y


class SerialMock:
    def write(self, arg, byteorder='little'):
        print("Serial mock: {} -- ".format(arg, byteorder))
        return -1

    def read(self, nbr_byte):
        print("Serial mock reading! ({})".format(nbr_byte))
        return b'\x00'


class RobotController(object):
    """" Controleur du robot, permet d'envoyer les commandes et de recevoir certaines informations du MCU."""
    def __init__(self, global_information: GlobalInformation):
        """" Si aucun lien serie n'est disponible, un SerialMock est instancie."""
        try:
            self.ser_mcu = serial.Serial("/dev/{}".format(SERIAL_MCU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for mcu!")
            self.ser_mcu = SerialMock()

        try:
            self.ser_polulu = serial.Serial("/dev/{}".format(SERIAL_POLULU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for polulu!")
            self.ser_polulu = SerialMock()

        self.last_timestamp = time.time()
        self._init_mcu_pid()
        self._startup_test()
        self.global_information = global_information
        self.record_power = False
        self.powers = {}

    def send_command(self, cmd: ICommand):
        """"
        Prend une commande et s'occupe de l'envoyer au MCU.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser_mcu.write(cmd.pack_command())

    def display_encoder(self):
        readings = []
        for motor in protocol.Motors:
            readings.append(self.read_encoder(motor, self.ser_mcu))
        print("(rear_x) {} -- (front_y) {} -- (front_x) {} -- (rear_y) {}".format(readings[0], readings[1], readings[2], readings[3]))

    def send_move_command(self, robot_position: Position, delta_t=None):
        now = time.time()
        if delta_t:
            regulator_delta_t = delta_t
        else:
            regulator_delta_t = now - self.last_timestamp
        self.last_timestamp = now
        cmd = MoveCommand(robot_position, regulator_delta_t)
        self.ser_mcu.write(cmd.pack_command())

    def send_servo_command(self, cmd):
        """"
        Prend une commande et s'occupe de l'envoyer au Pololu.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser_polulu.write(cmd)

    def read_encoder(self, motor_id: protocol.Motors) -> int:
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(protocol.generate_read_encoder(motor_id))
        self.ser_mcu.read(1)
        speed = self.ser_mcu.read(2)
        return int.from_bytes(speed, byteorder='big')

    def lower_pencil(self):
        cmd = servos.generate_pencil_command(servos.PencilStatus.LOWERED)
        self.send_servo_command(cmd)
        init_time = time.time()
        while time.time() - init_time < 1:
            pass

    def raise_pencil(self):
        cmd = servos.generate_pencil_command(servos.PencilStatus.RAISED)
        self.send_servo_command(cmd)
        init_time = time.time()
        while time.time() - init_time < 1:
            pass

    def light_red_led(self):
        cmd = LedCommand(Leds.UP_RED)
        self.send_command(cmd)

    def shutdown_red_led(self):
        cmd = LedCommand(Leds.DOWN_RED)
        self.send_command(cmd)

    def blink_green_led(self):
        cmd = LedCommand(Leds.BLINK_GREEN)
        self.send_command(cmd)

    def decode_manchester(self):
        cmd = DecodeManchesterCommand()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.send_command(cmd)

        result_code = int.from_bytes(self.ser_mcu.read(1), byteorder='big') # Decode result (success or error)
        figure_number = int.from_bytes(self.ser_mcu.read(1), byteorder='big')
        orientation = int.from_bytes(self.ser_mcu.read(1), byteorder='big')
        scaling_factor = int.from_bytes(self.ser_mcu.read(1), byteorder='big')

        return [result_code, figure_number, orientation, scaling_factor]

    def reset_state(self):
        cmd = protocol.generate_reset_state_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu_write(cmd) # Command does not expect any response.

    def reset_traveled_distance(self):
        cmd = protocol.generate_reset_traveled_distance_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd) # Command does not expect any response.

    def get_traveled_distance(self):
        cmd = protocol.generate_get_traveled_distance_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)

        traveled_distance_frontx = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_rearx = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_fronty = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_reary = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)

        return [traveled_distance_frontx, traveled_distance_rearx, traveled_distance_fronty, traveled_distance_reary]
        
    def get_manchester_power(self):
        cmd = protocol.generate_get_manchester_power()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)
        power_bytes = self.ser_mcu.read(2)
        power = int.from_bytes(power_bytes, byteorder='big')
        return power

    def move(self):
        """" S'occupe d'amener le robot a la bonne position. BLOQUANT! """
        retroaction = self.global_information.get_robot_position()
        now = time.time()
        last_time = now

        while not regulator.is_arrived(retroaction):
            retroaction = self.global_information.get_robot_position()
            now = time.time()
            delta_t = now - last_time
            if delta_t > REGULATOR_FREQUENCY:
                last_time = now
                self.send_move_command(retroaction, delta_t)
                if self.record_power:
                    power_level = self.get_manchester_power()
                    print("Power level: {}".format(power_level))
                    self.powers[retroaction] = power_level

    def precise_move(self, vec: Position, speed: Position=Position(20, 20)):
        self.reset_traveled_distance()

        retroaction = self.global_information.get_robot_position()
        angle = retroaction.theta

        distance_to_move_x, distance_to_move_y = correct_for_referential_frame(vec.pos_x, vec.pos_y, angle)
        target_speed_x, target_speed_y = correct_for_referential_frame(speed.pos_x, speed.pos_y, angle)

        last_timestamp = time.time()

        remaining_x, remaining_y = self.get_remaining_distances(distance_to_move_x, distance_to_move_y)
        while remaining_x > 0 or remaining_y > 0:
            delta_t = time.time() - last_timestamp
            if delta_t > REGULATOR_FREQUENCY:
                last_timestamp = time.time()
                if remaining_x > 0:
                    speed_x = target_speed_x
                else:
                    speed_x = 0

                if remaining_y > 0:
                    speed_y = target_speed_y
                else:
                    speed_y = 0

                cmd = protocol.generate_move_command(speed_x, speed_y, 0)
                self.ser_mcu.write(cmd)
                self.ser_mcu.read(self.ser_mcu.inWaiting())

                remaining_x, remaining_y = self.get_remaining_distances(distance_to_move_x, distance_to_move_y)

        cmd = protocol.generate_move_command(0, 0, 0)
        self.ser_mcu.write(cmd)

    def get_remaining_distances(self, target_distance_x, target_distance_y):
        distances = self.get_traveled_distance()
        distance_x = distances[3]
        distance_y = distances[1]
        remaining_x = target_distance_x - distance_x
        remaining_y = target_distance_y - distance_y
        return remaining_x, remaining_y

    def start_power_recording(self):
        self.record_power = True
        self.powers = {}

    def stop_power_recording(self):
        self.record_power = False

    def get_max_power_position(self) -> Position:
        max_level = 0
        max_pos = None
        for pos, power_level in self.powers.items():
            if power_level > max_level:
                max_level = power_level
                max_pos = pos
        return max_pos

    def set_robot_speed(self, speed: RobotSpeed):
        move_speed, deadzone = speed.value
        regulator.set_speed(move_speed, deadzone)

    def _init_mcu_pid(self):
        for motor in protocol.Motors:
            kp, ki, kd, dz = constants[motor.value]
            cmd = protocol.generate_set_pid_constant(motor, kp, ki, kd, dz)
            self.ser_mcu.write(cmd)

    def _startup_test(self):
        """ Effectue un test de base pour s'assurer que le MCU repond et met le MCU en mode de debogage."""
        print("startup test")
        cmd = LedCommand(Leds.UP_GREEN)
        self.send_command(cmd)
        time.sleep(1)
        cmd = LedCommand(Leds.DOWN_GREEN)
        self.send_command(cmd)
        cmd = LedCommand(Leds.UP_RED)
        self.send_command(cmd)
        time.sleep(1)
        cmd = LedCommand(Leds.DOWN_RED)
        self.send_command(cmd)
        self.raise_pencil()

        # Hack pour contourner le probleme que les moteurs parfois ne roule pas en positif avant d'avoir recu une
        # commande negative
        negative_speed_cmd = protocol.generate_move_command(-20, -20, 0)
        self.ser_mcu.write(negative_speed_cmd)
        time.sleep(0.1)
        positive_speed_cmd = protocol.generate_move_command(20, 20, 0)
        self.ser_mcu.write(positive_speed_cmd)
        time.sleep(0.1)
        null_speed_cmd = protocol.generate_move_command(0, 0, 0)
        self.ser_mcu.write(null_speed_cmd)

    def _get_return_code(self):
        return int.from_bytes(self.ser_mcu.read(1), byteorder='little')


def set_move_destination(move_destination: Position):
    regulator.setpoint = move_destination
