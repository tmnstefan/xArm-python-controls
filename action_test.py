from importlib.resources import simple

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

arm = XArmAPI('127.0.0.1')
def simple_move(arm:XArmAPI, x:float, y:float, z:float, roll = None, pitch = None, yaw = None):
    arm_util = arm_utilities(arm)
    arm_movement = cartesian_control(arm)
    setting = arm_settings(arm)
    errors = arm_errors(arm)
    arm_util.connect()
    setting.set_state(0)
    setting.set_collision_rebound(on=True)
    current_pos = setting.get_position(is_radian=False)[1]
    if current_pos[2] < 200:
        arm_movement.set_position(x=current_pos[0], y=current_pos[1], z=200, roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5], is_radian=False, wait=True)
    current_xy = np.array([current_pos[0], current_pos[1]])
    desired_xy = np.array([x, y])
    # https://wumbo.net/formulas/angle-between-two-vectors-2d/
    # currently finds the signed angle between given 2d vectors, positive if anticlockwise from current to desired, negative if clockwise
    signed_angle_rad = np.atan2(current_xy[0]*desired_xy[1] - current_xy[1]*desired_xy[0], current_xy[0]*desired_xy[0] + current_xy[1]*desired_xy[1])
    signed_angle_deg = np.degrees(signed_angle_rad)
    current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
    if signed_angle_deg > 45 or signed_angle_deg < -45:
        print("\nlarge angle change")
        if current_angle + signed_angle_deg > 360:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg - 360, is_radian=False, relative=True, wait=True, timeout=20)
        elif current_angle + signed_angle_deg < -360:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg + 360, is_radian=False, relative=True, wait=True, timeout=20)
        else:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg, is_radian=False, relative=True, wait=True, timeout=20)

    arm_movement.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, is_radian=False, wait=True, timeout=20)

    if errors.get_err_warn_code(show=True)[1] == [23, 0]:
        print(errors.get_c23_error_info(is_radian=False))
        errors.clean_error()
        setting.set_state(0)
        current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
        # Handle case where current_angle might be a list
        angle_val = current_angle[0] if isinstance(current_angle, list) else current_angle
        move_angle = 0 - int(angle_val)
        arm_movement.set_servo_angle(servo_id=1, angle=move_angle, is_radian=False, relative=True, wait=True, timeout=20) # doesnt work in absolute coordinate system so using relative for now
        arm_movement.move_gohome(wait=True, timeout=20)
        time.sleep(5) # i dont know why this works but its the only way to stop the arm trying to go through itself once it's reset
        simple_move(arm, x, y, z, roll, pitch, yaw)



#basic motion test
#simple_move(arm, x=0, y=-200, z=200, roll=180, pitch=0, yaw=0)

#test for dealing with going over angle limits
simple_move(arm, x=0, y=200, z=200, roll=180, pitch=0, yaw=0)
time.sleep(0.5)
simple_move(arm, x=-200, y=0, z=200, roll=180, pitch=0, yaw=0)
time.sleep(0.5)
simple_move(arm, x=0, y=-200, z=200, roll=180, pitch=0, yaw=0)
time.sleep(0.5)
simple_move(arm, x=200, y=0, z=200, roll=180, pitch=0, yaw=0)
time.sleep(0.5)
simple_move(arm, x=0, y=200, z=200, roll=180, pitch=0, yaw=0)
time.sleep(0.5)

# tests for dealing with large angle changes
simple_move(arm, x=-200, y=-300, z=-50, roll=180, pitch=0, yaw=0)
time.sleep(0.5)
simple_move(arm, x=50, y=350, z=300, roll=180, pitch=0, yaw=0)

current_xy = np.array([0, 200])
desired_xy = np.array([200, 0])

unit_x = current_xy / np.linalg.norm(current_xy)
unit_y = desired_xy / np.linalg.norm(desired_xy)
angle_rad = np.arccos(np.dot(unit_x, unit_y))
angle_deg = np.degrees(angle_rad)
# https://wumbo.net/formulas/angle-between-two-vectors-2d/
# currently finds the signed angle between given 2d vectors, positive if anticlockwise from current to desired, negative if clockwise
signed_angle_rad = np.atan2(current_xy[0]*desired_xy[1] - current_xy[1]*desired_xy[0], current_xy[0]*desired_xy[0] + current_xy[1]*desired_xy[1])
signed_angle_deg = np.degrees(signed_angle_rad)
print("signed angle is \n \n \n \n")
print(signed_angle_deg)
print(signed_angle_rad)

#angle = np.arccos(np.clip(np.dot(current_xy, desired_xy), -1.0, 1.0))
print("angle is \n \n \n \n")
#print(angle)
#print(np.degrees(angle))
print(angle_deg)
print(angle_rad)


#arm_util = arm_utilities(arm)
#arm_movement = cartesian_control(arm)
#setting=arm_settings(arm)
#arm_util.connect(port='127.0.0.1')
#setting.set_collision_rebound(on=True)
#print("\n \n using tool position")
#arm_movement.set_tool_position(x=200, y=0, z=200, roll=0, pitch=0, yaw=0, is_radian=False, wait=True)
#arm_movement.reset()
#print(arm_movement.get_servo_angle())
#arm_movement.set_position(x=-100, y=-300, z=200, roll=180, pitch=0, yaw=0, is_radian=False, wait=True, radius=300)
#arm_movement.set_position(x=100, y=300, z=200, roll=180, pitch=0, yaw=0, is_radian=False, wait=True, radius=300)
#current_pos = setting.get_position(is_radian=False)[1]
#print(current_pos)
#arm_movement.set_position(x=current_pos[0], y=current_pos[1], z=current_pos[2] + 100, roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5], is_radian=False)
#arm_movement.set_position_aa(axis_angle_pose=[0, 0, 100, 0, 0, 0], is_radian=False, relative=True)
#arm_movement.set_position(x=-300, y=0, z=200, roll=180, pitch=0, yaw=0, is_radian=False, wait=True, radius=300)
#print(arm_movement.get_servo_angle())


