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
import yaml

"""Testing for a variety of new functions for the arm, not all of the functions work"""

arm = XArmAPI('127.0.0.1')
def simple_move(arm:XArmAPI, x:float, y:float, z:float, roll = None, pitch = None, yaw = None):
    """Mildly improved motion handling compared to default motion functions"""
    # set up arm
    arm_util = arm_utilities(arm)
    arm_movement = cartesian_control(arm)
    setting = arm_settings(arm)
    errors = arm_errors(arm)
    arm_util.connect()
    setting.set_state(0)
    setting.set_collision_rebound(on=True)
    current_pos = setting.get_position(is_radian=False)[1]
    if current_pos[2] < 200: # move to at least 200mm above base height if not already
        arm_movement.set_position(x=current_pos[0], y=current_pos[1], z=200, roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5], is_radian=False, wait=True)
        time.sleep(1)
    current_xy = np.array([current_pos[0], current_pos[1]])
    desired_xy = np.array([x, y])
    # https://wumbo.net/formulas/angle-between-two-vectors-2d/
    # currently finds the signed angle between given 2d vectors, positive if anticlockwise from current to desired, negative if clockwise
    signed_angle_rad = np.atan2(current_xy[0]*desired_xy[1] - current_xy[1]*desired_xy[0], current_xy[0]*desired_xy[0] + current_xy[1]*desired_xy[1])
    signed_angle_deg = np.degrees(signed_angle_rad)
    current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
    # if angle change between desired and current position is over 45 degrees either way
    # move joint 1 to the desired angle before continuing motion
    if signed_angle_deg > 45 or signed_angle_deg < -45:
        if current_angle + signed_angle_deg > 360:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg - 360, is_radian=False, relative=True, wait=True, timeout=20)
        elif current_angle + signed_angle_deg < -360:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg + 360, is_radian=False, relative=True, wait=True, timeout=20)
        else:
            arm_movement.set_servo_angle(servo_id=1, angle=signed_angle_deg, is_radian=False, relative=True, wait=True, timeout=20)
    # move to desired position
    arm_movement.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, is_radian=False, wait=True, timeout=20)

    # if error code 23 (angle limit error) is triggered, move joint 1 back to 0 degrees and try again
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
        time.sleep(5) # arm is annoying and will try to move before fully resetting, this is a fix for that
        simple_move(arm, x, y, z, roll, pitch, yaw)


def move_to_vial_old(arm:XArmAPI, tray_x:float, tray_y:float, tray_z:float, row_num:int, column_num:int, x_spacing:float, y_spacing:float, x_offset:float, y_offset:float):
    """Old method of moving to a vial on a tray with known spacing"""
    arm_util = arm_utilities(arm)
    setting = arm_settings(arm)
    arm_util.connect()
    setting.set_state(0)
    setting.set_collision_rebound(on=True)
    column_pos = tray_y + x_offset + (column_num - 1) * x_spacing
    row_pos = tray_x + y_offset + (row_num - 1) * y_spacing
    simple_move(arm, x=row_pos, y=column_pos, z=tray_z + 100, roll=180, pitch=0, yaw=0)

def move_to_vial(arm:XArmAPI, tray_x:float, tray_y:float, tray_z:float, row_num:int, column_num:int, tray_type:int):
    """Move to above a given vial index for specified tray type"""
    path = f"vial_tray_{tray_type}.yml"
    # make sure entered tray type is valid, if so open relevant file
    try: 
        with open(path, "r") as f:
            tray_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}, please ensure you have input the correct tray type")
    # ensure column and row numbers are valid for given tray type
    if column_num > tray_data['dimensions']['column_num'] or row_num > tray_data['dimensions']['row_num'] or column_num < 1 or row_num < 1:
        raise ValueError(f"Row or column number exceeds dimensions of tray, please ensure you have input the correct row and column numbers for the given tray type")
    # extract positional data from yaml file
    x_spacing = tray_data['spacing']['x-spacing']
    y_spacing = tray_data['spacing']['y-spacing']
    x_offset = tray_data['spacing']['x-offset']
    y_offset = tray_data['spacing']['y-offset']
    height = tray_data['footprint']['height']
    # arm set up
    arm_util = arm_utilities(arm)
    setting = arm_settings(arm)
    arm_util.connect()
    setting.set_state(0)
    setting.set_collision_rebound(on=True)
    # find position of vial based on data from yaml file and move to it
    column_pos = tray_y + x_offset + (column_num - 1) * x_spacing
    row_pos = tray_x + y_offset + (row_num - 1) * y_spacing
    simple_move(arm, x=row_pos, y=column_pos, z=tray_z + height + 100, roll=180, pitch=0, yaw=0)

def plus_draw(arm:XArmAPI, draw_z:float, tool_length:float):
    """Crude way of drawing a cross onto a surface"""
    arm_movement = cartesian_control(arm)
    arm_movement.set_position(z=draw_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=5, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
    arm_movement.set_position(z=draw_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=-10, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
    arm_movement.set_position(z=draw_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=5, y=5, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
    arm_movement.set_position(z=draw_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(y=-10, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)
    arm_movement.set_position(z=draw_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(y=5, roll=0, pitch=0, yaw=0, relative=True, is_radian=False, wait=True)


def draw_vial_grid(arm:XArmAPI, tray_x:float, tray_y:float, tray_z:float, tray_type:int, tool_length:int=100):
    """Draw a "grid" at the positions where vials would be on a tray"""
    path = f"vial_tray_{tray_type}.yml"
    # make sure entered tray type is valid, if so open relevant file
    try:
        with open(path, "r") as f:
            tray_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}, please ensure you have input the correct tray type")
    row_num = tray_data['dimensions']['row_num']
    column_num = tray_data['dimensions']['column_num']
    for row in range(1, row_num + 1): # move to each vial in tray and draw a cross at that location
        for column in range(1, column_num + 1):
            move_to_vial(arm, tray_x=tray_x, tray_y=tray_y, tray_z=tray_z, row_num=row, column_num=column, tray_type=tray_type)
            time.sleep(1)
            plus_draw(arm, draw_z=tray_z, tool_length=tool_length)

def pick_film(arm:XArmAPI, film_x:float, film_y:float, film_z:float, tool_length:float):
    """Pick up film"""
    gripper = gripper_control(arm)
    arm_movement = cartesian_control(arm)
    # move to above film, move down to film, turn on gripper, move back up with film
    simple_move(arm, x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    gripper.set_vacuum_gripper(on=True, wait=True)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length + 6, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    gripper.set_vacuum_gripper(on=False, wait=True)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)

def pick_ball(arm:XArmAPI, film_x:float, film_y:float, film_z:float, tool_length:float):
    """Pick up peg solitaire ball, predecessor to main solitaire functions"""
    gripper = gripper_control(arm)
    arm_movement = cartesian_control(arm)
    # move to above ball, move down to ball, turn on gripper, move back up with ball
    simple_move(arm, x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    gripper.set_vacuum_gripper(on=True, wait=True)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=film_x, y=film_y + 56, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(x=film_x, y=film_y + 56, z=film_z + tool_length + 6, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    gripper.set_vacuum_gripper(on=False, wait=True)
    time.sleep(1)
    arm_movement.set_position(x=film_x, y=film_y, z=film_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)

def place_film(arm:XArmAPI, place_x:float, place_y:float, place_z:float, tool_length:float):
    """Place film at a desired location"""
    gripper = gripper_control(arm)
    arm_movement = cartesian_control(arm)
    # move to above placement point, move down to point, turn off gripper, move back up without film
    simple_move(arm, x=place_x, y=place_y, z=place_z + tool_length + 50, roll=180, pitch=0, yaw=0)
    time.sleep(1)
    arm_movement.set_position(x=place_x, y=place_y, z=place_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    gripper.set_vacuum_gripper(on=False, wait=True)
    arm_movement.set_servo_angle(servo_id=5, angle=4, speed=200, relative=True, is_radian=False)
    arm_movement.set_servo_angle(servo_id=5, angle=-4, speed=200, relative=True, is_radian=False)
    arm_movement.set_servo_angle(servo_id=5, angle=4, speed=200, relative=True, is_radian=False)
    arm_movement.set_servo_angle(servo_id=5, angle=-4, speed=200, relative=True, is_radian=False)
    time.sleep(1)
    arm_movement.set_position(x=place_x, y=place_y, z=place_z + tool_length + 50, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)

def move_film_grid(arm:XArmAPI, film_x:float, film_y:float, film_z:float, plate_x:float, plate_y:float, plate_z:float, row_num:int, column_num:int, tool_length:int=100):
    """Move a film from a specified index in a tray"""
    '''path = f"vial_tray_{tray_type}.yml"
    # make sure entered tray type is valid, if so open relevant file
    try:
        with open(path, "r") as f:
            tray_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}, please ensure you have input the correct tray type")
    row_num = tray_data['dimensions']['row_num']
    column_num = tray_data['dimensions']['column_num']'''
    for row in range(0, row_num): # move to each vial in tray and draw a cross at that location
        
        for column in range(0, column_num):
            pick_film(arm=arm, film_x=film_x, film_y=film_y, film_z=film_z, tool_length=tool_length)
            time.sleep(1)
            place_film(arm=arm, place_x=plate_x + (31 * column), place_y=plate_y - (31 * row), place_z=plate_z, tool_length=tool_length)
        film_z -= 1

"""Variety of old and new tests"""
#simple_move(arm=arm, x=100, y=100, z=100)
util = arm_utilities(arm=arm)
setting = arm_settings(arm)
movement = cartesian_control(arm)
errors = arm_errors(arm)
util.connect()
current = setting.get_position()[1]
arm.set_mode(0)
arm.set_state(0)
print(util.check_verification())
print(errors.get_err_warn_code())
util.clean_warn()
errors.clean_error()
arm.motion_enable(True)

arm.set_state(0)
print(errors.get_err_warn_code())

#move_film_grid(arm=arm, film_x=240, film_y=-165, film_z=8, plate_x=270, plate_y=0, plate_z=20, row_num=3, column_num=4, tool_length=60)

#picks up a ball, grid is 28x28
#pick_ball(arm=arm, film_x=257, film_y=-60, film_z=28, tool_length=60)


time.sleep(1)
#place_film(arm=arm, place_x=270, place_y=0, place_z=15, tool_length=60)
#movement.set_position(x=270, y=0, z=100)
#arm.set_vacuum_gripper(True)
time.sleep(2)
#arm.set_vacuum_gripper(False)
util.clean_warn()
util.disconnect()
"top left plate: (x=270, y=0, z=60)"
"second plate down on left (x=240, y=0, z=60)"
"plate holder distances: 30x30mm"
"plate stack: (x=245, y=-165, z=66)"
'''#tests, includes error handling for incorrect tray type
draw_vial_grid(arm, tray_x=0, tray_y=200, tray_z=100, tray_type=12, tool_length=80)

draw_vial_grid(arm, tray_x=0, tray_y=200, tray_z=100, tray_type=5, tool_length=80)

draw_vial_grid(arm, tray_x=0, tray_y=200, tray_z=100, tray_type=24, tool_length=80)
draw_vial_grid(arm, tray_x=0, tray_y=200, tray_z=100, tray_type=48, tool_length=80)
draw_vial_grid(arm, tray_x=0, tray_y=200, tray_z=100, tray_type=96, tool_length=80)

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
simple_move(arm, x=50, y=350, z=300, roll=180, pitch=0, yaw=0)'''

# attempt to use set_servo_angle for movement, does not work
'''def move_to_safe_position(arm:XArmAPI):
    arm_movement = cartesian_control(arm)
    settings = arm_settings(arm)
    settings.set_mode(1)
    arm_movement.move_gohome(wait=True, timeout=20)
    current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
    # Handle case where current_angle might be a list
    angle_val = current_angle[0] if isinstance(current_angle, list) else current_angle
    move_angle = 0 - int(angle_val)
    arm_movement.set_servo_angle(servo_id=1, angle=move_angle, is_radian=False, relative=True, wait=True, timeout=20) # doesnt work in absolute coordinate system so using relative for now
    settings.set_mode(1)
    safe_angles = settings.get_inverse_kinematics(pose = [0, 200, 200, 180, 0, 0, False])
    
    try:
        arm.set_servo_angle_j(angles=[90, 10, 32, 0, 22, 0], is_radian=False, wait=True, timeout=20)
    except Exception as e:
        print(f"Error occurred while setting servo angle: {e}")
        print(f"Safe angles were: {safe_angles[1]}")
    
    arm.set_servo_angle(angle=[90, 10, 32, 0, 22, 0], is_radian=False)

simple_move(arm, x=-100, y=-200, z=200, roll=180, pitch=0, yaw=0)
move_to_safe_position(arm)'''


"""Functions attempting to allow the arm to pick up and flip a film, WIP"""

def film_side_flip(arm:XArmAPI, stand_x:float, stand_y:float, stand_z:float, angle:float, tool_length:float):
    arm_movement = cartesian_control(arm)
    gripper = gripper_control(arm)
    simple_move(arm, x=stand_x - (np.cos(np.radians(angle)) * 50) + (np.sin(np.radians(angle)) * tool_length), y=stand_y - (np.sin(np.radians(angle)) * 50) + (np.cos(np.radians(angle)) * tool_length), z=stand_z)
    time.sleep(3)
    #current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
    # Handle case where current_angle might be a list
    #angle_val = current_angle[0] if isinstance(current_angle, list) else current_angle
    #start_angle = int(angle_val) + 90
    #end_angle = int(angle_val) - 90
    start_angle = angle + 90
    end_angle = angle - 90
    # move to side 1 of stand
    simple_move(arm, x=stand_x - (np.cos(np.radians(angle)) * 50) + (np.sin(np.radians(angle)) * tool_length), y=stand_y - (np.sin(np.radians(angle)) * 50) + (np.cos(np.radians(angle)) * tool_length), z=stand_z, roll=start_angle, pitch=90, yaw=0)
    time.sleep(1)
    # slide film into stand
    arm_movement.set_position(x=stand_x + (np.sin(np.radians(angle)) * tool_length), y=stand_y + (np.cos(np.radians(angle)) * tool_length), z=stand_z, roll=start_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    #let go of film
    gripper.set_vacuum_gripper(on=False, wait=True)
    # move to separate from film
    arm_movement.set_position(x=stand_x + (np.sin(np.radians(angle)) * (tool_length + 50)), y=stand_y + (np.cos(np.radians(angle)) * (tool_length + 50)), z=stand_z, roll=start_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    # move back to position with distance from stand
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50) + (np.sin(np.radians(angle)) * (tool_length + 50)), y=stand_y - (np.sin(np.radians(angle)) * 50) + (np.cos(np.radians(angle)) * (tool_length + 50)), z=stand_z, roll=start_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    # flip to other side of stand
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50) - (np.sin(np.radians(angle)) * (tool_length + 50)), y=stand_y - (np.sin(np.radians(angle)) * 50) - (np.cos(np.radians(angle)) * (tool_length + 50)), z=stand_z, roll=end_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    # move back towards stand to pick up film again
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50) - (np.sin(np.radians(angle)) * (tool_length + 5)), y=stand_y - (np.sin(np.radians(angle)) * 50) - (np.cos(np.radians(angle)) * (tool_length + 5)), z=stand_z, roll=end_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    # slide into stand
    arm_movement.set_position(x=stand_x - (np.sin(np.radians(angle)) * (tool_length + 5)), y=stand_y - (np.cos(np.radians(angle)) * (tool_length + 5)), z=stand_z, roll=end_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)
    # pick up film again
    gripper.set_vacuum_gripper(on=True, wait=True)
    # slide out of stand
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50) - (np.sin(np.radians(angle)) * (tool_length + 5)), y=stand_y - (np.sin(np.radians(angle)) * 50) - (np.cos(np.radians(angle)) * (tool_length + 5)), z=stand_z, roll=end_angle, pitch=90, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(1)

def film_upright_flip(arm:XArmAPI, stand_x:float, stand_y:float, stand_z:float, angle:float, tool_length:float):
    arm_movement = cartesian_control(arm)
    gripper = gripper_control(arm)
    simple_move(arm, x=stand_x - (np.cos(np.radians(angle)) * 50) + (np.sin(np.radians(angle)) * tool_length), y=stand_y - (np.sin(np.radians(angle)) * 50) + (np.cos(np.radians(angle)) * tool_length), z=stand_z)
    time.sleep(3)
    #current_angle = arm_movement.get_servo_angle(servo_id=1)[1]
    # Handle case where current_angle might be a list
    #angle_val = current_angle[0] if isinstance(current_angle, list) else current_angle
    #move_angle = 180 - int(angle_val)
    move_angle = 180 - angle
    simple_move(arm, x=stand_x - (np.cos(np.radians(angle)) * 50) + (np.sin(np.radians(angle)) * tool_length), y=stand_y - (np.sin(np.radians(angle)) * 50) + (np.cos(np.radians(angle)) * tool_length), z=stand_z, roll=180, pitch=90, yaw=np.abs(move_angle))
    time.sleep(3)
    arm_movement.set_position(x=stand_x, y=stand_y, z=stand_z, roll=180, pitch=90, yaw=move_angle, relative=False, is_radian=False, wait=True)
    time.sleep(3)
    gripper.set_vacuum_gripper(on=False, wait=True)
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50), y=stand_y - (np.sin(np.radians(angle)) * 50), z=stand_z, roll=180, pitch=90, yaw=np.abs(move_angle), relative=False, is_radian=False, wait=True)
    time.sleep(3)
    arm_movement.set_position(x=stand_x, y=stand_y, z=stand_z, relative=False, is_radian=False, wait=True)
    gripper.set_vacuum_gripper(on=True, wait=True)
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50), y=stand_y - (np.sin(np.radians(angle)) * 50), z=stand_z, roll=180, pitch=90, yaw=np.abs(move_angle), relative=False, is_radian=False, wait=True)  

def film_stand_flip(arm:XArmAPI, stand_x:float, stand_y:float, stand_z:float, angle:float, tool_length:float):
    simple_move(arm, x=stand_x - (np.cos(np.radians(angle)) * 50), y=stand_y - (np.sin(np.radians(angle)) * 50), z=stand_z + tool_length, roll=180, pitch=0, yaw=0)
    time.sleep(3)
    arm_movement = cartesian_control(arm)
    gripper = gripper_control(arm)
    arm_movement.set_position(x=stand_x, y=stand_y, z=stand_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    time.sleep(3)
    gripper.set_vacuum_gripper(on=False, wait=True)
    arm_movement.set_position(z=20, relative=True, is_radian=False, wait=True)
    time.sleep(3)
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50), y=stand_y - (np.sin(np.radians(angle)) * 50), z=stand_z + tool_length + 20, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)
    arm_movement.set_position(z=-30, relative=True, is_radian=False, wait=True)
    arm_movement.set_position(roll = 0, pitch=0, yaw=180, relative=False, is_radian=False, wait=True)
    time.sleep(3)
    arm_movement.set_position(x=stand_x, y=stand_y, z=stand_z - tool_length, relative=True, is_radian=False, wait=True)
    gripper.set_vacuum_gripper(on=True, wait=True)
    arm_movement.set_position(x=stand_x - (np.cos(np.radians(angle)) * 50), y=stand_y - (np.sin(np.radians(angle)) * 50), z=stand_z + tool_length, roll=180, pitch=0, yaw=0, relative=False, is_radian=False, wait=True)    

#pick_film(arm, film_x=200, film_y=0, film_z=20, tool_length=80)
#print(arm.get_vacuum_gripper())
#time.sleep(3)
#film_side_flip(arm, stand_x=300, stand_y=0, stand_z=300, angle=0, tool_length=80)
#film_upright_flip(arm, stand_x=300, stand_y=0, stand_z=300, angle=0, tool_length=80)
#film_stand_flip(arm, stand_x=300, stand_y=0, stand_z=300, angle=0, tool_length=80)

#film_stand_flip(arm, stand_x=0, stand_y=375, stand_z=300, angle=90, tool_length=80)
#film_stand_flip(arm, stand_x=-375, stand_y=0, stand_z=300, angle=180, tool_length=80)
#film_stand_flip(arm, stand_x=0, stand_y=-375, stand_z=300, angle=270, tool_length=80)