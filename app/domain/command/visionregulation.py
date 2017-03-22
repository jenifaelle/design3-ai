import time
import json
from websocket import create_connection
from mcu.robotcontroller import robot_controller, set_move_destination
from domain.gameboard.position import Position
from mcu.commands import regulator
from mcu import robotcontroller

DELTA_T = 0.3


class VisionRegulation:
    def __init__(self):
        self.connection = None

    def set_url(self, url):
        self.connection = create_connection("ws://" + url + ":3000")

    def push_path(self, path):
        new_path = []
        for pos in path:
            x = pos.pos_x
            y = pos.pos_y
            new_pos = {'x': x, 'y': y}
            new_path.append(new_pos)

        data = {}
        data["headers"] = "push_path"
        data["data"] = new_path
        self.connection.send(json.dumps(data))

    def go_to_positions(self, positions):
        for position in positions:
            print("####DEBUG####\n{}\n".format(position))
            self.go_to_position(position)

    def go_to_position(self, position):
        data = {}
        data["headers"] = "pull_robot_position"
        data["data"] = {}
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()

        robot_position_info = json.loads(robot_position_json)
        pos_x = float(robot_position_info['x'])
        pos_y = float(robot_position_info['y'])
        pos_t = float(robot_position_info['theta'])
        robot_position = Position(int(pos_x), int(pos_y), pos_t)
        set_move_destination(position)

        now = time.time()
        last_time = time.time()

        while not regulator.is_arrived(robot_position):
            now = time.time()
            delta_t = now - last_time
            if delta_t > DELTA_T:
                last_time = time.time()
                self.connection.send(json.dumps(data))

                robot_position_json = self.connection.recv()
                try:
                    robot_position_info = json.loads(robot_position_json)
                    pos_x = float(robot_position_info['x'])
                    pos_y = float(robot_position_info['y'])
                    theta = float(robot_position_info['theta'])
                except (json.JSONDecodeError, ValueError) as e:
                    pos_x = 0
                    pos_y = 0
                    theta = 0
                robot_position = Position(int(pos_x), int(pos_y), theta)

                robot_controller.send_move_command(robot_position, delta_t)

        robotcontroller.set_move_destination(robot_position)
        robot_controller.send_move.command(robot_position)
        

vision_regulator = VisionRegulation()