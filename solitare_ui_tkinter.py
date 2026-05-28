import tkinter as tk
from tkinter import ttk
import numpy as np
import time

class solitare_ui:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.geometry("700x600")
        self.game = None
        
        # Create main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # IP Address input
        ip_label = ttk.Label(left_frame, text="IP Address:")
        ip_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.ip_entry = ttk.Entry(left_frame, width=30)
        self.ip_entry.pack(anchor=tk.W, pady=(0, 20))
        self.ip_entry.insert(0, "127.0.0.1")
        
        connect_btn = ttk.Button(left_frame, text="Connect", command=self.connect_to_ip)
        connect_btn.pack(anchor=tk.W, pady=(0, 20))

        # Current Score
        current_label = ttk.Label(left_frame, text="Current Score:")
        current_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.current_score = ttk.Label(left_frame, text="0", font=("Arial", 14, "bold"))
        self.current_score.pack(anchor=tk.W, pady=(0, 15))
        
        # Session Best Score
        best_label = ttk.Label(left_frame, text="Session Best Score:")
        best_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.best_score = ttk.Label(left_frame, text="0", font=("Arial", 14, "bold"))
        self.best_score.pack(anchor=tk.W, pady=(0, 20))
        
        # Reset button
        reset_btn = ttk.Button(left_frame, text="Reset", command=self.reset_scores)
        reset_btn.pack(anchor=tk.W, pady=(20, 0))
        
        # Right panel - board
        right_frame = ttk.LabelFrame(main_frame, text="Peg Solitaire Board", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # board layout
        self.peg_buttons = []
        self.board_layout = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1]
        ]
        
        # board buttons
        board_frame = ttk.Frame(right_frame)
        board_frame.pack(anchor=tk.CENTER)

        self.selected_position = [0, 0]
        
        # Store button references
        self.board_buttons = {}

        for row in range(7):
            button_row = []
            for col in range(7):
                if self.board_layout[row][col] == 1:
                    btn = tk.Button(
                        board_frame,
                        width=4,
                        height=2,
                        bg="#AD9745",
                        activebackground="#9C883E",
                        relief=tk.RAISED,
                        state=tk.DISABLED,
                        bd=2,
                        command=lambda r=row, c=col: self.button_clicked(r, c)
                    )
                    self.board_buttons[(row, col)] = btn
                    btn.grid(row=row, column=col, padx=2, pady=2, sticky="NSEW")
                    button_row.append(btn)
                if self.board_layout[row][col] == 0:
                    btn = tk.Button(
                        board_frame,
                        width=4,
                        height=2,
                        bg="#FFFFFF",
                        activebackground="#B6B6B6",
                        relief=tk.RAISED,
                        state=tk.DISABLED,
                        bd=2,
                        command=lambda r=row, c=col: self.button_destination_clicked(r, c)
                    )
                    self.board_buttons[(row, col)] = btn
                    btn.grid(row=row, column=col, padx=2, pady=2, sticky="NSEW")
                    button_row.append(btn)
                    
                else:
                    # placeholder for layout consistency
                    placeholder = tk.Frame(board_frame, width=4, height=2)
                    placeholder.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(None)
            
            self.peg_buttons.append(button_row)
    
    def button_clicked(self, row, col):
        """Handle button clicks"""
        self.selected_position = [row, col]
        if self.game == None:
            pass
        else:
            # check for if any valid moves exist, if so highlight buttons corresponding to moves
            valid = self.game.check_valid_moves(horizontal_index=col, vertical_index=row)
            if len(valid) != 0:
                self.selected_position = [row, col]
                for button_row in self.peg_buttons:
                    for button in button_row:
                        if button != None:
                            button.configure(state=tk.DISABLED)
                for index in valid:
                    print(f"index: {index}")
                    self.board_buttons[(index[0], index[1])].configure(state=tk.NORMAL,
                                                                        bg="#BEDCFF",
                                                                        activebackground="#7CA4FC", 
                                                                        command=lambda r=index[0], c=index[1]: self.button_destination_clicked(r, c))
    
    def button_destination_clicked(self, row, column):
        """Handle button clicks when selecting destination for"""
        if self.game == None:
            pass
        else:
            # set positions for balls that need to be moved and move them
            captured_position = [int((row - self.selected_position[0]) / 2) + self.selected_position[0] , int((column - self.selected_position[1]) / 2) + self.selected_position[1]]
            self.game.move_ball(center_pos=[257, -4, 28], start_vertical=self.selected_position[0], start_horizontal=self.selected_position[1], end_vertical=row, end_horizontal=column)
            self.game.remove_captured_ball(center_pos=[257, -4, 28], vertical=captured_position[0], horizontal=captured_position[1], prison_x=165, prison_y=82, prison_z=30)
            # show movement on board
            self.board_buttons[(self.selected_position[0], self.selected_position[1])].configure(state=tk.DISABLED,
                                                                        bg="#FFFFFF",
                                                                        activebackground="#B6B6B6", 
                                                                        command=lambda r=self.selected_position[0], c=self.selected_position[1]: self.button_destination_clicked(r, c))
            self.board_buttons[(captured_position[0], captured_position[1])].configure(state=tk.DISABLED,
                                                                        bg="#FFFFFF",
                                                                        activebackground="#B6B6B6", 
                                                                        command=lambda r=captured_position[0], c=captured_position[1]: self.button_destination_clicked(r, c))
            self.board_buttons[(row, column)].configure(state=tk.NORMAL,
                                                                        bg="#AD9745",
                                                                        activebackground="#9C883E", 
                                                                        command=lambda r=row, c=column: self.button_clicked(r, c))
            # change buttons that were highlighted as move options back to their regular colours
            for i in range(7):
                for j in range(7):
                    try:
                        if self.board_buttons[(i, j)].cget("bg") == "#AD9745":
                            self.board_buttons[(i, j)].configure(state=tk.NORMAL)
                        if self.board_buttons[(i, j)].cget("bg") == "#BEDCFF":
                            self.board_buttons[(i, j)].configure(state=tk.DISABLED, bg="#FFFFFF", activebackground="#B6B6B6", command=lambda r=captured_position[0], c=captured_position[1]: self.button_destination_clicked(r, c))
                    except Exception as e:
                        print(e)
            score_text = self.current_score.cget("text")
            try: # increment score
                score = int(score_text) + 1
                self.current_score.configure(text=f"{score}")
            except Exception as e:
                pass

    def connect_to_ip(self):
        """Connect to the specified IP address"""
        ip = self.ip_entry.get()
        if not ip.strip():
            print("Please enter a valid IP address")
            return
        
        try:
            from xarm.wrapper import XArmAPI
            from solitare_game import solitare
            
            # Create XArmAPI connection and Solitaire instance
            arm = XArmAPI(port=ip)
            self.game = solitare(arm=arm)
            print(f"Connected to: {ip}")
            print(f"Game instance created: {self.game}")
            
            # Enable all game buttons now that game is initialized
            for btn in self.board_buttons.values():
                btn.config(state=tk.NORMAL)
            
            print("All buttons enabled successfully")
            
        except Exception as e:
            print(f"Connection failed: {e}")
        

    def reset_scores(self):
        """Reset the current score"""
        
        if self.game == None:
            pass
        else:
            # move to reasonable base position and modify session best score
            self.game.simple_move(x=257, y=-4, z=200)
            best = self.current_score.cget("text")
            self.best_score.configure(text=best)
            self.current_score.config(text="0")
            for i in range (7):
                for j in range (7):
                    # reset buttons to their initial states
                    try:
                        self.board_buttons[(i, j)].configure(
                            width=4,
                            height=2,
                            bg="#AD9745",
                            activebackground="#9C883E",
                            relief=tk.RAISED,
                            state=tk.NORMAL,
                            bd=2,
                            command=lambda r=i, c=j: self.button_clicked(r, c)
                            )
                        if i == 3 and j == 3:
                            self.board_buttons[(i, j)].configure(
                                width=4,
                                height=2,
                                bg="#FFFFFF",
                                activebackground="#B6B6B6",
                                relief=tk.RAISED,
                                state=tk.DISABLED,
                                bd=2,
                                command=lambda r=i, c=j: self.button_destination_clicked(r, c)
                            )
                    except Exception as e:
                        pass

                    

if __name__ == "__main__":
    root = tk.Tk()
    app = solitare_ui(root)
    root.mainloop()