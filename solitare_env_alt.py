import os
import time
from collections import defaultdict
from typing import Optional, TYPE_CHECKING, cast
import numpy as np
import gymnasium as gym
import math
from gymnasium.envs.registration import register

if TYPE_CHECKING:
    from solitare_ui_tkinter import solitare_ui

class solitare_rl_env(gym.Env):

    def __init__(self, ui:'solitare_ui', is_debug=False):
        self.is_debug = is_debug
        self.ui = ui
        #self.ui.connect_to_ip()
        self.ui.reset_scores()
        self.current = 0
        self.runs = 0
        
        obs_low = np.concatenate([
            np.full((7, 7), -1).flatten(),        # board array
        ])

        obs_high = np.concatenate([
            np.full((7, 7), 1).flatten(),        # board array
        ])
        self.observation_space = gym.spaces.Box(low=obs_low, high=obs_high, dtype=np.int64)
        self.action_space = gym.spaces.Discrete(7 * 7 * 4)
        self._action_rows = 7
        self._action_cols = 7
        self._action_dirs = 4

        if self.ui.game != None:
            self.game = self.ui.game
        else:
            raise Exception ("Game not found. Please initialize the solitare_ui and pass it to the environment.")
        
        self.valid_moves = self.game.check_all_valid_moves()

    
    def _decode_action(self, action):
        """Convert a flat DQN-style action index into (row, col, direction)."""
        if isinstance(action, (tuple, list, np.ndarray)):
            action_array = np.asarray(action, dtype=np.int64)
            if action_array.shape == (3,):
                return tuple(int(x) for x in action_array)

        action_space = cast(gym.spaces.Discrete, self.action_space)
        action_index = int(np.asarray(action).item())
        if action_index < 0 or action_index >= action_space.n:
            raise ValueError(f"Action {action_index} is out of range for action space size {action_space.n}.")

        direction = action_index % self._action_dirs
        action_index //= self._action_dirs
        source_col = action_index % self._action_cols
        source_row = action_index // self._action_cols
        return source_row, source_col, direction

    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            dict: Observation with agent and target positions
        """
        return np.concatenate([
            np.array(self.game.ball_positions).flatten(),        # board array
        ])
    

    def _get_info(self):
        return {
            "score": int(self.ui.current_score.cget("text")),
            "board state": np.array(self.game.ball_positions).flatten(),
        }
        

    def reset(self, *, seed:Optional[int] = None, options:Optional[dict] = None):
        """Start a new episode.

        Args:
            seed: Random seed for reproducible episodes
            options: Additional configuration (unused in this example)

        Returns:
            tuple: (observation, info) for the initial state
        """
        # IMPORTANT: Must call this first to seed the random number generator
        super().reset(seed=seed)
        self.runs = 0
        # Randomly place the agent anywhere on the grid
        self.ui.reset_scores()
        #self.ui.connect_to_ip()
        self.game.reset_board()
        self.current = 0

        self.valid_moves = self.game.check_all_valid_moves()

        observation = self._get_obs()
        info = self._get_info()
 
        return observation, info
        
    def step(self, action):
        """Execute one timestep within the environment.

        Args:
            action: The action to take

        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        
        self.valid_moves = self.game.check_all_valid_moves()
        source_row, source_col, direction = self._decode_action(action)

        if self.is_debug:
            print(f"\n[STEP START] ball_positions:\n{np.array(self.game.ball_positions)}")
            print(f"[STEP START] valid moves: {self.valid_moves}\n")
            print(f"[STEP START] action: {action} -> decoded: ({source_row}, {source_col}, {direction})\n")
            #time.sleep(0.2)
        terminated = False
        truncated = False
        reward = 0
        #time.sleep(0.05)
        self.runs += 1

        if direction == 0:  # up
            dest_row, dest_col = source_row - 2, source_col
        elif direction == 1:  # down
            dest_row, dest_col = source_row + 2, source_col
        elif direction == 2:  # left
            dest_row, dest_col = source_row, source_col - 2
        elif direction == 3:  # right
            dest_row, dest_col = source_row, source_col + 2
        else:
            raise Exception(f"Invalid direction: {direction}")
        
        valid_destinations = self.game.check_valid_moves(horizontal_index=source_col, vertical_index=source_row)
        if len(self.valid_moves) == 0:
            terminated = True
            self.valid_moves = self.game.check_all_valid_moves()
            if int(self.ui.current_score.cget("text")) == 32:
                reward += 100
            else:
                reward -= 100
        elif self.runs >= 1000:
            terminated = True
            self.valid_moves = self.game.check_all_valid_moves()
            reward -= 32 * 32
        else:
            if (dest_row, dest_col) in valid_destinations:
                self.runs += 1
                if self.is_debug:
                    print(f"\nExecuting move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
                self.ui.button_clicked(source_row, source_col)
                self.ui.button_destination_clicked(dest_row, dest_col)
                self.game.ball_positions[source_row][source_col] = 0
                self.game.ball_positions[dest_row][dest_col] = 1
                self.game.ball_positions[(source_row + dest_row) // 2][(source_col + dest_col) // 2] = 0    
                self.ui.root.update()
                self.current = 0
                self.valid_moves = self.game.check_all_valid_moves()
                reward += 1
                #reward += int(self.ui.current_score.cget("text")) * int(self.ui.current_score.cget("text"))
                #if reward < 30:
                #    reward = 30
                if self.is_debug:
                    print(f"\n[STEP END] ball_positions:\n{np.array(self.game.ball_positions)}")
                    print(f"[STEP END] valid moves: {self.valid_moves}\n")
            else:
                reward -= 2
                if self.is_debug:
                    print(f"\nInvalid move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
                #terminated = True
        observation = self._get_obs()
        info = self._get_info()
        if self.is_debug:
            print(f"\nlast run reward: {reward}\n")
        return observation, reward, terminated, truncated, info
    

'''# Register the environment so we can create it with gym.make()
gym.register(
    id="bulletsim-delta-v0",
    entry_point="arm_env_delta:bulletsim_env_delta",
    max_episode_steps=80,  # Prevent infinite episodes
)


from stable_baselines3 import DQN

env = gym.make("bulletsim-delta-v0")

model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0003, train_freq=20, gamma=0.99, gradient_steps=20)
model.learn(total_timesteps=10000, log_interval=4)
model.save("solitare")

model = DQN.load("solitare", env=env)

obs, info = env.reset()
while True:
    action = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()'''