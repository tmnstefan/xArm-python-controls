import os
import time
from collections import defaultdict
from typing import Optional, cast
import numpy as np
import gymnasium as gym
import math
from gymnasium.envs.registration import register
import matplotlib
import matplotlib.pyplot as plt
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

"""Headless file for testing a variety of RL structures and comparing their performance"""

class solitare_rl_env(gym.Env):

    def __init__(self, is_debug=False):
        self.is_debug = is_debug
        self.current = 0
        self.runs = 0
        self.score = 0
        self.all_scores = []
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        
        obs_low = np.concatenate([
            np.full((7, 7), -1).flatten(),        # board array (49 values)
            np.array([0.0]),                       # normalized remaining balls
            np.array([0.0]),                       # progress metric
        ])

        obs_high = np.concatenate([
            np.full((7, 7), 1).flatten(),        # board array (49 values)
            np.array([1.0]),                       # normalized remaining balls
            np.array([1.0]),                       # progress metric
        ])
        self.observation_space = gym.spaces.Box(low=obs_low, high=obs_high, dtype=np.float32)
        self.action_space = gym.spaces.Discrete(7 * 7 * 4)
        self._action_rows = 7
        self._action_cols = 7
        self._action_dirs = 4
        
        self.valid_moves = self.check_all_valid_moves()

    def check_valid_moves(self, horizontal_index:int, vertical_index:int):
        out = []
        if vertical_index < 0 or horizontal_index < 0:
            return out
        if vertical_index >= len(self.ball_positions) or horizontal_index >= len(self.ball_positions[vertical_index]):
            return out
        if self.ball_positions[vertical_index][horizontal_index] != 1:
            return out

        # right
        if horizontal_index + 2 < len(self.ball_positions[vertical_index]):
            if self.ball_positions[vertical_index][horizontal_index + 1] == 1 and self.ball_positions[vertical_index][horizontal_index + 2] == 0:
                out.append((vertical_index, horizontal_index + 2))

        # left
        if horizontal_index - 2 >= 0:
            if self.ball_positions[vertical_index][horizontal_index - 1] == 1 and self.ball_positions[vertical_index][horizontal_index - 2] == 0:
                out.append((vertical_index, horizontal_index - 2))

        # down
        if vertical_index + 2 < len(self.ball_positions):
            if self.ball_positions[vertical_index + 1][horizontal_index] == 1 and self.ball_positions[vertical_index + 2][horizontal_index] == 0:
                out.append((vertical_index + 2, horizontal_index))

        # up
        if vertical_index - 2 >= 0:
            if self.ball_positions[vertical_index - 1][horizontal_index] == 1 and self.ball_positions[vertical_index - 2][horizontal_index] == 0:
                out.append((vertical_index - 2, horizontal_index))

        return out
    
    def check_all_valid_moves(self):
        valid = []
        for i in range(7):
            for j in range(7):
                moves = self.check_valid_moves(horizontal_index=j, vertical_index=i)
                for move in moves:
                    valid.append((i, j, move[0], move[1]))
        return valid
    
    def _get_action_mask(self) -> np.ndarray:
        """Generate a boolean mask of valid actions.
        
        Returns:
            np.ndarray: Boolean array of shape (action_space_size,) where True indicates valid action
        """
        action_space = cast(gym.spaces.Discrete, self.action_space)
        mask = np.zeros(action_space.n, dtype=np.bool_)
        
        for source_row in range(7):
            for source_col in range(7):
                valid_destinations = self.check_valid_moves(horizontal_index=source_col, vertical_index=source_row)
                
                for dest_row, dest_col in valid_destinations:
                    # Determine direction based on source and destination
                    if dest_row == source_row - 2:  # up
                        direction = 0
                    elif dest_row == source_row + 2:  # down
                        direction = 1
                    elif dest_col == source_col - 2:  # left
                        direction = 2
                    elif dest_col == source_col + 2:  # right
                        direction = 3
                    else:
                        continue
                    
                    # Calculate action index from (row, col, direction)
                    action_index = source_row * (self._action_cols * self._action_dirs) + source_col * self._action_dirs + direction
                    mask[action_index] = True
        
        return mask
    
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
            np.ndarray: Observation including board state, ball count, and progress
        """
        # Calculate progress metrics
        remaining_balls = 32 - self.score
        normalized_remaining = remaining_balls / 32.0  # 0 to 1 scale
        progress = self.score / 32.0  # 0 to 1 scale (progress toward goal)
        
        return np.concatenate([
            np.array(self.ball_positions).flatten().astype(np.float32),  # board array (49 values)
            np.array([normalized_remaining], dtype=np.float32),           # remaining balls (1 value)
            np.array([progress], dtype=np.float32),                       # progress metric (1 value)
        ])
    

    def _get_info(self):
        return {
            "score": self.score,
            "board state": np.array(self.ball_positions).flatten(),
            "action_mask": self._get_action_mask(),
        }
        
    def reset_board(self):
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        self.balls_in_jail = 0

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
        self.all_scores.append(self.score)
        self.score = 0
        #self.ui.connect_to_ip()
        self.reset_board()
        self.current = 0

        self.valid_moves = self.check_all_valid_moves()

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
        
        self.valid_moves = self.check_all_valid_moves()
        source_row, source_col, direction = self._decode_action(action)

        if self.is_debug:
            print(f"\n[STEP START] ball_positions:\n{np.array(self.ball_positions)}")
            print(f"[STEP START] valid moves: {self.valid_moves}\n")
            print(f"[STEP START] action: {action} -> decoded: ({source_row}, {source_col}, {direction})\n")
            #time.sleep(0.05)
        terminated = False
        truncated = False
        reward = 0
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
        
        valid_destinations = self.check_valid_moves(horizontal_index=source_col, vertical_index=source_row)
        if len(self.valid_moves) == 0:
            # Terminal state: no more moves available
            terminated = True
            self.valid_moves = self.check_all_valid_moves()
            if self.score == 32:
                # SUCCESS: Only 1 ball remaining (solved solitaire!)
                reward = 1000.0
            else:
                # FAILURE: Dead-end state, scale penalty by proximity to goal
                # Reaching 10+ balls is better than reaching 1 ball
                remaining_balls = 32 - self.score
                reward = -remaining_balls * 10.0  # Penalty scales with distance from goal
                reward = max(reward, -200.0)  # Cap penalty to prevent extreme values
        elif self.runs >= 150:
            # Timeout: too many steps without solving
            terminated = True
            self.valid_moves = self.check_all_valid_moves()
            reward = -50.0
        else:
            if (dest_row, dest_col) in valid_destinations:
                # Valid move executed successfully
                self.runs += 1
                if self.is_debug:
                    print(f"\nExecuting move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
                self.ball_positions[source_row][source_col] = 0
                self.ball_positions[dest_row][dest_col] = 1
                self.ball_positions[(source_row + dest_row) // 2][(source_col + dest_col) // 2] = 0    
                self.current = 0
                self.score += 1
                self.valid_moves = self.check_all_valid_moves()
                
                # Reward components:
                # - Small penalty for each step (encourages efficiency)
                # - Progress bonus for each ball removed
                step_penalty = -0.05  # Small penalty per step
                progress_bonus = 0.5  # Bonus for each ball removed (0.5 * 31 moves = 15.5 bonus)
                reward = progress_bonus + step_penalty
                if self.is_debug:
                    print(f"\n[STEP END] ball_positions:\n{np.array(self.ball_positions)}")
                    print(f"[STEP END] valid moves: {self.valid_moves}\n")
            else:
                # Invalid move (should be very rare with action masking)
                reward = -3.0
                if self.is_debug:
                    print(f"\nInvalid move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
        observation = self._get_obs()
        info = self._get_info()
        if self.is_debug:
            print(f"\nlast run reward: {reward}\n")
        return observation, reward, terminated, truncated, info

class solitare_rl_env_forced(gym.Env):

    def __init__(self, is_debug=False):
        self.is_debug = is_debug
        self.current = 0
        self.runs = 0
        self.score = 0
        self.all_scores = []
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        
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
        
        self.valid_moves = self.check_all_valid_moves()

    def check_valid_moves(self, horizontal_index:int, vertical_index:int):
        out = []
        if vertical_index < 0 or horizontal_index < 0:
            return out
        if vertical_index >= len(self.ball_positions) or horizontal_index >= len(self.ball_positions[vertical_index]):
            return out
        if self.ball_positions[vertical_index][horizontal_index] != 1:
            return out

        # right
        if horizontal_index + 2 < len(self.ball_positions[vertical_index]):
            if self.ball_positions[vertical_index][horizontal_index + 1] == 1 and self.ball_positions[vertical_index][horizontal_index + 2] == 0:
                out.append((vertical_index, horizontal_index + 2))

        # left
        if horizontal_index - 2 >= 0:
            if self.ball_positions[vertical_index][horizontal_index - 1] == 1 and self.ball_positions[vertical_index][horizontal_index - 2] == 0:
                out.append((vertical_index, horizontal_index - 2))

        # down
        if vertical_index + 2 < len(self.ball_positions):
            if self.ball_positions[vertical_index + 1][horizontal_index] == 1 and self.ball_positions[vertical_index + 2][horizontal_index] == 0:
                out.append((vertical_index + 2, horizontal_index))

        # up
        if vertical_index - 2 >= 0:
            if self.ball_positions[vertical_index - 1][horizontal_index] == 1 and self.ball_positions[vertical_index - 2][horizontal_index] == 0:
                out.append((vertical_index - 2, horizontal_index))

        return out
    
    def check_all_valid_moves(self):
        valid = []
        for i in range(7):
            for j in range(7):
                moves = self.check_valid_moves(horizontal_index=j, vertical_index=i)
                for move in moves:
                    valid.append((i, j, move[0], move[1]))
        return valid
    
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
            np.array(self.ball_positions).flatten(),        # board array
        ])
    

    def _get_info(self):
        return {
            "score": self.score,
            "board state": np.array(self.ball_positions).flatten(),
        }
        
    def reset_board(self):
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        self.balls_in_jail = 0

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
        self.all_scores.append(self.score)
        self.score = 0
        #self.ui.connect_to_ip()
        self.reset_board()
        self.current = 0

        self.valid_moves = self.check_all_valid_moves()

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
        
        self.valid_moves = self.check_all_valid_moves()
        source_row, source_col, direction = self._decode_action(action)

        if self.is_debug:
            print(f"\n[STEP START] ball_positions:\n{np.array(self.ball_positions)}")
            print(f"[STEP START] valid moves: {self.valid_moves}\n")
            print(f"[STEP START] action: {action} -> decoded: ({source_row}, {source_col}, {direction})\n")
            #time.sleep(0.05)
        terminated = False
        truncated = False
        reward = 0
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
        
        valid_destinations = self.check_valid_moves(horizontal_index=source_col, vertical_index=source_row)
        if len(self.valid_moves) == 0:
            terminated = True
            self.valid_moves = self.check_all_valid_moves()
            if self.score == 32:
                reward += 32 * 32
            else:
                reward -= 32 * 32 * 5
        elif self.runs >= 300:
            terminated = True
            self.valid_moves = self.check_all_valid_moves()
            reward -= 32 * 32
        else:
            if (dest_row, dest_col) in valid_destinations:
                self.runs += 1
                if self.is_debug:
                    print(f"\nExecuting move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
                self.ball_positions[source_row][source_col] = 0
                self.ball_positions[dest_row][dest_col] = 1
                self.ball_positions[(source_row + dest_row) // 2][(source_col + dest_col) // 2] = 0    
                self.current = 0
                self.score += 1
                self.valid_moves = self.check_all_valid_moves()
                reward -= self.score * self.score
                #reward += self.current_score * self.current_score
                #if reward < 30:
                #    reward = 30
                if self.is_debug:
                    print(f"\n[STEP END] ball_positions:\n{np.array(self.ball_positions)}")
                    print(f"[STEP END] valid moves: {self.valid_moves}\n")
            else:
                terminated = True
                reward -= 32 * 32
                if self.is_debug:
                    print(f"\nInvalid move: ({source_row}, {source_col}) to ({dest_row}, {dest_col})\n")
        observation = self._get_obs()
        info = self._get_info()
        if self.is_debug:
            print(f"\nlast run reward: {reward}\n")
        return observation, reward, terminated, truncated, info

class solitare_rl_env_alt(gym.Env):

    def __init__(self, is_debug=False):
        self.is_debug = is_debug
        #self.ui.connect_to_ip()
        self.current = 0
        self.runs = 0
        self.score = 0
        self.all_scores = []
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
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
        
        self.valid_moves = self.check_all_valid_moves()

    def reset_board(self):
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        self.balls_in_jail = 0

    def check_valid_moves(self, horizontal_index:int, vertical_index:int):
        out = []
        if vertical_index < 0 or horizontal_index < 0:
            return out
        if vertical_index >= len(self.ball_positions) or horizontal_index >= len(self.ball_positions[vertical_index]):
            return out
        if self.ball_positions[vertical_index][horizontal_index] != 1:
            return out

        # right
        if horizontal_index + 2 < len(self.ball_positions[vertical_index]):
            if self.ball_positions[vertical_index][horizontal_index + 1] == 1 and self.ball_positions[vertical_index][horizontal_index + 2] == 0:
                out.append((vertical_index, horizontal_index + 2))

        # left
        if horizontal_index - 2 >= 0:
            if self.ball_positions[vertical_index][horizontal_index - 1] == 1 and self.ball_positions[vertical_index][horizontal_index - 2] == 0:
                out.append((vertical_index, horizontal_index - 2))

        # down
        if vertical_index + 2 < len(self.ball_positions):
            if self.ball_positions[vertical_index + 1][horizontal_index] == 1 and self.ball_positions[vertical_index + 2][horizontal_index] == 0:
                out.append((vertical_index + 2, horizontal_index))

        # up
        if vertical_index - 2 >= 0:
            if self.ball_positions[vertical_index - 1][horizontal_index] == 1 and self.ball_positions[vertical_index - 2][horizontal_index] == 0:
                out.append((vertical_index - 2, horizontal_index))

        return out
    
    def check_all_valid_moves(self):
        valid = []
        for i in range(7):
            for j in range(7):
                moves = self.check_valid_moves(horizontal_index=j, vertical_index=i)
                for move in moves:
                    valid.append((i, j, move[0], move[1]))
        return valid
    
    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            dict: Observation with agent and target positions
        """
        if len(self.valid_moves) == 0:
            return np.concatenate([
                np.array(self.ball_positions).flatten(),        # board array
                np.array([0, 0, 0, 0]), # current selected space
            ])
        if self.current >= len(self.valid_moves):
            self.current = 0
        return np.concatenate([
            np.array(self.ball_positions).flatten(),        # board array
            np.array(self.valid_moves[self.current]), # current selected space
        ])
    

    def _get_info(self):
        return {
            "score": self.score,
            "board state": np.array(self.ball_positions).flatten(),
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
        self.reset_board()
        self.current = 0
        self.all_scores.append(self.score)
        self.score = 0

        self.valid_moves = self.check_all_valid_moves()

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
        self.valid_moves = self.check_all_valid_moves()
        if self.is_debug:
            print(f"\n[STEP START] ball_positions:\n{np.array(self.ball_positions)}")
            print(f"[STEP START] valid moves: {self.valid_moves}\n")
        terminated = False
        truncated = False
        reward = 0
        
        if action == 0:
            if len(self.valid_moves) == 0:
                terminated = True
                if self.score == 32:
                    reward += 100
                else:
                    reward -= 30
                #reward -= 33
                #reward += np.sqrt(self.score * self.runs)
            else:
                if self.current >= len(self.valid_moves) - 1:
                    action = 1
                    reward -= 4
                    self.current = np.random.randint(0, len(self.valid_moves))
                else:
                    self.current += 1
        if action == 1:
            if len(self.valid_moves) == 0:
                terminated = True
                if self.score == 32:
                    reward += 100
                else:
                    reward -= 30
                #reward -= 33
                #reward += np.sqrt(self.score * self.runs)
            else:
                move = self.valid_moves[self.current]
                if self.is_debug:
                    print(f"\nExecuting move: {move}\n")
                self.ball_positions[move[0]][move[1]] = 0
                self.ball_positions[move[2]][move[3]] = 1
                self.ball_positions[(move[0] + move[2]) // 2][(move[1] + move[3]) // 2] = 0    
                self.current = 0
                self.valid_moves = self.check_all_valid_moves()
                if self.is_debug:
                    print(f"\n[STEP END] ball_positions:\n{np.array(self.ball_positions)}")
                    print(f"[STEP END] valid moves: {self.valid_moves}\n")
                if self.current >= len(self.valid_moves):
                    self.current = 0
                reward -= 1
                self.score += 1
                #reward += int(self.ui.current_score.cget("text")) * int(self.ui.current_score.cget("text"))
            
        observation = self._get_obs()
        info = self._get_info()
        if self.is_debug:
            print(f"\nlast run reward: {reward}\n")
        return observation, reward, terminated, truncated, info

# Register the environment so we can create it with gym.make()
gym.register(
    id="solitaire_headless-v0",
    entry_point="solitare_env_headless:solitare_rl_env",
    max_episode_steps=10000,  # Prevent infinite episodes
)


from stable_baselines3 import DQN
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

def mask_fn(env):
    """Extract action mask from environment info."""
    return env.unwrapped._get_action_mask()

env = gym.make("solitaire_headless-v0", is_debug=False)
env = ActionMasker(env, mask_fn)
base_env = cast(solitare_rl_env, env.unwrapped)

#model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0003, train_freq=32, gamma=0.99, gradient_steps=-1)
model = MaskablePPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, gamma=0.99)
model.learn(total_timesteps=40000, log_interval=50)

# Plot scores after training completes
if len(base_env.all_scores) > 0:
    plt.figure(figsize=(12, 6))
    plt.plot(base_env.all_scores, label='Episode Scores', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.title('Training Scores Over Episodes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('training_scores.png')
    print(f"Score plot saved as 'training_scores.png'")
    print(f"Total episodes: {len(base_env.all_scores)}")
    print(f"Max score: {max(base_env.all_scores)}")
    print(f"Average score: {np.mean(base_env.all_scores):.2f}")
    plt.show()

model.save("solitare")

model = DQN.load("solitare", env=env)

obs, info = env.reset()
while True:
    action = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
