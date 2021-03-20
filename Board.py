from BoardPieces import *


class JanggiBoard:
    """
    A class to represent an instance of a Janggi game. Responsible for
    knowing current status of the game: who's turn it is, if someone is
    in check, if someone has won, and interacting with the game board.
    Details of implementing moves and tracking rules of each piece are
    abstracted down into the JanggiBoard and BoardPiece classes. Janggi
    game will contain a JanggiBoard object and will only be responsible
    for interacting with that object and tracking status.

    Attributes:
        _board : a game board constructed by a dictionary of dictionaries. Each
                 row is represented by a numerical key and each column sub key
                 by a character. The game piece objects are placed directly within
                 the dictionary

        _red_palace :  a tuple of tuples with each inner tuple representing a coordinate pair
                       on the board. These coordinates will be used to determine the legal range
                       of movement for Generals and Guards.

       _blue_palace : a tuple of tuples with each inner tuple representing a coordinate pair
                       on the board. These coordinates will be used to determine the legal range
                       of movement for Generals and Guards.

       _general_locations : a dictionary containing the current location of each players general

       _alphabet : a string with the first 9 lowercase letters of the alphabet. used to help
                   determine indices for ranges of motion.

       _checkmate : boolean value signalling if game is currently over or not
    """

    def __init__(self):
        # creates a game board made up of a dictionary of dictionaries
        self._board = \
            {number: {letter: None for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']}
             for number in range(1, 11)}

        new_pieces = self.pieces_generator()

        current_row = 0
        for row in self._board.values():
            current_row += 1
            for column in row.keys():
                self._board[current_row][column] = next(new_pieces)

        # (row, column)
        self._red_palace = ((1, 'd'), (1, 'e'), (1, 'f'),
                            (2, 'd'), (2, 'e'), (2, 'f'),
                            (3, 'd'), (3, 'e'), (3, 'f'))

        self._blue_palace = ((8, 'd'), (8, 'e'), (8, 'f'),
                             (9, 'd'), (9, 'e'), (9, 'f'),
                             (10, 'd'), (10, 'e'), (10, 'f'))

        self._general_locations = {'BLUE': (9, 'e'), 'RED': (2, 'e')}

        # used for indexing
        self._alphabet = 'abcdefghi'

        self._checkmate = False

    def pass_legality_check(self, move_to, piece, current_turn, hypothetical_movement=False):
        """
        This method is used to determine if a potential move is legal or not. The method call
        takes on two general types:
            1) Hypothetical: if the hypothetical_movement parameter is supplied an argument of
            True then legality checks involving a general check status are skipped due to the
            fact that determining a general's check status requires use of this same method to
            determine if other game pieces are able to make a hypothetical "capture" of the
            general on the next turn. Though such a capture never happens, this means a general
            is in check.

            2) Real: if no argument is supplied in place of hypothetical_movement, then it defaults
            to false and a real movement attempt is being made. The attempted move passes through
            all the legality checks based on the type of piece it is.

        Parameters:
            move_to (tuple) : represents the space to move TO
            piece (BoardPiece object) : the object to be moved to move_to
            current_turn (string) : the string representation of who's turn it is
            hypothetical_movement (bool) : determines whether the legality is being
                                            assessed for a real move or not.

        Returns:
            (bool): whether or not the desired move is legal
        """
        piece_color = piece.get_color()
        if piece_color == 'BLUE':
            opposing_color = 'RED'
        else:
            opposing_color = 'BLUE'

        movement_range = piece.get_movement_range()
        general = self.get_location_contents(self._general_locations[current_turn])

        if not hypothetical_movement:
            # if the player's general is in check, and they aren't attempting to move that
            # general, check if there exists any move which would break the check. If not
            # the player cannot do this as their only option is to move the general
            if self.get_general_check_status(current_turn) is True and piece != general:
                if not self.can_friendly_break_check(general):
                    return False
                elif not self.test_save_general_movement(piece, move_to, piece_color):
                    return False
            # if the player's general is in check and the piece they are trying to move
            # is their general. Checks to see if that general has an escape path or not.
            elif self.get_general_check_status(current_turn) is True \
                    and self.safe_general_move_check(opposing_color, move_to) is False:
                return False

        # object trying to move belongs to other player
        if piece_color != current_turn:
            return False

        # movement is out of game piece's legal move range
        elif move_to not in movement_range:
            return False

        # trying to move into a place where a piece of the same color exists (take one's own piece)
        elif self.get_location_contents(move_to) is not None \
                and piece_color == self.get_location_contents(move_to).get_color():
            return False

        # cannons cant capture other cannons
        if self.get_location_contents(move_to) is not None:
            if "CANNON" in piece.get_name() and \
                    "CANNON" in self.get_location_contents(move_to).get_name():
                return False

        # generals or guards cannot leave the palace
        if "GENERAL" in piece.get_name() or "GUARD" in piece.get_name():
            if move_to not in self._blue_palace and move_to not in self._red_palace:
                return False

        # this legality check calls a method to check for pieces in the path of its
        # movement. For chariot, it requires there to be none in the path.
        if "CHARIOT" in piece.get_name():
            current_pos = piece.get_current_pos()
            if self.pieces_in_orthogonal_path(current_pos, move_to) != 0:
                return False

        # this legality check calls a method to check for pieces in the path of its
        # movement. For chariot, it requires there to be at least ONE in its path.
        # It also requires that the piece to be jumped over is not a cannon. It checks
        # for this by supplying any additional argument to the method that returns a bool
        # for whether or not the piece in the path matches the specified string.
        if "CANNON" in piece.get_name():
            current_pos = piece.get_current_pos()
            if self.pieces_in_orthogonal_path(current_pos, move_to) != 1:
                return False
            if self.pieces_in_orthogonal_path(current_pos, move_to, "CANNON"):
                return False

        # calls a method specific to elephants to see if the elephant is blocked anywhere
        # along its path
        if "ELEPHANT" in piece.get_name():
            if self.is_elephant_path_blocked(piece, move_to):
                return False

        # calls a method specific to horses to see if the elephant is blocked anywhere
        # along its path
        if "HORSE" in piece.get_name():
            if self.is_horse_path_blocked(piece, move_to):
                return False
        return True

    def get_location_contents(self, coordinates):
        """
        Takes in a tuple representing a row and column
        and returns the game piece object at the board
        coordinates, or None if none is there.

        Parameters:
            coordinates : a tuple representing a location on the game board (row (int), column (string))

        Returns:
            BoardPiece object located at coordinates, or None
        """
        return self._board[coordinates[0]][coordinates[1]]

    def move_piece(self, move_from, move_to, current_turn):
        """
        Takes as arguments the to location and the from location
        for the desired move as well as a string representing
        who's turn it currently is. Passes these into _pass_legality_check
        method. If legality check method returns true, the board is updated
        to reflect a successful move.


        Parameters:
            move_from : tuple coordinates
            move_to : tuple coordinates
            current_turn : string representing current turn

        Returns:
            (bool) move successful or not
        """
        board_piece = self.get_location_contents(move_from)

        if board_piece is None:
            return False
        elif self.pass_legality_check(move_to, board_piece, current_turn) is False:
            return False
        else:
            self._board[move_to[0]][move_to[1]] = board_piece
            self._board[move_from[0]][move_from[1]] = None
            board_piece.update_current_pos(move_to)

            if board_piece.is_general():
                self._general_locations[current_turn] = move_to

            return True

    def print_board(self):
        """
        Visual representation of the board for debugging purposes
        """
        display_row = -1

        display = [[],
                   [],
                   [],
                   [],
                   [],
                   [],
                   [],
                   [],
                   [],
                   []]

        for row in self._board.values():
            display_row += 1
            for item in row.values():
                if item is not None:
                    display_spot = item.get_name()
                    display[display_row].append(display_spot)
                else:
                    display[display_row].append("__________")

        for row in display:
            print(row)

    def is_general_stuck(self, general, opposing_color):
        """
        Checks if the general has any move available that would not
        put it in check.


        Parameters:
            general (BoardPiece object)
            opposing_color (String)

        Returns:
            True if the general has no moves, False if moves
            are available.
        """
        general_range = general.get_movement_range()
        general_color = general.get_color()
        escape_options = []
        check_zone = []

        # determining a 'check zone' which the general cannot move into
        for row in self._board.values():
            for item in row.values():
                if item is not None and item.get_color() == opposing_color:
                    for location in item.get_movement_range():
                        if self.pass_legality_check(location, item, opposing_color, True):
                            check_zone.append(location)

        # determining the overlap if general's movement range and the check zone
        for option in general_range:
            if option not in check_zone and self.pass_legality_check(option, general, general_color, True):
                escape_options.append(option)

        if len(escape_options) == 0:
            return True
        else:
            return False

    def safe_general_move_check(self, opposing_color, move_to):
        """
        Checks to see if a *specific* move by general would put it
        in check or not.


        Parameters:
           opposing_color (string)
            move_to (tuple)

        Returns:
            (bool) move safe or not
        """
        check_zone = []

        for row in self._board.values():
            for item in row.values():
                if item is not None and item.get_color() == opposing_color:
                    for location in item.get_movement_range():
                        check_zone.append(location)

        if move_to in check_zone:
            return False
        else:
            return True

    def get_checkmate_status(self):
        """
        Returns checkmate status of the current board
        """
        return self._checkmate

    def get_general_check_status(self, general_color):
        """
        Checks to see if a player's general is in check by
        scanning the board for the opponent's pieces and
        seeing if they are in range of the general.


        Parameters:
            general_color (string)

        Returns:
            (bool) move successful or not
        """
        general_location = self._general_locations[general_color]

        if general_color == 'BLUE':
            enemy_color = 'RED'
        else:
            enemy_color = 'BLUE'

        # scans the game board for opponent pieces and
        # checks if they could theoretically take the general
        for row in self._board.values():
            for item in row.values():
                if item is not None and item.get_color() != general_color:
                    for potential_move in item.get_movement_range():
                        if potential_move == general_location \
                                and self.pass_legality_check(potential_move, item, enemy_color, True):
                            return True

        return False

    def update_checkmate_status(self):
        """
        Updates the checkmate status of the board if the right
        conditions have been met. Sees if each general is able
        to move or not by calling is_general_stuck, and if they
        are not able to move, sees if there is a friendly piece
        that is able to break the check by calling can_friendly_break_check
        method.
        """

        red_general_location = self._general_locations['RED']
        red_general = self.get_location_contents(red_general_location)

        blue_general_location = self._general_locations['BLUE']
        blue_general = self.get_location_contents(blue_general_location)

        if self.is_general_stuck(red_general, 'BLUE') and not self.can_friendly_break_check(red_general):
            self._checkmate = True
        if self.is_general_stuck(blue_general, 'RED') and not self.can_friendly_break_check(blue_general):
            self._checkmate = True

    def can_friendly_break_check(self, general):
        """
        Searches the board for friendly pieces that can break
        the general out of a check by making a move. Does this
        by scanning the game board for friendly pieces, checking
        their legal moves, then passing each legal move into the
        method test_save_general_movement which will test the movement,
        assess if the check status changed, then restore the board back
        to its original state.


        Parameters:
            general (BoardPiece object)

        Returns:
            (bool) if the general can be broken out of check by another piece
            or not
        """
        general_color = general.get_color()
        general_location = general.get_current_pos()

        for row in self._board.values():
            for item in row.values():
                if item != general:
                    if item is not None and item.get_color() == general_color:
                        for potential_move in item.get_movement_range():

                            if potential_move != general_location \
                                    and self.pass_legality_check(potential_move, item, general_color, True):

                                if self.test_save_general_movement(item, potential_move, general_color):
                                    return True
        return False

    def test_save_general_movement(self, friendly_piece, save_general_move, general_color):
        """
        Tests if a given move will take the general out
        of check. Performs the potential movement by mutating the actual
        game board, then runs a general_status_check, then restores the
        board back to original state.


        Parameters:
            friendly_piece : piece object
            save_general_move : tuple coordinates
            general_color : string representing current turn

        Returns:
            (bool) if the move will break the check or not
        """
        save_item = self.get_location_contents(save_general_move)
        original_location = friendly_piece.get_current_pos()

        self._board[save_general_move[0]][save_general_move[1]] = friendly_piece
        self._board[original_location[0]][original_location[1]] = None

        general_still_checked = self.get_general_check_status(general_color)

        self._board[save_general_move[0]][save_general_move[1]] = save_item
        self._board[original_location[0]][original_location[1]] = friendly_piece

        if general_still_checked:
            return False
        else:
            return True

    def pieces_in_orthogonal_path(self, move_from, move_to, searching_for="ANY"):
        """
        If no argument is supplied in searching_for parameter,
        will return the number of pieces in the path between
        move_from and move_to. Primarily used for Cannons and
        Chariots. If a string is supplied indicating a type of
        piece, the method will return whether or not that piece
        is in the path. This is mainly used to prevent cannons
        from jumping other cannons.

        Parameters:
            move_from : tuple coordinates
            move_to : tuple coordinates
            searching_for : when supplied this argument will
            change the method so that it returns a bool indicating
            if a specific type of piece is in the path.

        Returns:
            (int) : number of pieces in path
            (bool) : specified piece type is in path
        """
        found = []
        if move_from[0] == move_to[0]:
            from_index = self._alphabet.index(move_from[1])
            to_index = self._alphabet.index(move_to[1])
            if move_from[1] < move_to[1]:
                for column in self._alphabet[from_index + 1: to_index:]:
                    if self.get_location_contents((move_from[0], column)) is not None:
                        found.append(self.get_location_contents((move_from[0], column)).get_name())
            if move_from[1] > move_to[1]:
                for column in self._alphabet[from_index - 1: to_index:-1]:
                    if self.get_location_contents((move_from[0], column)) is not None:
                        found.append(self.get_location_contents((move_from[0], column)).get_name())

        elif move_from[1] == move_to[1]:
            from_index = move_from[0]
            to_index = move_to[0]
            if from_index > to_index:
                for row in range(from_index - 1, to_index, -1):
                    if self.get_location_contents((row, move_from[1])) is not None:
                        found.append(self.get_location_contents((row, move_from[1])).get_name())
            if from_index < to_index:
                for row in range(from_index + 1, to_index, 1):
                    if self.get_location_contents((row, move_from[1])) is not None:
                        found.append(self.get_location_contents((row, move_from[1])).get_name())

        elif move_from[1] == 'd' or move_from[1] == 'f':
            if move_from[0] <= 3:
                if self.get_location_contents((2, 'e')) is not None:
                    found.append(self.get_location_contents((2, 'e')).get_name())
            else:
                if self.get_location_contents((9, 'e')) is not None:
                    found.append(self.get_location_contents((9, 'e')).get_name())

        if searching_for == 'ANY':
            return len(found)
        else:
            for item_found in found:
                if "CANNON" in item_found:
                    return True

    def is_elephant_path_blocked(self, elephant, move_to):
        """
        Determines if an elephant is blocked along its path to a specified
        move point.


        Parameters:
            elephant (BoardPiece object)
            move_to (tuple): coordinates

        Returns:
            (bool) blocked or not
        """
        move_from = elephant.get_current_pos()
        items_found = []

        move_from_column_index = self._alphabet.index(move_from[1])
        move_to_column_index = self._alphabet.index(move_to[1])

        north_south = move_to[0] - move_from[0]
        east_west = move_to_column_index - move_from_column_index

        if abs(north_south) == 3:
            if north_south > 0:
                items_found.append(self.get_location_contents((move_from[0] + 1, move_from[1])))
                if east_west > 0:
                    items_found.append(self.get_location_contents((move_from[0] + 2,
                                                                   self._alphabet[move_from_column_index + 1])))
                else:
                    items_found.append(self.get_location_contents((move_from[0] + 2,
                                                                   self._alphabet[move_from_column_index - 1])))
            else:
                items_found.append(self.get_location_contents((move_from[0] - 1, move_from[1])))
                if east_west > 0:
                    items_found.append(self.get_location_contents((move_from[0] - 2,
                                                                   self._alphabet[move_from_column_index + 1])))
                else:
                    items_found.append(self.get_location_contents((move_from[0] - 2,
                                                                   self._alphabet[move_from_column_index - 1])))

        else:
            if east_west > 0:
                items_found.append(self.get_location_contents((move_from[0],
                                                               self._alphabet[move_from_column_index + 1])))
                if north_south > 0:
                    items_found.append(self.get_location_contents((move_from[0] + 1,
                                                                   self._alphabet[move_from_column_index + 2])))
                else:
                    items_found.append(self.get_location_contents((move_from[0] - 1,
                                                                   self._alphabet[move_from_column_index + 2])))
            else:
                items_found.append(self.get_location_contents((move_from[0],
                                                               self._alphabet[move_from_column_index - 1])))
                if north_south > 0:
                    items_found.append(self.get_location_contents((move_from[0] + 1,
                                                                   self._alphabet[move_from_column_index - 2])))
                else:
                    items_found.append(self.get_location_contents((move_from[0] - 1,
                                                                   self._alphabet[move_from_column_index - 2])))

        for item in items_found:
            if item is not None:
                return True
        return False

    def is_horse_path_blocked(self, horse, move_to):
        """
        Determines if a horse is blocked along its path to a specified
        move point.


        Parameters:
            horse (BoardPiece object)
            move_to (tuple): coordinates

        Returns:
            (bool) blocked or not
        """
        move_from = horse.get_current_pos()

        move_from_column_index = self._alphabet.index(move_from[1])
        move_to_column_index = self._alphabet.index(move_to[1])

        north_south = move_to[0] - move_from[0]
        east_west = move_to_column_index - move_from_column_index

        if abs(north_south) == 2:
            if north_south > 0:
                item_found = self.get_location_contents((move_from[0] + 1, move_from[1]))
            else:
                item_found = self.get_location_contents((move_from[0] - 1, move_from[1]))
        else:
            if east_west > 0:
                item_found = self.get_location_contents((move_from[0], self._alphabet[move_from_column_index + 1]))
            else:
                item_found = self.get_location_contents((move_from[0], self._alphabet[move_from_column_index - 1]))

        if item_found is None:
            return False
        else:
            return True

    @staticmethod
    def parse_coordinate(string_location):
        """
        Takes a string in the format "a1"
        and returns a tuple in the form
        (1, "a")

        Parameters:
            string_location (string)

        Returns:
            row, column (tuple)
        """
        column = string_location[0]
        row = int(string_location[1:])
        return row, column

    @staticmethod
    def pieces_generator():
        """
        Rolls out the pieces in their correct order on the board by creating each
        object one by one
        """
        pieces = [Chariot('RED', 1, 'a'), Elephant('RED', 1, 'b'), Horse('RED', 1, 'c'), Guard('RED', 1, 'd'), None,
                  Guard('RED', 1, 'f'), Elephant('RED', 1, 'g'), Horse('RED', 1, 'h'), Chariot('RED', 1, 'i'),
                  None, None, None, None, General('RED', 2, 'e'), None, None, None, None,
                  None, Cannon('RED', 3, 'b'), None, None, None, None, None, Cannon('RED', 3, 'h'), None,
                  Soldier('RED', 4, 'a'), None, Soldier('RED', 4, 'c'), None, Soldier('RED', 4, 'e'), None,
                  Soldier('RED', 4, 'g'), None, Soldier('RED', 4, 'i'), None, None, None, None, None, None, None, None,
                  None, None, None, None, None, None, None, None, None, None, Soldier('BLUE', 7, 'a'), None,
                  Soldier('BLUE', 7, 'c'), None, Soldier('BLUE', 7, 'e'), None, Soldier('BLUE', 7, 'g'), None,
                  Soldier('BLUE', 7, 'i'), None, Cannon('BLUE', 8, 'b'), None, None, None, None, None,
                  Cannon('BLUE', 8, 'h'), None, None, None, None, None, General('BLUE', 9, 'e'), None, None, None, None,
                  Chariot('BLUE', 10, 'a'), Elephant('BLUE', 10, 'b'), Horse('BLUE', 10, 'c'), Guard('BLUE', 10, 'd'),
                  None, Guard('BLUE', 10, 'f'), Elephant('BLUE', 10, 'g'), Horse('BLUE', 10, 'h'),
                  Chariot('BLUE', 10, 'i'),
                  ]

        while len(pieces) > 0:
            yield pieces.pop(0)