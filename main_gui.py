# main_gui.py
# This file sets up the Tkinter graphical user interface for the Tic-Tac-Toe game,
# integrating the game logic and AI algorithms.

import tkinter as tk
from tkinter import messagebox, ttk
from game import GameCore
from algo import AIAgent

class TicTacToeGUI:
    """
    The GUI class for the Tic-Tac-Toe game using Tkinter.
    Manages the visual representation of the game, user interactions,
    and integrates with the game logic and AI agents.
    """
    def __init__(self, master):
        """
        Initializes the Tic-Tac-Toe GUI.
        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("AI Tic-Tac-Toe")
        master.geometry("400x550")
        master.resizable(False, False)

        self.game_state = GameCore()
        self.buttons = []

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#FDFDFD')
        self.style.configure('TLabel', background='#FDFDFD', foreground='#242426', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 14, 'bold'), borderwidth=0)
        self.style.configure('TCombobox', font=('Helvetica', 12))

        self.main_frame = ttk.Frame(master, padding="15", style='TFrame')
        self.main_frame.pack(expand=True, fill='both')

        self.title_label = tk.Label(self.main_frame, text="AI Tic-Tac-Toe", font=('Helvetica', 24, 'bold'), bg='#FDFDFD', fg='#242426')
        self.title_label.pack(pady=10)

        self.player_selection_frame = ttk.Frame(self.main_frame, padding="5", style='TFrame')
        self.player_selection_frame.pack(pady=10, fill='x')

        tk.Label(self.player_selection_frame, text="Player X:", font=('Helvetica', 12), bg='#FDFDFD', fg='#0066FF').grid(row=0, column=0, padx=5, pady=2)
        self.player_x_agent = tk.StringVar(value=self.game_state.players['X'])
        self.player_x_dropdown = ttk.Combobox(self.player_selection_frame, textvariable=self.player_x_agent,
                                               values=['Human', 'Minimax', 'Alpha-Beta', 'Expectiminimax', 'Gemini LLM'],
                                               state='readonly', font=('Helvetica', 10))
        self.player_x_dropdown.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.player_x_dropdown.bind("<<ComboboxSelected>>", lambda event: self.handle_player_change('X', self.player_x_agent.get()))

        tk.Label(self.player_selection_frame, text="Player O:", font=('Helvetica', 12), bg='#FDFDFD', fg='#FF7F00').grid(row=1, column=0, padx=5, pady=2)
        self.player_o_agent = tk.StringVar(value=self.game_state.players['O'])
        self.player_o_dropdown = ttk.Combobox(self.player_selection_frame, textvariable=self.player_o_agent,
                                               values=['Human', 'Minimax', 'Alpha-Beta', 'Expectiminimax', 'Gemini LLM'],
                                               state='readonly', font=('Helvetica', 10))
        self.player_o_dropdown.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.player_o_dropdown.bind("<<ComboboxSelected>>", lambda event: self.handle_player_change('O', self.player_o_agent.get()))

        self.player_selection_frame.grid_columnconfigure(1, weight=1)

        self.start_reset_button = ttk.Button(self.main_frame, text="Start Game", command=self.initialize_game)
        self.start_reset_button.pack(pady=10)

        self.status_message = tk.StringVar()
        self.status_message.set("Select players and start the game")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_message, font=('Helvetica', 12), bg='#FDFDFD', fg='#242426')
        self.status_label.pack(pady=5)

        self.board_frame = ttk.Frame(self.main_frame, width=300, height=300, relief="raised", borderwidth=1, padding="5", style='TFrame')
        self.board_frame.pack(pady=10, padx=10)
        self.board_frame.grid_propagate(False)

        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
            for j in range(3):
                button = tk.Button(self.board_frame, text="", font=('Helvetica', 32, 'bold'),
                                   width=4, height=2,
                                   command=lambda r=i, c=j: self.handle_cell_click(r, c),
                                   bg='#FFFFFF', fg='#242426', relief="raised", bd=1)
                button.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                self.buttons.append(button)

        self.info_message = tk.StringVar()
        self.info_message.set(f"X: {self.game_state.players['X']} | O: {self.game_state.players['O']}")
        self.info_label = tk.Label(self.main_frame, textvariable=self.info_message, font=('Helvetica', 9), bg='#FDFDFD', fg='#242426')
        self.info_label.pack(pady=5)

        self.update_board_gui()

    def update_board_gui(self):
        """
        Updates the visual representation of the game board and status messages.
        """
        for idx, button in enumerate(self.buttons):
            row, col = divmod(idx, 3)
            cell_value = self.game_state.board[row][col]
            button.config(text=cell_value if cell_value else "",
                          fg='#0066FF' if cell_value == 'X' else '#FF7F00',
                          bg='#FFFFFF')

            is_winning_cell = False
            if self.game_state.winning_line:
                for r, c in self.game_state.winning_line:
                    if r == row and c == col:
                        is_winning_cell = True
                        break

            if is_winning_cell:
                button.config(bg='#C7E5CD')

            # Disable buttons based on game state and current player
            if not self.game_state.game_active or cell_value is not None or \
               self.game_state.players[self.game_state.current_player] != 'Human':
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.NORMAL)

        self.start_reset_button.config(text="Reset Game" if self.game_state.game_active else "Start Game")
        self.player_x_dropdown.config(state=tk.DISABLED if self.game_state.game_active else 'readonly')
        self.player_o_dropdown.config(state=tk.DISABLED if self.game_state.game_active else 'readonly')

        self.info_message.set(f"X: {self.game_state.players['X']} | O: {self.game_state.players['O']}")
        if self.game_state.game_active:
            self.info_message.set(f"X: {self.game_state.players['X']} | O: {self.game_state.players['O']} | Turn: {self.game_state.current_player}")

        self.master.update_idletasks()

    def initialize_game(self):
        """
        Initializes a new game.
        """
        self.game_state.initialize_game()
        self.status_message.set("Game started! Player X's turn")
        self.update_board_gui()
        self.master.after(100, self.handle_turn) # Start the first turn with a slight delay

    def handle_player_change(self, player, agent):
        """
        Handles changes in player agent selection.
        Args:
            player (str): The player symbol ('X' or 'O').
            agent (str): The selected agent type.
        """
        self.game_state.set_player_agent(player, agent)
        self.info_message.set(f"X: {self.game_state.players['X']} | O: {self.game_state.players['O']}")
        self.status_message.set("Select players and start the game")

    def handle_cell_click(self, row, col):
        """
        Handles a click on a Tic-Tac-Toe board cell.
        Args:
            row (int): The row index of the clicked cell.
            col (int): The column index of the clicked cell.
        """
        if not self.game_state.game_active or self.game_state.board[row][col] is not None or \
           self.game_state.players[self.game_state.current_player] != 'Human':
            return

        self.game_state.make_move(row, col, self.game_state.current_player)
        self.update_board_gui()
        self.check_game_end_or_next_turn()

    def check_game_end_or_next_turn(self):
        """
        Checks if the game has ended (win or draw) or proceeds to the next turn.
        """
        if self.game_state.winner:
            if self.game_state.winner == 'Draw':
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.status_message.set("Game Over: Draw!")
            else:
                messagebox.showinfo("Game Over", f"Player {self.game_state.winner} wins!")
                self.status_message.set(f"Game Over: Player {self.game_state.winner} wins!")
            self.game_state.game_active = False # Ensure game state is set to inactive
            self.update_board_gui()
        elif self.game_state.game_active:
            self.master.after(500, self.handle_turn) # Introduce a slight delay before the next turn

    def handle_turn(self):
        """
        Manages the current player's turn, including AI moves.
        """
        if not self.game_state.game_active or self.game_state.winner:
            self.update_board_gui() # Ensure buttons are disabled if game is over
            return

        current_agent = self.game_state.players[self.game_state.current_player]

        if current_agent != 'Human':
            self.status_message.set(f"Player {self.game_state.current_player} ({current_agent}) is thinking...")
            self.update_board_gui() # Update GUI to show AI thinking state and disable buttons

            board_copy = [row[:] for row in self.game_state.board]
            row, col = None, None

            if current_agent == 'Minimax':
                row, col = AIAgent.get_minimax_move(board_copy, self.game_state.current_player)
            elif current_agent == 'Alpha-Beta':
                row, col = AIAgent.get_alpha_beta_move(board_copy, self.game_state.current_player)
            elif current_agent == 'Expectiminimax':
                row, col = AIAgent.get_expectiminimax_move(board_copy, self.game_state.current_player)
            elif current_agent == 'Gemini LLM':
                row, col = AIAgent.get_gemini_move(board_copy, self.game_state.current_player)
            else:
                row, col = AIAgent.get_minimax_move(board_copy, self.game_state.current_player)

            if row is not None and col is not None:
                self.game_state.make_move(row, col, self.game_state.current_player)
            else:
                messagebox.showerror("AI Error", "AI failed to make a valid move. Falling back to next turn.")
                # If AI fails, still need to advance turn or handle error gracefully
                if self.game_state.current_player == 'X':
                    self.game_state.current_player = 'O'
                else:
                    self.game_state.current_player = 'X'

            self.update_board_gui()
            self.check_game_end_or_next_turn()
        else:
            self.status_message.set(f"Player {self.game_state.current_player}'s turn")
            self.update_board_gui() # Re-enable human player buttons

if __name__ == "__main__":
    root = tk.Tk()
    game_gui = TicTacToeGUI(root)
    root.mainloop()