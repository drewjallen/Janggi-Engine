from Board import JanggiBoard


class JanggiGame:
    """
    A class to represent an instance of a Janggi game. Responsible for
    knowing current status of the game: who's turn it is, if someone is
    in check, if someone has won, and interacting with the game board.
    Details of implementing moves and tracking rules of each piece are
    abstracted down into the JanggiBoard and BoardPiece classes. Janggi
    game will contain a JanggiBoard object and will only be responsible
    for interacting with that object and tracking status.

    Attributes:
        _current_board : an instance of a JanggiBoard object which will
                         store all of the board pieces
        _game_state :  depending on the game state is 'UNFINISHED' or 'RED_WON'
                       or 'BLUE_WON'
       _current_turn : tracking who's turn it is which helps establish legality
                        of a move.

       _is_in_check : a dictionary holding the current check status of each player.
    """

    def __init__(self):
        """
        Initializes game board by creating a JanggiBoard object, and
        initializes _game_state to represent unfinished.
        """
        self._current_board = JanggiBoard()
        self._game_state = 'UNFINISHED'
        self._current_turn = 'BLUE'
        self._is_in_check = {'BLUE': False, 'RED': False}

    def display_board(self):
        """
        Calls the print_board method of the board object
        to print a visual representation of the board
        to the console.
        :return:
        """
        self._current_board.print_board()

    def get_game_state(self):
        """
        returns either 'UNFINISHED' or 'RED_WON' or 'BLUE_WON depending
        on the current state of the game.

        Returns:
            _game_state (string) : depending on the game state is 'UNFINISHED' or 'RED_WON'
                    or 'BLUE_WON'
          """
        return self._game_state

    def checkmate(self, loser):
        """
        This method is called by update_check_status to declare
        a winner. It assigns the proper string declaring which
        team won to the _game_state field.

        Parameters:
            loser (string): a string representing which player is now in checkmate and has lost
        """
        if loser == 'RED':
            self._game_state = 'BLUE_WON'
        else:
            self._game_state = 'RED_WON'

    def is_in_check(self, player):
        """
          Retrieves the check status of the given player.

          Parameters:
              player (string): 'red' or 'blue'

          Returns:
              in_check (bool): True or False depending on if the player is in check
          """
        return self._is_in_check[player.upper()]

    def make_move(self, move_from, move_to):
        """
          First performs input validation, making sure that the entered
          positions are valid algebraic notation coordinates.

          Then will call a method to parse the string representation
          of the coordinates and turn into the tuple representation
          required by this program.

          Then passes the tuples into the
          move method in the game board object so
          that JanggiGame class doesn't have to worry about
          implementation of moving a piece and checking legality
          of moves.

          If a move is successfully made, change_turn() and
          update_check_status() will be called to change turns
          and see if either player is now in check or checkmate.

          Parameters:
              move_from (string) : piece to be moved
              move_to (string) : destination for piece

          Returns:
              move_made (bool) : if move was successful or not
          """

        print("Attempting: ", move_from, "->", move_to)

        # input validation
        if move_from[0].lower() not in "abcdefghi" or move_to[0].lower() not in "abcdefghi":
            return False
        if len(move_from) < 2 or len(move_to) < 2:
            return False
        elif len(move_from) == 3:
            if move_from[1] != '1' or move_from[2] != '0':
                return False
        elif len(move_to) == 3:
            if move_to[1] != '1' or move_to[2] != '0':
                return False

        # if the game is declared over but user tries to make a move
        if self.get_game_state() != 'UNFINISHED':
            return False

        # this allows user to 'pass' a turn so long as their general is not
        # in check
        if move_from == move_to and self.is_in_check(self._current_turn) is False:
            self.change_turn()
            print("Move passed")
            return True

        # retrieve the parsed coordinates to make desired moves
        parsed_move_from = self._current_board.parse_coordinate(move_from)
        parsed_move_to = self._current_board.parse_coordinate(move_to)

        move_made = self._current_board.move_piece(parsed_move_from, parsed_move_to, self._current_turn)
        if move_made:
            self.change_turn()
            self.update_check_status()
            print("Move completed")
        return move_made

    def get_current_turn(self):
        """
         Returns which player's turn it currently is

         Returns:
             current_turn
        """
        return self._current_turn

    def change_turn(self):
        """
         Changes the value of _current_turn from RED to BLUE
         or BLUE to RED
        """
        if self._current_turn == 'BLUE':
            self._current_turn = 'RED'
        else:
            self._current_turn = 'BLUE'

    def update_check_status(self):

        """
        Calls the board object's get_general_check_status on each player
        to see if either is in check. If they are, the JanggiGame's
        _is_in_check field is updated.

        Also calls board object's update_checkmate_status to see if a
        checkmate has been achieved.
        """

        if self._current_board.get_general_check_status('RED') is True:
            self._is_in_check['RED'] = True
            self._is_in_check['BLUE'] = False
            self._current_board.update_checkmate_status()

            game_over = self._current_board.get_checkmate_status()
            if game_over:
                self.checkmate('RED')

        elif self._current_board.get_general_check_status('BLUE') is True:
            self._is_in_check['RED'] = False
            self._is_in_check['BLUE'] = True
            self._current_board.update_checkmate_status()

            game_over = self._current_board.get_checkmate_status()
            if game_over:
                self.checkmate('BLUE')

        else:
            self._is_in_check['RED'] = False
            self._is_in_check['BLUE'] = False
