from importlib.resources import simple
from xarm.wrapper import XArmAPI
from actions.error import arm_errors
from actions.gripper import gripper_control
from actions.move_cartesian import cartesian_control
from actions.read_write import read_write_control
from actions.register_release import register_release_control
from actions.settings import arm_settings
from actions.trajectory_recording import trajectory_recording
from actions.util import arm_utilities
from xarm.wrapper import XArmAPI
import numpy as np
import time

class solitare():

    def __init__(self, arm:XArmAPI, tool_length = 60) -> None:
        self.arm = arm
        self.errors = arm_errors(arm)
        self.gripper = gripper_control(arm)
        self.movement = cartesian_control(arm)
        self.settings = arm_settings(arm)
        self.util=arm_utilities(arm)
        self.util.connect()
        self.errors.clean_error()
        self.util.clean_warn()
        self.settings.set_state(0)
        self.settings.set_collision_rebound(on=True)
        self.balls_in_jail = 0

        #grid separation in mm
        self.grid_separation = 29
        self.tool_length = tool_length
        
        #self.ball_positions = np.full(shape=(6, 6), fill_value=-1)
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]

    def reset_board(self):
        self.ball_positions = [[-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [1, 1, 1, 0, 1, 1, 1], 
                               [1, 1, 1, 1, 1, 1, 1], 
                               [-1, -1, 1, 1, 1, -1, -1], 
                               [-1, -1, 1, 1, 1, -1, -1]]
        self.balls_in_jail = 0

    def simple_move(self, x:float, y:float, z:float, roll = None, pitch = None, yaw = None):
        # set up arm
        current_pos = self.settings.get_position(is_radian=False)[1]
        if current_pos[2] < 200: # move to at least 200mm above base height if not already
            self.movement.set_position(x=current_pos[0], y=current_pos[1], z=200, roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5], is_radian=False, wait=True)
            time.sleep(1)
        current_xy = np.array([current_pos[0], current_pos[1]])
        desired_xy = np.array([x, y])
        # https://wumbo.net/formulas/angle-between-two-vectors-2d/
        # currently finds the signed angle between given 2d vectors, positive if anticlockwise from current to desired, negative if clockwise
        signed_angle_rad = np.atan2(current_xy[0]*desired_xy[1] - current_xy[1]*desired_xy[0], current_xy[0]*desired_xy[0] + current_xy[1]*desired_xy[1])
        signed_angle_deg = np.degrees(signed_angle_rad)
        current_angle = self.movement.get_servo_angle(servo_id=1)[1]
        # if angle change between desired and current position is over 45 degrees either way
        # move joint 1 to the desired angle before continuing motion
        if signed_angle_deg > 45 or signed_angle_deg < -45:
            if current_angle + signed_angle_deg > 360:
                self.movement.set_servo_angle(servo_id=1, angle=signed_angle_deg - 360, is_radian=False, relative=True, wait=True, timeout=20)
            elif current_angle + signed_angle_deg < -360:
                self.movement.set_servo_angle(servo_id=1, angle=signed_angle_deg + 360, is_radian=False, relative=True, wait=True, timeout=20)
            else:
                self.movement.set_servo_angle(servo_id=1, angle=signed_angle_deg, is_radian=False, relative=True, wait=True, timeout=20)
        # move to desired position
        self.movement.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, is_radian=False, wait=True, timeout=20)

        # if error code 23 (angle limit error) is triggered, move joint 1 back to 0 degrees and try again
        if self.errors.get_err_warn_code(show=True)[1] == [23, 0]:
            print(self.errors.get_c23_error_info(is_radian=False))
            self.errors.clean_error()
            self.settings.set_state(0)
            current_angle = self.movement.get_servo_angle(servo_id=1)[1]
            # Handle case where current_angle might be a list
            angle_val = current_angle[0] if isinstance(current_angle, list) else current_angle
            move_angle = 0 - int(angle_val)
            self.movement.set_servo_angle(servo_id=1, angle=move_angle, is_radian=False, relative=True, wait=True, timeout=20) # doesnt work in absolute coordinate system so using relative for now
            self.movement.move_gohome(wait=True, timeout=20)
            time.sleep(5) # arm is annoying and will try to move before fully resetting, this is a fix for that
            self.simple_move(x, y, z, roll, pitch, yaw)

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
    
    def check_grid(self):
        complete = False
        for i in range(7):
            for j in range(7):
                output = self.check_valid_moves(i, j)
                if output.count == 0:
                    complete = True
                    break
        return complete
    
    def move_ball(self, center_pos:list[float], start_vertical:int, start_horizontal:int, end_vertical:int, end_horizontal:int):
        # using top left corner of grid as base pos
        base_pos = [center_pos[0] + (self.grid_separation * 3), center_pos[1] + (self.grid_separation * 3), center_pos[2]]
        ball_x = base_pos[0] - (self.grid_separation * start_vertical)
        ball_y = base_pos[1] - (self.grid_separation * start_horizontal)
        ball_z = base_pos[2]
        target_x = base_pos[0] - (self.grid_separation * end_vertical)
        target_y = base_pos[1] - (self.grid_separation * end_horizontal)
        self.simple_move(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 20)
        time.sleep(0.1)
        self.movement.set_position(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 5, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        time.sleep(0.1)
        self.gripper.set_vacuum_gripper(on=True, wait=True)
        while self.gripper.get_vacuum_gripper()[1] != 1:
            self.movement.set_position(x=0, y=0, z=-0.5, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
        time.sleep(0.1)
        self.movement.set_position(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.movement.set_position(x=target_x, y=target_y, z=ball_z + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.movement.set_position(x=target_x, y=target_y, z=ball_z + self.tool_length + 6, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.gripper.set_vacuum_gripper(on=False, wait=True)
        time.sleep(0.1)
        
        self.movement.set_position(x=target_x, y=target_y, z=ball_z + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.ball_positions[end_vertical][end_horizontal] = 1
        self.ball_positions[start_vertical][start_horizontal] = 0

    def remove_captured_ball(self, center_pos:list[float], vertical:int, horizontal:int):
        base_pos = [center_pos[0] + (self.grid_separation * 3), center_pos[1] + (self.grid_separation * 3), center_pos[2]]
        ball_x = base_pos[0] - (self.grid_separation * vertical)
        ball_y = base_pos[1] - (self.grid_separation * horizontal)
        ball_z = base_pos[2]
        self.simple_move(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 20)
        time.sleep(0.1)
        self.movement.set_position(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 5, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        time.sleep(0.1)
        self.gripper.set_vacuum_gripper(on=True, wait=True)
        while self.gripper.get_vacuum_gripper()[1] != 1:
            self.movement.set_position(x=0, y=0, z=-0.5, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
        time.sleep(0.1)
        #prison_pos = self.closest_jail_position(x=ball_x, y=ball_y, center_pos=center_pos)
        prison_pos = self.next_jail_position(center_pos=center_pos)
        self.movement.set_position(x=ball_x, y=ball_y, z=ball_z + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.movement.set_position(x=prison_pos[0], y=prison_pos[1], z=prison_pos[2] + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.movement.set_position(x=prison_pos[0], y=prison_pos[1], z=prison_pos[2] + self.tool_length + 6, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.gripper.set_vacuum_gripper(on=False, wait=True)
        time.sleep(0.1)
        self.movement.set_position(x=prison_pos[0], y=prison_pos[1], z=prison_pos[2] + self.tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
        self.ball_positions[vertical][horizontal] = 0
        self.balls_in_jail += 1

    def closest_jail_position(self, x, y, center_pos):
        """Calculate the closest jail position for a captured ball"""
        closest_position = [0, 0, 0]  # x, y, z
        change_x = center_pos[0] - x
        change_y = center_pos[1] - y
        print(f"change_x: {change_x}, change_y: {change_y}")
        closest_position[0] = center_pos[0] + ((change_x) / (np.sqrt(change_x ** 2 + change_y ** 2)) * 130) * -1
        closest_position[1] = center_pos[1] + ((change_y) / (np.sqrt(change_x ** 2 + change_y ** 2)) * 130) * -1
        closest_position[2] = 25
        print(f"\nclosest jail position: {closest_position}\n")
        return closest_position

    def next_jail_position(self, center_pos):
        """Calculate the next jail position for a captured ball based on how many balls are already in jail"""
        angle = (self.balls_in_jail * 10) % 360
        # Use a single fixed ring for jail positions; do not increase radius per group
        radius = 130
        x = center_pos[0] - (radius * np.cos(np.radians(angle)))
        y = center_pos[1] - (radius * np.sin(np.radians(angle)))
        z = 25
        return [x, y, z]