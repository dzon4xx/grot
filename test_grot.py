import pytest

from grot import Position, Direction, GrotGame, Board, main


@pytest.fixture
def start_pos():
    return Position(0, 0)


@pytest.fixture
def direction():
    return Direction(1, 0)


@pytest.fixture
def game():
    return GrotGame(start_pos())


def test_game_should_increment_position_when_move(game, direction, start_pos):
    # when
    game.move(direction)
    # then
    assert game.pos == start_pos + direction


def test_game_should_set_direction_is_visited_when_move(game, direction):
    # when
    assert not direction.is_visited
    game.move(direction)
    # then
    assert direction.is_visited


def test_game_should_increment_num_of_moves_when_move_in_not_visited_direction(game, direction):
    # when
    assert not direction.is_visited
    assert game.num_of_moves == 0
    game.move(direction)
    # then
    assert game.num_of_moves == 1


def test_game_should_not_increment_num_of_moves_when_move_in_visited_direction(game, direction):
    # when
    direction.is_visited = True
    assert game.num_of_moves == 0
    game.move(direction)
    # then
    assert game.num_of_moves == 0


def positions_not_on_board():
    Position.max_x = 3
    Position.max_y = 3
    return [Position(4, 3), Position(3, 4), Position(4, 4), Position(-1, 4), Position(2, -1)]


def positions_on_board():
    Position.max_x = 3
    Position.max_y = 3
    return [Position(2, 2), Position(0, 0), Position(0, 3), Position(3, 0), Position(3, 3)]


def positions_should_be_equal_when_the_same_coordinates():
    assert Position(0, 0) == Position(0, 0)


def positions_should_increment_when_direction_added():
    position = Position(0, 0)
    position += Direction(1, 0)
    assert position == Position(1, 0)


@pytest.mark.parametrize('position', positions_on_board())
def test_position_is_on_board_should_return_true_when_position_on_board(position):
    assert position.is_on_board is True


@pytest.mark.parametrize('position', positions_not_on_board())
def test_position_is_on_board_should_return_false_when_position_not_on_board(position):
    assert position.is_on_board is False


def test_direction_should_be_created_from_symbol():
    # given
    symbol = 'u'
    symbol_meaning = (0, -1)
    # when
    direction = Direction.from_symbol(symbol)
    # then
    assert (direction.dx, direction.dy) == symbol_meaning


def test_board_creates_directions_when_description_given():
    # given
    description = [['u']]
    # when
    directions = Board.create_directions(description)
    # then
    assert directions[0][0] == Direction.from_symbol('u')


def test_board_gets_direction_for_position():
    # given
    description = [['u']]
    position = Position(0, 0)
    # when
    board = Board(description)
    # then
    assert board[position] == Direction.from_symbol('u')


def test_board_should_clear_visited_directions():
    # given
    description = [['u']]
    position = Position(0, 0)
    # when
    board = Board(description)
    board[position].is_visited = True
    board.clear_visited_directions()
    # then
    assert board[position].is_visited is False


def test_board_should_yield_starting_positions():
    # given
    description = [['u']]
    Position(0, 0)
    # when
    board = Board(description)
    # then
    assert next(board.starting_positions()) == Position(0, 0)


def test_board_init_should_set_board_dimensions_for_position_class():
    # given
    description = [['u']]
    # when
    Board(description)
    # then
    assert (Position.max_x, Position.max_y) == (0, 0)


descriptions = (
    ([
     ['u', 'd', 'u', 'u'],
     ['u', 'r', 'l', 'l'],
     ['u', 'u', 'l', 'u'],
     ['l', 'd', 'u', 'l'],
     ], (3, 3)),
    ([
     ['l', 'l', 'd', 'l'],
     ['r', 'u', 'r', 'd'],
     ['d', 'u', 'r', 'r'],
     ['l', 'u', 'u', 'u'],
     ], (3, 0)),
    ([
     ['r', 'r', 'r', 'd'],
     ['d', 'l', 'l', 'l'],
     ['r', 'r', 'r', 'd'],
     ['l', 'l', 'l', 'l'],
     ], (0, 0))
)


@pytest.mark.parametrize('description, start_position', descriptions)
def test_main(description, start_position):
    assert start_position == main(description)
