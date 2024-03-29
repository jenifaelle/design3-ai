from domain.gameboard.position import Position


def get_filter_path(path, scaling=1):
    filter_path = []
    if len(path) == 0:
        return filter_path
    last_x = path[0].pos_x
    last_y = path[0].pos_y
    last_increment_x = 0
    last_increment_y = 0
    is_first = True
    is_second = True
    index = 0
    for position in path:
        is_corner = False
        if (position.pos_y == last_y + 1) and (last_increment_y != +1):
            last_increment_y = 1
            is_corner = True
        if (position.pos_y == last_y - 1) and (last_increment_y != -1):
            last_increment_y = -1
            is_corner = True
        if (position.pos_x == last_x + 1) and (last_increment_x != 1):
            last_increment_x = 1
            is_corner = True
        if (position.pos_x == last_x - 1) and (last_increment_x != -1):
            last_increment_x = -1
            is_corner = True
        if (position.pos_y == last_y) and (last_increment_y != 0):
            last_increment_y = 0
            is_corner = True
        if (position.pos_x == last_x) and (last_increment_x != 0):
            last_increment_x = 0
            is_corner = True
        if is_first:
            is_corner = False
            is_first = False
        elif is_second:
            is_corner = False
            is_second = False
        if is_corner:
            point = path[index - 1]
            filter_path.append(Position(point.pos_x * scaling, point.pos_y * scaling))
        last_y = position.pos_y
        last_x = position.pos_x
        index = index + 1
    last_position = path[len(path) - 1]
    filter_path.append(Position(last_position.pos_x * scaling, last_position.pos_y * scaling))
    return filter_path
