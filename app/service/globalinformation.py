import json

import requests
from typing import Tuple, List

from domain.gameboard.position import Position
from websocket import create_connection

from domain.pathfinding.dijkstra import ObstacleType


ROBOT_RADIUS = 150


class GlobalInformation:
    def __init__(self):
        self.connection = None

    def set_url(self, url: str):
        self.base_station_url = url
        self.connection = create_connection("ws://" + url + ":3000")

    def get_robot_position(self):
        data = {'headers': 'pull_robot_position',
                'data': {}}
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()
        robot_position_info = json.loads(robot_position_json)
        pos_x = int(float(robot_position_info['x']))
        pos_y = int(float(robot_position_info['y']))
        theta = float(robot_position_info['theta'])
        robot_position = Position(pos_x, pos_y, theta)
        return robot_position

    def get_robot_orientation(self):
        pos = self.get_robot_position()
        return pos.theta

    def get_obstacles(self) -> List[Tuple[Position, int, ObstacleType]]:
        # pos, radius, tag
        data_json = requests.get("http://{}:12345/obstacles".format(self.base_station_url)).json()
        obstacles = data_json['data']['obstacles']

        formated_obstacles = []
        for obstacle in obstacles:
            pos = Position(int(obstacle['position']['x']), int(obstacle['position']['y']))
            radius = obstacle['dimension']['length']
            tag = obstacle['tag']
            if tag == "RIGHT":
                obs_type = ObstacleType.PASS_BY_RIGHT
            elif tag == "LEFT":
                obs_type = ObstacleType.PASS_BY_LEFT
            else:
                obs_type = ObstacleType.NORMAL

            obs = pos, radius, obs_type
            formated_obstacles.append(obs)

        return formated_obstacles

    def get_drawzone_corner_position(self):
        pass

    def get_robot_radius(self):
        return ROBOT_RADIUS

    def get_board_dimensions(self) -> Tuple[int, int]:
        # FIXME!
        return 10, 10

