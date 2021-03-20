class BoardPiece:
    """
    A class to represent an instance of a board piece. Acts as the parent
    class for the subclasses of each kind. Each piece is ONLY responsible
    for:
        - knowing its own current position
        - knowing its own name ('Red Horse', 'Blue Elephant', etc.)
        - knowing its own color
        - knowing its own possible range of movement
            (this will sometimes include illegal moves, but it is not the
            responsibility of the piece to determine the legality of each
            move. This more or less represents where a piece *could* move
            if the entire game board were blank)
    """

    def __init__(self, color, name, row, column):
        """
        Initializes current position to an empty string, which will be filled in
        upon creation of each object.
        """
        self._current_pos = (row, column)
        self._color = color
        self._name = name
        self._alphabet = 'abcdefghi'

        if self._color == 'RED':
            self._y_movement_direction = 1
            self._enemy_palace = ((8, 'd'), (8, 'e'), (8, 'f'),
                                  (9, 'd'), (9, 'e'), (9, 'f'),
                                  (10, 'd'), (10, 'e'), (10, 'f'))

        else:
            self._y_movement_direction = -1
            self._enemy_palace = ((1, 'd'), (1, 'e'), (1, 'f'),
                                  (2, 'd'), (2, 'e'), (2, 'f'),
                                  (3, 'd'), (3, 'e'), (3, 'f'))

    def update_current_pos(self, location):
        """
        Updates the pieces position on the game board

        Parameters:
            location (string)
        """
        self._current_pos = location

    def get_current_pos(self):
        """
        Returns a tuple representing (row, column)
        """
        return self._current_pos

    def get_color(self):
        """
        Returns the piece's color
        """
        return self._color

    def get_name(self):
        """
        Returns the color and type ('red horse', 'blue elephant', etc.)
        """
        return self._color + " " + self._name

    def get_movement_range(self):
        """
       Returns a list of tuples each representing a possible space within a piece's
       'range of movement'. NOTE: this will sometimes include illegal moves, but it is not the
        responsibility of the piece to determine the legality of each
        move. This more or less represents where a piece *could* move
        if the entire game board were blank. Once returned back up to the board object, the locations
        on the list are checked for legality.
        """
        pass

    @staticmethod
    def is_general():
        return False


class General(BoardPiece):
    def __init__(self, color, row, column):
        super().__init__(color, 'GENERAL', row, column)
        self._is_in_check = False

    def is_general(self):
        return True

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        current_column_index = self._alphabet.index(current_column)
        movement_range = []

        if current_row - 1 > 0:
            movement_range.append((current_row - 1, current_column))
        if current_row + 1 <= 10:
            movement_range.append((current_row + 1, current_column))
        movement_range.append((current_row, self._alphabet[current_column_index + 1]))
        movement_range.append((current_row, self._alphabet[current_column_index - 1]))

        if self.get_color() == 'BLUE':
            if current == (8, 'd') or current == (8, 'f'):
                movement_range.append((9, 'e'))
            if current == (9, 'e'):
                movement_range.append((8, 'd'))
                movement_range.append((8, 'f'))
                movement_range.append((10, 'd'))
                movement_range.append((10, 'f'))
            if current == (10, 'd') or current == (10, 'f'):
                movement_range.append((9, 'e'))

        if self.get_color() == 'RED':
            if current == (3, 'd') or current == (3, 'f'):
                movement_range.append((2, 'e'))
            if current == (2, 'e'):
                movement_range.append((1, 'd'))
                movement_range.append((1, 'f'))
                movement_range.append((3, 'd'))
                movement_range.append((3, 'f'))
            if current == (1, 'd') or current == (1, 'f'):
                movement_range.append((2, 'e'))

        return movement_range


class Guard(BoardPiece):
    """
    A guard piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'GUARD', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        current_column_index = self._alphabet.index(current_column)
        movement_range = []

        if current_row - 1 > 0:
            movement_range.append((current_row - 1, current_column))
        if current_row + 1 <= 10:
            movement_range.append((current_row + 1, current_column))
        movement_range.append((current_row, self._alphabet[current_column_index + 1]))
        movement_range.append((current_row, self._alphabet[current_column_index - 1]))

        if self.get_color() == 'BLUE':
            if current == (8, 'd') or current == (8, 'f'):
                movement_range.append((9, 'e'))
            if current == (9, 'e'):
                movement_range.append((8, 'd'))
                movement_range.append((8, 'f'))
                movement_range.append((10, 'd'))
                movement_range.append((10, 'f'))
            if current == (10, 'd') or current == (10, 'f'):
                movement_range.append((9, 'e'))

        if self.get_color() == 'RED':
            if current == (3, 'd') or current == (3, 'f'):
                movement_range.append((2, 'e'))
            if current == (2, 'e'):
                movement_range.append((1, 'd'))
                movement_range.append((1, 'f'))
                movement_range.append((3, 'd'))
                movement_range.append((3, 'f'))
            if current == (1, 'd') or current == (1, 'f'):
                movement_range.append((2, 'e'))

        return movement_range


class Horse(BoardPiece):
    """
    A horse piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'HORSE', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        current_column_index = self._alphabet.index(current_column)
        movement_range = []

        if current_row + 2 <= 10:
            if current_column_index + 1 <= len(self._alphabet) - 1:
                movement_range.append((current_row + 2, self._alphabet[current_column_index + 1]))
            if current_column_index - 1 >= 0:
                movement_range.append((current_row + 2, self._alphabet[current_column_index - 1]))
        if current_row - 2 > 0:
            if current_column_index + 1 <= len(self._alphabet) - 1:
                movement_range.append((current_row - 2, self._alphabet[current_column_index + 1]))
            if current_column_index - 1 >= 0:
                movement_range.append((current_row - 2, self._alphabet[current_column_index - 1]))
        if current_column_index + 2 <= len(self._alphabet) - 1:
            if current_row + 1 <= 10:
                movement_range.append((current_row + 1, self._alphabet[current_column_index + 2]))
            if current_row - 1 > 0:
                movement_range.append((current_row - 1, self._alphabet[current_column_index + 2]))
        if current_column_index - 2 >= 0:
            if current_row + 1 <= 10:
                movement_range.append((current_row + 1, self._alphabet[current_column_index - 2]))
            if current_row - 1 > 0:
                movement_range.append((current_row - 1, self._alphabet[current_column_index - 2]))

        return movement_range


class Elephant(BoardPiece):
    """
    An elephant piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'ELEPHANT', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        current_column_index = self._alphabet.index(current_column)
        movement_range = []

        if current_row + 3 <= 10:
            if current_column_index + 2 <= len(self._alphabet) - 1:
                movement_range.append((current_row + 3, self._alphabet[current_column_index + 2]))
            if current_column_index - 2 >= 0:
                movement_range.append((current_row + 3, self._alphabet[current_column_index - 2]))
        if current_row - 3 > 0:
            if current_column_index + 2 <= len(self._alphabet) - 1:
                movement_range.append((current_row - 3, self._alphabet[current_column_index + 2]))
            if current_column_index - 2 >= 0:
                movement_range.append((current_row - 3, self._alphabet[current_column_index - 2]))
        if current_column_index + 3 <= len(self._alphabet) - 1:
            if current_row + 2 <= 10:
                movement_range.append((current_row + 2, self._alphabet[current_column_index + 3]))
            if current_row - 2 > 0:
                movement_range.append((current_row - 2, self._alphabet[current_column_index + 3]))
        if current_column_index - 3 >= 0:
            if current_row + 2 <= 10:
                movement_range.append((current_row + 2, self._alphabet[current_column_index - 3]))
            if current_row - 2 > 0:
                movement_range.append((current_row - 2, self._alphabet[current_column_index - 3]))

        return movement_range


class Chariot(BoardPiece):
    """
    A chariot piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'CHARIOT', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        movement_range = []

        for row in range(1, 11):
            if row != current_row:
                movement_range.append((row, current_column))

        for column in self._alphabet:
            if column != current[1]:
                movement_range.append((current_row, column))

        if current == (8, 'f'):
            movement_range.append((10, 'd'))

        if current == (8, 'd'):
            movement_range.append((10, 'f'))

        if current == (10, 'd'):
            movement_range.append((8, 'f'))

        if current == (10, 'f'):
            movement_range.append((8, 'd'))

        if current == (3, 'f'):
            movement_range.append((1, 'd'))

        if current == (3, 'd'):
            movement_range.append((1, 'f'))

        if current == (1, 'd'):
            movement_range.append((3, 'f'))

        if current == (1, 'f'):
            movement_range.append((3, 'd'))

        return movement_range


class Cannon(BoardPiece):
    """
    A cannon piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'CANNON', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = current[1]
        movement_range = []

        for row in range(1, 11):
            if row != current_row:
                movement_range.append((row, current_column))

        for column in self._alphabet:
            if column != current[1]:
                movement_range.append((current_row, column))

        if current == (8, 'f'):
            movement_range.append((10, 'd'))

        if current == (8, 'd'):
            movement_range.append((10, 'f'))

        if current == (10, 'd'):
            movement_range.append((8, 'f'))

        if current == (10, 'f'):
            movement_range.append((8, 'd'))

        if current == (3, 'f'):
            movement_range.append((1, 'd'))

        if current == (3, 'd'):
            movement_range.append((1, 'f'))

        if current == (1, 'd'):
            movement_range.append((3, 'f'))

        if current == (1, 'f'):
            movement_range.append((3, 'd'))

        return movement_range


class Soldier(BoardPiece):
    """
    A soldier piece which inherits from the BoardPiece
    """

    def __init__(self, color, row, column):
        super().__init__(color, 'SOLDIER', row, column)

    def get_movement_range(self):
        current = self.get_current_pos()
        current_row = current[0]
        current_column = self._alphabet.index(current[1])
        if self._color == 'BLUE' and current_row == 1:
            forward = None
        elif self.get_color() == 'RED' and current_row == 10:
            forward = None
        else:
            forward = (current_row + self._y_movement_direction, current[1])
        if current_column == 0:
            left = None
        else:
            left = (current_row, self._alphabet[current_column - 1])
        if current_column == 8:
            right = None
        else:
            right = (current_row, self._alphabet[current_column + 1])

        directions = [forward, left, right]

        if self.get_color() == 'RED':
            if self.get_current_pos() == (8, 'd') or self.get_current_pos() == (8, 'f'):
                directions.append((9, 'e'))
            if self.get_current_pos() == (9, 'e'):
                directions.append((10, 'd'))
                directions.append((10, 'f'))

        if self.get_color() == 'BLUE':
            if self.get_current_pos() == (3, 'd') or self.get_current_pos() == (3, 'f'):
                directions.append((2, 'e'))
            if self.get_current_pos() == (2, 'e'):
                directions.append((1, 'd'))
                directions.append((1, 'f'))

        movement_range = []
        for direction in directions:
            if direction is not None:
                movement_range.append(direction)

        return movement_range
