# game.py
# This file contains the combined core logic and state management for the Tic-Tac-Toe game.

class GameCore:
    """
    Manages the state of a Tic-Tac-Toe game and provides methods for game rules
    and board analysis. This class combines the functionalities previously
    found in GameLogic and GameState.
    """
    def __init__(self):
        """
        Initializes the Tic-Tac-Toe game board and state variables.
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = False
        self.winner = None
        self.winning_line = None
        self.players = {'X': 'Human', 'O': 'Minimax'}

    def initialize_game(self):
        """
        Resets the game state to its initial configuration, starting a new game.
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = True
        self.winner = None
        self.winning_line = None

    def make_move(self, row, col, player):
        """
        Attempts to make a move on the board.
        Args:
            row (int): The row index (0-2).
            col (int): The column index (0-2).
            player (str): The symbol of the player making the move ('X' or 'O').
        Returns:
            bool: True if the move was successfully made, False otherwise.
        """
        if not self.game_active or self.board[row][col] is not None or self.winner:
            return False

        self.board[row][col] = player

        self.winner = GameCore.check_winner(self.board)
        self.winning_line = GameCore.get_winning_line(self.board)

        if self.winner:
            self.game_active = False
        else:
            self.current_player = 'O' if player == 'X' else 'X'
        return True

    def set_player_agent(self, player, agent):
        """
        Sets the AI agent type for a specific player ('X' or 'O').
        Args:
            player (str): The player symbol ('X' or 'O').
            agent (str): The type of agent (e.g., 'Human', 'Minimax', 'Gemini LLM').
        """
        self.players[player] = agent

    @staticmethod
    def check_winner(board):
        """
        Checks if there's a winner on the current board or if it's a draw.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
                                  Each cell can be 'X', 'O', or None.
        Returns:
            str: 'X' if X wins, 'O' if O wins, 'Draw' if it's a draw,
                 or None if the game is still ongoing.
        """
        for i in range(3):
            if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]

        for j in range(3):
            if board[0][j] and board[0][j] == board[1][j] == board[2][j]:
                return board[0][j]

        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

        if GameCore.is_board_full(board):
            return 'Draw'

        return None

    @staticmethod
    def get_winning_line(board):
        """
        Returns the coordinates of the winning line if a winner exists.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
        Returns:
            list of list: A list of [row, col] pairs representing the winning line,
                          or None if no winner.
        """
        for i in range(3):
            if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
                return [[i, 0], [i, 1], [i, 2]]

        for j in range(3):
            if board[0][j] and board[0][j] == board[1][j] == board[2][j]:
                return [[0, j], [1, j], [2, j]]

        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return [[0, 0], [1, 1], [2, 2]]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return [[0, 2], [1, 1], [2, 0]]

        return None

    @staticmethod
    def is_board_full(board):
        """
        Checks if the Tic-Tac-Toe board is completely filled.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(cell is not None for row in board for cell in row)

    @staticmethod
    def get_available_moves(board):
        """
        Gets a list of all empty cells (available moves) on the board.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
        Returns:
            list of list: A list of [row, col] pairs for available moves.
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    moves.append([i, j])
        return moves