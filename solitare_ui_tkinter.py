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
        
        # Right panel - Peg board
        right_frame = ttk.LabelFrame(main_frame, text="Peg Solitaire Board", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Standard peg solitaire board layout (7x7 with specific empty spaces)
        self.peg_buttons = []
        self.board_layout = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]
        ]
        
        # Create board buttons
        board_frame = ttk.Frame(right_frame)
        board_frame.pack(anchor=tk.CENTER)

        self.selected_position = [0, 0]
        
        # Store button references for easy access
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
                        command=lambda r=row, c=col: self.peg_clicked(r, c)
                    )
                    #if row == 3 and col == 3:
                        #btn.configure(bg="#B6B6B6",activebackground="#A7A6A6", relief=tk.FLAT)
                    self.board_buttons[(row, col)] = btn
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(btn)
                else:
                    # Create invisible placeholder for layout consistency
                    placeholder = tk.Frame(board_frame, width=4, height=2)
                    placeholder.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(None)
            
            self.peg_buttons.append(button_row)
    
    def peg_clicked(self, row, col):
        """Handle peg button clicks"""
        if self.game == None:
            pass
        else:
            valid = self.game.check_valid_moves(horizontal_index=col, vertical_index=row)
            if valid.count != 0:
                self.selected_position = [col, row]
                for button_row in self.peg_buttons:
                    for button in button_row:
                        if button != None:
                            button.configure(state=tk.DISABLED)
                for index in valid:
                    print(f"index: {index}")
                    self.board_buttons[(index[1], index[0])].configure(state=tk.ACTIVE,
                                                                        bg="#FFFFFF",
                                                                        activebackground="#B6B6B6", 
                                                                        command=lambda r=row, c=col: self.peg_destination_clicked(r, c))
    
    def peg_destination_clicked(self, row, column):
        ...

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
            print(f"Enabling {len(self.board_buttons)} buttons...")
            for btn in self.board_buttons.values():
                btn.config(state=tk.NORMAL)
            
            print("All buttons enabled successfully")
            
        except Exception as e:
            print(f"Connection failed: {e}")
        

    def reset_scores(self):
        """Reset the current score"""
        self.current_score.config(text="0")

if __name__ == "__main__":
    root = tk.Tk()
    app = solitare_ui(root)
    root.mainloop()