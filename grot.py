import logging
import sys


class GrotGame:
    """State of grot game"""

    def __init__(self, start_pos):
        self.start_pos = start_pos
        self.pos = Position(start_pos.x, start_pos.y)
        self.num_of_moves = 0

    def move(self, direction):
        self.pos += direction
        if not direction.is_visited:
            self.num_of_moves += 1
            direction.is_visited = True

    @property
    def is_on_board(self):
        return self.pos.is_on_board

    def __lt__(self, other):
        return self.num_of_moves < other.num_of_moves

    def __str__(self):
        return ' '.join(['Start position: ', str(self.start_pos), 'Moves: ', str(self.num_of_moves)])


class Position:
    """Describes position on board of grot game"""

    max_x = None
    max_y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, direction):
        self.x += direction.dx
        self.y += direction.dy
        return self

    @property
    def is_on_board(self):
        return self.x >= 0 and self.x <= self.max_x and self.y >= 0 and self.y <= self.max_y

    def __str__(self):
        return ' '.join(('x: ', str(self.x), 'y: ', str(self.y)))


class Direction:
    """Describes direction of movement you can perform in game of grot"""
    directions_map = {
        'u': (0, -1),
        'd': (0, 1),
        'r': (1, 0),
        'l': (-1, 0),
    }

    def __init__(self, dx, dy, symbol=''):
        self.dx = dx
        self.dy = dy
        self._symbol = symbol
        self.is_visited = False

    @classmethod
    def from_symbol(cls, symbol):
        try:
            return cls(*cls.directions_map[symbol], symbol)
        except KeyError as e:
            raise KeyError('Symbol {} not found. Allowed symbols are: {}'
                           .format(symbol, cls.directions_map.keys())) from e

    def __eq__(self, other):
        return self.dx == other.dx and self.dy == other.dy

    def __str__(self):
        return ' '.join(('dx: ', str(self.dx), 'dy: ', str(self.dy), 'symbol: ', self._symbol))


class Board:
    """Hold all directions present on board of grot game"""

    def __init__(self, description):
        Position.max_x = len([row for row in description]) - 1
        Position.max_y = len(description[0]) - 1
        self._directions = self.create_directions(description)

    @staticmethod
    def create_directions(description):
        for y_cord, row in enumerate(description):
            for x_cord, dir_symbol in enumerate(row):
                description[y_cord][x_cord] = Direction.from_symbol(dir_symbol)
        return description

    def __getitem__(self, pos):
        direction = self._directions[pos.y][pos.x]
        return direction

    def __setitem__(self, key, value):
        pass

    def clear_visited_directions(self):
        for y_cord, row in enumerate(self._directions):
            for x_cord, dir_symbol in enumerate(row):
                self._directions[y_cord][x_cord].is_visited = False

    def starting_positions(self):
        for y_cord, row in enumerate(self._directions):
            for x_cord, step_symbol in enumerate(row):
                yield Position(x_cord, y_cord)


def main(description):
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger('grot')
    logger.setLevel(logging.INFO)
    board = Board(description)
    all_games = []
    for start_position in board.starting_positions():
        logger.debug('Start pos: {}'.format(str(start_position)))
        game = GrotGame(start_position)
        prev_direction = None
        while game.is_on_board:
            direction = board[game.pos]
            logger.debug('Next dir: {}'.format(str(direction)))
            if direction.is_visited:
                game.move(prev_direction)
            else:
                game.move(direction)
                prev_direction = direction
            if game.num_of_moves == ((Position.max_x + 1) * (Position.max_y + 1)) + 1:
                raise RuntimeError('Algorithm fault. All fields visited but game did not returned')
        board.clear_visited_directions()
        logger.debug(str(game))
        all_games.append(game)

    longest_game = max(all_games)
    logger.info('Longest game: {}'.format(str(longest_game)))
    return longest_game.start_pos.x, longest_game.start_pos.y
