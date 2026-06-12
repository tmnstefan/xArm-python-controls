import tkinter as tk
from tkinter import ttk
from xml.parsers.expat import model
import numpy as np
import time
import numpy as np
import gymnasium as gym
from gymnasium.envs.registration import register
from stable_baselines3 import DQN
import os
import sv_ttk

class solitare_ui:
    def __init__(self, root):
        sv_ttk.set_theme("dark")
        self.root = root
        self.root.title("Peg Solitaire high runs camera angle 1 attempt 2")
        self.root.geometry("1800x900")
        self.game = None
        self.training = False
        self.center_pos = [254.0, -3.0, 28.0]
        
        # Create main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.center_entry = tk.Toplevel(root)
        self.center_entry.title("Set Center Position")
        self.center_entry.geometry("600x400")
        self.center_entry.attributes('-topmost', True)
        self.center_entry.lift()
        center_label = ttk.Label(self.center_entry, text="Enter Center Position (x, y, z):")
        center_label.pack(pady=10)
        self.x_entry = ttk.Entry(self.center_entry, width=30)
        self.x_entry.pack(pady=5)
        self.y_entry = ttk.Entry(self.center_entry, width=30)
        self.y_entry.pack(pady=5)
        self.z_entry = ttk.Entry(self.center_entry, width=30)
        self.z_entry.pack(pady=5)
        self.x_entry.insert(0, "254.0")
        self.y_entry.insert(0, "-3.0")
        self.z_entry.insert(0, "28.0")
        set_center_btn = ttk.Button(self.center_entry, text="Set Center Position", command=self.set_center_position)
        set_center_btn.pack(pady=10)
        self.root.wait_window(self.center_entry)

        self.ip_entry = tk.Toplevel(root)
        self.ip_entry.title("Connect to IP")
        self.ip_entry.geometry("600x400")
        self.ip_entry.attributes('-topmost', True)
        self.ip_entry.lift()
        ip_label = ttk.Label(self.ip_entry, text="IP Address:")
        ip_label.pack(pady=(0, 5))
        self.ip_enter = ttk.Entry(self.ip_entry, width=30)
        self.ip_enter.pack(pady=(0, 20))
        self.ip_enter.insert(0, "127.0.0.1")
        connect_btn = ttk.Button(self.ip_entry, text="Connect", command=self.connect_to_ip)
        connect_btn.pack(pady=10)
        self.root.wait_window(self.ip_entry)

        # Left panel
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # IP Address input
        '''ip_label = ttk.Label(left_frame, text="IP Address:")
        ip_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.ip_entry = ttk.Entry(left_frame, width=30)
        self.ip_entry.pack(anchor=tk.W, pady=(0, 20))
        self.ip_entry.insert(0, "127.0.0.1")
        
        connect_btn = ttk.Button(left_frame, text="Connect", command=self.connect_to_ip)
        connect_btn.pack(anchor=tk.W, pady=(0, 20))'''
        # Current Score
        current_label = ttk.Label(left_frame, text="Current Score:", font=("Arial", 14, "bold"))
        current_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.current_score = ttk.Label(left_frame, text="0", font=("Arial", 20, "bold"))
        self.current_score.pack(anchor=tk.W, pady=(0, 15))
        
        # Session Best Score
        best_label = ttk.Label(left_frame, text="Session Best Score:", font=("Arial", 14, "bold"))
        best_label.pack(anchor=tk.W, pady=(10, 5))

        # Last score
        last_label = ttk.Label(left_frame, text="Last Score:", font=("Arial", 14, "bold"))
        last_label.pack(anchor=tk.W, pady=(10, 5))

        self.last_score = ttk.Label(left_frame, text="0", font=("Arial", 20, "bold"))
        self.last_score.pack(anchor=tk.W, pady=(0, 20))

        self.best_score = ttk.Label(left_frame, text="0", font=("Arial", 20, "bold"))
        self.best_score.pack(anchor=tk.W, pady=(0, 20))

        no_iterations_label = ttk.Label(left_frame, text="Training Iterations:", font=("Arial", 14, "bold"))
        no_iterations_label.pack(anchor=tk.W, pady=(10, 5))

        self.no_iterations = ttk.Entry(left_frame, font=("Arial", 20, "bold"))
        self.no_iterations.pack(anchor=tk.W, pady=(0, 20))
        self.no_iterations.insert(0, "10000")

        train_btn = ttk.Button(left_frame, text="Train Agent", command=self.train_agent)
        train_btn.pack(anchor=tk.W, pady=(0, 20))

        # Run on Robot button (disabled until a trained model is available)
        self.run_btn = ttk.Button(left_frame, text="Run on Robot", command=self.run_on_robot, state=tk.DISABLED)
        self.run_btn.pack(anchor=tk.W, pady=(0, 20))

        try:
            if os.path.exists("solitaire_agent.zip"):
                self.run_btn.config(state=tk.NORMAL)
        except Exception:
            pass
        
        # Reset button
        reset_btn = ttk.Button(left_frame, text="Reset", command=self.reset_scores)
        reset_btn.pack(anchor=tk.W, pady=(20, 0))
        
        # Right panel - board
        right_frame = ttk.LabelFrame(main_frame, text="Peg Solitaire Board", padding=50)
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
                        width=12,
                        height=6,
                        bg="#AD9745",
                        activebackground="#9C883E",
                        relief=tk.RAISED,
                        state=tk.NORMAL,
                        bd=2,
                        command=lambda r=row, c=col: self.button_clicked(r, c)
                    )
                    self.board_buttons[(row, col)] = btn
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(btn)
                if self.board_layout[row][col] == 0:
                    btn = tk.Button(
                        board_frame,
                        width=12,
                        height=6,
                        bg="#FFFFFF",
                        activebackground="#B6B6B6",
                        relief=tk.RAISED,
                        state=tk.NORMAL,
                        bd=2,
                        command=lambda r=row, c=col: self.button_destination_clicked(r, c)
                    )
                    self.board_buttons[(row, col)] = btn
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(btn)
                    
                else:
                    # placeholder for layout consistency
                    placeholder = tk.Frame(board_frame, width=12, height=6)
                    placeholder.grid(row=row, column=col, padx=2, pady=2)
                    button_row.append(None)
            
            self.peg_buttons.append(button_row)

    def set_center_position(self):
        """Set the center position for the game based on user input"""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            z = float(self.z_entry.get())
            self.center_pos = [x, y, z]
            print(f"Center position set to: {self.center_pos}")
            self.center_entry.destroy()
            self.root.deiconify()
        except ValueError:
            print("Invalid input for center position. Please enter numeric values.")

    def train_agent(self):
        """Train the agent using the current game state"""
        if self.game is None:
            print("Please connect to the game first.")
            return
        
        self.training = True
        # training logic
        from solitare_env_alt import solitare_rl_env
        from stable_baselines3 import DQN
        env = solitare_rl_env(ui=self, is_debug=False)

        model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0001, gamma=0.99, policy_kwargs=dict(net_arch=[512, 512]))
        try:
            iterations = int(self.no_iterations.get())
            print(f"Training for {iterations} iterations...")
        except ValueError:
            print("Invalid input for training iterations. Please enter a numeric value.")
            self.training = False
            return
        model.learn(total_timesteps=iterations, log_interval=4)
        model.save("solitaire_agent")
        model = DQN.load("solitaire_agent", env=env) # low runs camera angle 1

        obs, info = env.reset()
        #self._run_model_loop(model, env, obs)
        # mark training complete and enable Run button
        self.training = False
        try:
            self.run_btn.config(state=tk.NORMAL)
        except Exception:
            pass

    def _run_model_loop(self, model, env, obs):
        action, _ = model.predict(obs, deterministic=True)
        print(f"[MODEL LOOP] action={action}, current step moves={len(env.valid_moves)}")
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            print(f"[MODEL LOOP] episode ended, stopping robot execution")
            return
        self.root.update_idletasks()
        self.root.after(500, lambda: self._run_model_loop(model, env, obs))

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
                    #print(f"index: {index}")
                    self.board_buttons[(index[0], index[1])].configure(state=tk.NORMAL,
                                                                        bg="#BEDCFF",
                                                                        activebackground="#7CA4FC", 
                                                                        width=12,
                                                                        height=6,
                                                                        command=lambda r=index[0], c=index[1]: self.button_destination_clicked(r, c))

    def button_destination_clicked(self, row, column):
        """Handle button clicks when selecting destination for"""
        if self.game == None:
            pass
        else:
            # set positions for balls that need to be moved and move them
            captured_position = [int((row - self.selected_position[0]) / 2) + self.selected_position[0] , int((column - self.selected_position[1]) / 2) + self.selected_position[1]]
            if not self.training:
                self.game.move_ball(center_pos=self.center_pos, start_vertical=self.selected_position[0], start_horizontal=self.selected_position[1], end_vertical=row, end_horizontal=column)
                self.game.remove_captured_ball(center_pos=self.center_pos, vertical=captured_position[0], horizontal=captured_position[1])
                #print(f"\nMoved ball from {self.selected_position} to {[row, column]}, captured ball at {captured_position}\n")
                #print(f"[UI MOVE] ball_positions:\n{np.array(self.game.ball_positions)}")
                #print(f"[UI MOVE] valid moves: {self.game.check_all_valid_moves()}\n")
            # show movement on board
            if (self.selected_position[0], self.selected_position[1]) in self.board_buttons:
                self.board_buttons[(self.selected_position[0], self.selected_position[1])].configure(state=tk.DISABLED,
                                                                            width=12,
                                                                            height=6,
                                                                            bg="#FFFFFF",
                                                                            activebackground="#B6B6B6", 
                                                                            command=lambda r=self.selected_position[0], c=self.selected_position[1]: self.button_destination_clicked(r, c))
            if (captured_position[0], captured_position[1]) in self.board_buttons:
                self.board_buttons[(captured_position[0], captured_position[1])].configure(state=tk.DISABLED,
                                                                            width=12,
                                                                            height=6,
                                                                            bg="#FFFFFF",
                                                                            activebackground="#B6B6B6", 
                                                                            command=lambda r=captured_position[0], c=captured_position[1]: self.button_destination_clicked(r, c))
            if (row, column) in self.board_buttons:
                self.board_buttons[(row, column)].configure(state=tk.NORMAL,
                                                                            width=12,
                                                                            height=6,
                                                                            bg="#AD9745",
                                                                            activebackground="#9C883E", 
                                                                            command=lambda r=row, c=column: self.button_clicked(r, c))
            # change buttons that were highlighted as move options back to their regular colours
            for i in range(7):
                for j in range(7):
                    try:
                        if self.board_buttons[(i, j)].cget("bg") == "#AD9745":
                            self.board_buttons[(i, j)].configure(state=tk.NORMAL, width=12, height=6)
                        if self.board_buttons[(i, j)].cget("bg") == "#BEDCFF":
                            self.board_buttons[(i, j)].configure(state=tk.DISABLED, width=12, height=6, bg="#FFFFFF", activebackground="#B6B6B6", command=lambda r=captured_position[0], c=captured_position[1]: self.button_destination_clicked(r, c))
                    except Exception as e:
                        #print(e)
                        pass
            score_text = self.current_score.cget("text")
            try: # increment score
                score = int(score_text) + 1
                self.current_score.configure(text=f"{score}")
            except Exception as e:
                pass

    def connect_to_ip(self):
        """Connect to the specified IP address"""
        ip = self.ip_enter.get()
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
            # If a trained model exists, enable the Run button
            self.ip_entry.destroy()
            self.root.deiconify()
            
            print("All buttons enabled successfully")
            
        except Exception as e:
            print(f"Connection failed: {e}")
        

    def run_on_robot(self):
        """Load a trained model and run it on the connected robot."""
        if self.game is None:
            print("Please connect to the game first.")
            return

        # Try to load saved model
        try:
            from solitare_env import solitare_rl_env
            from stable_baselines3 import DQN

            env = solitare_rl_env(ui=self)
            # load model (expects file 'solitaire_agent.zip')
            model = DQN.load("solitaire_agent", env=env)
            obs, info = env.reset()
            # ensure training flag is off
            self.training = False
            # start model loop which will use the env to call UI/robot actions
            self._run_model_loop(model, env, obs)
        except Exception as e:
            print(f"Failed to run model on robot: {e}")

    def reset_scores(self):
        """Reset the current score"""
        
        if self.game == None:
            pass
        else:
            # move to reasonable base position and modify session best score
            if not self.training:
                self.game.simple_move(x=257, y=-4, z=200)
            try:
                current = int(self.current_score.cget("text"))
                self.last_score.configure(text=str(current))
            except Exception:
                current = 0
            try:
                best = int(self.best_score.cget("text"))
            except Exception:
                best = 0
            if current > best:
                self.best_score.configure(text=str(current))
            self.current_score.config(text="0")
            for i in range (7):
                for j in range (7):
                    # reset buttons to their initial states
                    try:
                        self.board_buttons[(i, j)].configure(
                            width=12,
                            height=6,
                            bg="#AD9745",
                            activebackground="#9C883E",
                            relief=tk.RAISED,
                            state=tk.NORMAL,
                            bd=2,
                            command=lambda r=i, c=j: self.button_clicked(r, c)
                            )
                        if i == 3 and j == 3:
                            self.board_buttons[(i, j)].configure(
                                width=12,
                                height=6,
                                bg="#FFFFFF",
                                activebackground="#B6B6B6",
                                relief=tk.RAISED,
                                state=tk.DISABLED,
                                bd=2,
                                command=lambda r=i, c=j: self.button_destination_clicked(r, c)
                            )
                    except Exception as e:
                        pass

class solitare_config:
    def __init__(self):
        self.state = 0        

if __name__ == "__main__":
    root = tk.Tk()
    app = solitare_ui(root)
    root.mainloop()