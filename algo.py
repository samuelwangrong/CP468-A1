# algo.py
# This file contains various AI algorithms for Tic-Tac-Toe,
# including Minimax, Alpha-Beta Pruning, Expectiminimax, and Gemini LLM integration.

import math
import os
import re
import google.generativeai as genai
from game import GameCore

class AIAgent:
    """
    A static class containing methods for different AI strategies to play Tic-Tac-Toe.
    """

    @staticmethod
    def minimax(board, depth, is_maximizing, player):
        """
        The Minimax algorithm implementation for Tic-Tac-Toe.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            depth (int): The current depth of the recursion tree.
            is_maximizing (bool): True if the current player is the maximizing player (AI),
                                  False if it's the minimizing player (opponent).
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            int: The score of the current board state.
        """
        opponent = 'O' if player == 'X' else 'X'
        winner = GameCore.check_winner(board)

        if winner == player:
            return 10 - depth
        if winner == opponent:
            return depth - 10
        if winner == 'Draw':
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = player
                        score = AIAgent.minimax(board, depth + 1, False, player)
                        board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = opponent
                        score = AIAgent.minimax(board, depth + 1, True, player)
                        board[i][j] = None
                        best_score = min(score, best_score)
            return best_score

    @staticmethod
    def alpha_beta(board, depth, alpha, beta, is_maximizing, player):
        """
        The Alpha-Beta Pruning algorithm implementation for Tic-Tac-Toe.
        An optimized version of Minimax that prunes branches that cannot
        possibly influence the final decision.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            depth (int): The current depth of the recursion tree.
            alpha (float): The best value that the maximizer currently can guarantee at this level or above.
            beta (float): The best value that the minimizer currently can guarantee at this level or above.
            is_maximizing (bool): True if the current player is the maximizing player (AI),
                                  False if it's the minimizing player (opponent).
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            int: The score of the current board state.
        """
        opponent = 'O' if player == 'X' else 'X'
        winner = GameCore.check_winner(board)

        if winner == player:
            return 10 - depth
        if winner == opponent:
            return depth - 10
        if winner == 'Draw':
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = player
                        score = AIAgent.alpha_beta(board, depth + 1, alpha, beta, False, player)
                        board[i][j] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = opponent
                        score = AIAgent.alpha_beta(board, depth + 1, alpha, beta, True, player)
                        board[i][j] = None
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return best_score

    @staticmethod
    def expectiminimax(board, depth, is_maximizing, player):
        """
        The Expectiminimax algorithm implementation for Tic-Tac-Toe.
        This algorithm considers the probability of opponent's moves being random
        or optimal. Here, it uses a weighted average of optimal and random moves.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            depth (int): The current depth of the recursion tree.
            is_maximizing (bool): True if the current player is the maximizing player (AI),
                                  False if it's the minimizing player (opponent).
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            int: The expected score of the current board state.
        """
        opponent = 'O' if player == 'X' else 'X'
        winner = GameCore.check_winner(board)

        if winner == player:
            return 10 - depth
        if winner == opponent:
            return depth - 10
        if winner == 'Draw':
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = player
                        score = AIAgent.expectiminimax(board, depth + 1, False, player)
                        board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            available_moves = GameCore.get_available_moves(board)
            if not available_moves:
                return 0

            optimal_score = math.inf
            for i, j in available_moves:
                board[i][j] = opponent
                score = AIAgent.expectiminimax(board, depth + 1, True, player)
                board[i][j] = None
                optimal_score = min(score, optimal_score)

            total_random_score = 0
            for i, j in available_moves:
                board[i][j] = opponent
                score = AIAgent.expectiminimax(board, depth + 1, True, player)
                board[i][j] = None
                total_random_score += score

            average_random_score = total_random_score / len(available_moves)

            return 0.8 * optimal_score + 0.2 * average_random_score

    @staticmethod
    def get_minimax_move(board, player):
        """
        Determines the best move for the AI using the Minimax algorithm.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            list: A [row, col] pair representing the best move.
        """
        best_move = [-1, -1]
        best_score = -math.inf

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = player
                    score = AIAgent.minimax(board, 0, False, player)
                    board[i][j] = None

                    if score > best_score:
                        best_score = score
                        best_move = [i, j]
        return best_move

    @staticmethod
    def get_alpha_beta_move(board, player):
        """
        Determines the best move for the AI using the Alpha-Beta Pruning algorithm.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            list: A [row, col] pair representing the best move.
        """
        best_move = [-1, -1]
        best_score = -math.inf

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = player
                    score = AIAgent.alpha_beta(board, 0, -math.inf, math.inf, False, player)
                    board[i][j] = None

                    if score > best_score:
                        best_score = score
                        best_move = [i, j]
        return best_move

    @staticmethod
    def get_expectiminimax_move(board, player):
        """
        Determines the best move for the AI using the Expectiminimax algorithm.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            list: A [row, col] pair representing the best move.
        """
        best_move = [-1, -1]
        best_score = -math.inf

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = player
                    score = AIAgent.expectiminimax(board, 0, False, player)
                    board[i][j] = None

                    if score > best_score:
                        best_score = score
                        best_move = [i, j]
        return best_move

    @staticmethod
    def get_gemini_move(board, player):
        """
        Determines the next move for the AI by querying the Gemini LLM.
        Includes fallback to Minimax if the API call fails or returns an invalid response.
        Args:
            board (list of list): The current 3x3 Tic-Tac-Toe board.
            player (str): The symbol of the AI player ('X' or 'O').
        Returns:
            list: A [row, col] pair representing the move suggested by Gemini,
                  or by Minimax if Gemini fails.
        """
        try:
            gemini_api_key = ("AIzaSyCj2sw3gjHNM9ZqstMc-4H_x4JkNxSqZ14")
            genai.configure(api_key=gemini_api_key)

            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            board_str_list = []
            for r_idx, row in enumerate(board):
                row_cells = []
                for c_idx, cell in enumerate(row):
                    if cell is None:
                        row_cells.append(f"({r_idx},{c_idx})")
                    else:
                        row_cells.append(cell)
                board_str_list.append(" | ".join(row_cells))
            board_str = "\n".join(board_str_list)

            prompt = f"""You are playing Tic-Tac-Toe. You are player {player}.

Current board state:
{board_str}

Rules:
- You are {player}
- Choose the best move to win or block opponent
- Return ONLY the coordinates as [row,col] where row and col are 0, 1, or 2
- Example response: [1,2]

Your move:"""

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=50,
                    temperature=0.1
                )
            )

            content = response.text.strip()

            match = re.search(r'\[(\d),(\d)\]', content)
            if match:
                row = int(match.group(1))
                col = int(match.group(2))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] is None:
                    return [row, col]

            print(f"Gemini API failed or returned invalid response, falling back to Minimax. Response: '{content}'")
            return AIAgent.get_minimax_move(board, player)

        except ValueError as e:
            print(f"Configuration error: {e}, falling back to Minimax.")
            return AIAgent.get_minimax_move(board, player)
        except Exception as e:
            print(f"An unexpected error occurred with Gemini API: {e}, falling back to Minimax.")
            return AIAgent.get_minimax_move(board, player)