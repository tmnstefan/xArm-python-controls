import os
import time
from collections import defaultdict
from typing import Optional, TYPE_CHECKING
import numpy as np
import gymnasium as gym
import math
from gymnasium.envs.registration import register

if TYPE_CHECKING:
    from solitare_ui_tkinter import solitare_ui

"""Basic RL environment for this variant of solitaire"""

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
            np.full(2, 0),         # current selected space
            np.full(2, 0),       # space to move to
        ])

        obs_high = np.concatenate([
            np.full((7, 7), 1).flatten(),        # board array
            np.full(2, 6),         # current selected space
            np.full(2, 6),       # space to move to
        ])
        self.observation_space = gym.spaces.Box(low=obs_low, high=obs_high, dtype=np.int64)
        self.action_space = gym.spaces.Discrete(2)  # 0: select next move, 1: execute move

        if self.ui.game != None:
            self.game = self.ui.game
        else:
            raise Exception ("Game not found. Please initialize the solitare_ui and pass it to the environment.")
        
        self.valid_moves = self.game.check_all_valid_moves()

    
    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            dict: Observation with agent and target positions
        """
        if len(self.valid_moves) == 0:
            return np.concatenate([
                np.array(self.game.ball_positions).flatten(),        # board array
                np.array([0, 0, 0, 0]), # current selected space
            ])
        if self.current >= len(self.valid_moves):
            self.current = 0
        return np.concatenate([
            np.array(self.game.ball_positions).flatten(),        # board array
            np.array(self.valid_moves[self.current]), # current selected space
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
        self.runs += 1
        self.valid_moves = self.game.check_all_valid_moves()
        if self.is_debug:
            print(f"\n[STEP START] ball_positions:\n{np.array(self.game.ball_positions)}")
            print(f"[STEP START] valid moves: {self.valid_moves}\n")
        terminated = False
        truncated = False
        reward = 0
        
        if action == 0:
            if len(self.valid_moves) == 0:
                terminated = True
                #reward -= 33
                reward += np.sqrt(int(self.ui.current_score.cget("text")) * self.runs)
            else:
                if self.current >= len(self.valid_moves) - 1:
                    action = 1
                    self.current = np.random.randint(0, len(self.valid_moves))
                else:
                    self.current += 1
        if action == 1:
            if len(self.valid_moves) == 0:
                terminated = True
                #reward -= 33
                reward += np.sqrt(int(self.ui.current_score.cget("text")) * self.runs)
            else:
                move = self.valid_moves[self.current]
                if self.is_debug:
                    print(f"\nExecuting move: {move}\n")
                self.ui.button_clicked(move[0], move[1])
                self.ui.button_destination_clicked(move[2], move[3])
                self.game.ball_positions[move[0]][move[1]] = 0
                self.game.ball_positions[move[2]][move[3]] = 1
                self.game.ball_positions[(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = 0    
                self.ui.root.update()
                self.current = 0
                self.valid_moves = self.game.check_all_valid_moves()
                if self.is_debug:
                    print(f"\n[STEP END] ball_positions:\n{np.array(self.game.ball_positions)}")
                    print(f"[STEP END] valid moves: {self.valid_moves}\n")
                if self.current >= len(self.valid_moves):
                    self.current = 0
                #reward += 1
                #reward += int(self.ui.current_score.cget("text")) * int(self.ui.current_score.cget("text"))
            
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