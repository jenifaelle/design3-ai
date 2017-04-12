import sys
import queue
import math
from domain.pathfinding.grid import Grid


class NoPathFound(Exception):
    pass


BEFORE = True


class Information:
    def __init__(self, allo, bo):
        self.value = allo
        self.boolean = bo

    def set_value(self, intege):
        self.value = intege

    def set_bool(self, boolea):
        self.boolean = boolea


class RobotPositionInvalid(Exception):
    def __init__(self, position):
        message = "Robot position is invalid : " + str(position)
        Exception.__init__(self, message)


class PathFinding:
    def __init__(self, game_board, begin_position, end_position):
        self.grid = Grid(game_board)
        self.obstacles_position = game_board.obstacles_position
        self.begin_position = begin_position
        self.end_position = end_position
        self.end_position.set_weight(0)
        self.information = Information(0, True)

    def find_path(self):
        if self.end_position.weight == sys.maxsize:
            self.end_position = find_closes_destination(self.grid, self.end_position)

        if self.begin_position.weight == sys.maxsize:
            raise RobotPositionInvalid(self.begin_position)

        initialise_weight(self.grid, self.end_position)

        path = find(
            self.grid, self.begin_position, self.end_position, self.obstacles_position, self.grid.width,
            self.grid.length, self.information
        )
        return path


def find(grid, begin_position, end_position, obstacles_position, width, length, information):
    path = []
    current_neighbor = begin_position
    while current_neighbor.weight > 0:
        neighbors = grid.neighbors(current_neighbor)
        new_neighbors = removed_already_visited_neighbors(neighbors, path)
        current_neighbor = find_minimum(new_neighbors, end_position, obstacles_position, width, length, information)
        current_neighbor.set_path()
        path.append(current_neighbor)
    return path


def find_closes_destination(grid, end_position):
    neighbors = queue.Queue()
    neighbors.put(end_position)
    current_neighbor = end_position
    visited_neighbors = []
    while current_neighbor.weight == sys.maxsize:
        current_neighbor = neighbors.get()
        new_neighbors = grid.neighbors(current_neighbor)
        for new_neighbor in new_neighbors:
            if not new_neighbor in visited_neighbors:
                visited_neighbors.append(new_neighbor)
                neighbors.put(new_neighbor)
    closest = []
    while not neighbors.empty():
        postentionnaly_closest = neighbors.get()
        if not postentionnaly_closest.weight == sys.maxsize:
            closest.append(postentionnaly_closest)
    return find_real_value_minimum(closest, end_position)


def find_real_value_minimum(neighbors, destination):
    old_distance = sys.maxsize
    current_neighbor = neighbors[0]
    for neighbor in neighbors:
        new_distance = (neighbor.pos_x - destination.pos_x)**2 + (neighbor.pos_y - destination.pos_y)**2
        if new_distance <= old_distance:
            old_distance = new_distance
            current_neighbor = neighbor
    return current_neighbor


def find_distance_from_closest_obstacle(neighbor, obstacles_position, width, length, information):
    old_distance = sys.maxsize
    critic_wall = 3
    for obstacle_position in obstacles_position:
        new_distance = math.sqrt(
            (neighbor.pos_x - obstacle_position.pos_x)**2 + (neighbor.pos_y - obstacle_position.pos_y)**2
        )
        if new_distance <= old_distance:
            old_distance = new_distance

    #print("last_distance_from_obstacle : " + str(information.value))
    #print("old_distance : " + str(old_distance))
    #print(information)
    if old_distance < information.value:
        information.set_bool(True)
    if old_distance > information.value:
        information.set_bool(False)
    information.set_value(old_distance)
    if neighbor.pos_x < critic_wall or (width - neighbor.pos_x) < critic_wall:
        old_distance = neighbor.pos_x
    if neighbor.pos_y < critic_wall or (length - neighbor.pos_y) < critic_wall:
        old_distance = neighbor.pos_y

    return old_distance


def find_minimum(neighbors, destination, obstacles_position, width, length, information):
    if len(neighbors) <= 0:
        raise NoPathFound
    current_neighbor = neighbors[0]
    #print("new min")
    new_min = []
    for neighbor in neighbors:
        if neighbor.weight < current_neighbor.weight:
            new_min = []
            current_neighbor = neighbor
            new_min.append(neighbor)
        if neighbor.weight <= current_neighbor.weight:
            new_min.append(neighbor)

    if information.boolean and not BEFORE:
        print("Dangerus")
        old_distance = 0
        for neighbor in new_min:
            #new_distance = (neighbor.pos_x - destination.pos_x)**2 + (neighbor.pos_y - destination.pos_y)**2
            new_distance = find_distance_from_closest_obstacle(neighbor, obstacles_position, width, length, information)
            if new_distance >= old_distance:
                old_distance = new_distance
                current_neighbor = neighbor
    else:
        print("Easy")
        old_distance = sys.maxsize
        for neighbor in new_min:
            new_distance = (neighbor.pos_x - destination.pos_x)**2 + (neighbor.pos_y - destination.pos_y)**2
            find_distance_from_closest_obstacle(neighbor, obstacles_position, width, length, information)
            if new_distance <= old_distance:
                old_distance = new_distance
                current_neighbor = neighbor

    return current_neighbor


def removed_already_visited_neighbors(neighbors, path):
    new_neighbors = []
    for neighbor in neighbors:
        if neighbor not in path and not (neighbor.weight == sys.maxsize):
            new_neighbors.append(neighbor)
    return new_neighbors


def initialise_weight(grid, begin_position):
    neighbors = queue.Queue()
    neighbors.put(begin_position)
    while not neighbors.empty():
        neighbor = neighbors.get()
        new_neighbors = grid.neighbors(neighbor)
        for new_neighbor in new_neighbors:
            if new_neighbor.weight == -1:
                new_neighbor.set_weight(neighbor.weight + 1)
                neighbors.put(new_neighbor)
