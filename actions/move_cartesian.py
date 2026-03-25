from xarm import XArmAPI

def reset(arm:XArmAPI):
    arm.reset()

class cartesian_control():

    def __init__(self, arm:XArmAPI):
        self.arm = arm
        pass

    def reset(self, speed=None, mvacc=None, mvtime=None, is_radian=None, wait=False, timeout=None):
        """
        Reset the xArm
        \nWarning: without limit detection
        \nNote:
            1. If there are errors or warnings, this interface will clear the warnings and errors.
            2. If not ready, the api will auto enable motion and set state
            3. This interface does not modify the value of last_used_angles/last_used_joint_speed/last_used_joint_acc

        :param speed: reset speed (unit: rad/s if is_radian is True else °/s), default is 50 °/s
        :param mvacc: reset acceleration (unit: rad/s^2 if is_radian is True else °/s^2), default is 5000 °/s^2
        :param mvtime: reserved
        :param is_radian: if the speed and acceleration are in radians or not, defaults to self.default_is_radian
        :param wait: whether to wait for the arm to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        """
        return self.arm.reset(speed=speed, mvacc=mvacc, mvtime=mvtime, is_radian=is_radian, wait=wait, timeout=timeout)

    def set_position(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None, radius=None,
                     speed=None, mvacc=None, mvtime=None, relative=False, is_radian=None,
                     wait=False, timeout=None, **kwargs):
        """
        Set the cartesian position, the API will modify self.last_used_position value

        Note:
            1. If it is xArm5, roll must be set to 180° or π rad, pitch must be set to 0
            2. If the parameter(roll/pitch/yaw) you are passing is an radian unit, set is_radian to True.
                ex: code = arm.set_position(x=300, y=0, z=200, roll=-3.14, pitch=0, yaw=0, is_radian=True)
            3. If you want to wait for the robot to complete this action and then return, set wait to True.
                ex: code = arm.set_position(x=300, y=0, z=200, roll=180, pitch=0, yaw=0, is_radian=False, wait=True)
            4. This interface is only used in the base coordinate system.

        :param x: cartesian position x, (mm), default is self.last_used_position[0]
        :param y: cartesian position y, (mm), default is self.last_used_position[1]
        :param z: cartesian position z, (mm), default is self.last_used_position[2]
        :param roll: rotate around the X axis, (unit: rad if is_radian is True else °), default is self.last_used_position[3]
        :param pitch: rotate around the Y axis, (unit: rad if is_radian is True else °), default is self.last_used_position[4]
        :param yaw: rotate around the Z axis, (unit: rad if is_radian is True else °), default is self.last_used_position[5]
        :param radius: move radius, if radius is None or radius less than 0, will MoveLine, else MoveArcLine
            MoveLine: Linear motion
                ex: code = arm.set_position(..., radius=None)
            MoveArcLine: Linear arc motion with interpolation
                ex: code = arm.set_position(..., radius=0)
                Note: Need to set radius>=0
        :param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        :param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        :param mvtime: 0, reserved
        :param relative: relative move or not
        :param is_radian: the roll/pitch/yaw in radians or not, default is self.default_is_radian
        :param wait: whether to wait for the arm to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        :param kwargs: extra parameters
            \n:param motion_type: motion planning type, default is 0
            \n    motion_type == 0: default, linear planning
            \n    motion_type == 1: prioritize linear planning, and turn to IK for joint planning when linear planning is not possible
            \n    motion_type == 2: direct transfer to IK using joint planning
            \n    Note: 
            \n        1. only available if firmware_version >= 1.11.100
            \n        2. when motion_type is 1 or 2, linear motion cannot be guaranteed
            \n        3. once IK is transferred to joint planning, the given Cartesian velocity and acceleration are converted into joint velocity and acceleration according to the percentage
            \n            speed = speed / max_tcp_speed * max_joint_speed
            \n            mvacc = mvacc / max_tcp_acc * max_joint_acc
            \n        4. if there is no suitable IK, a C40 error will be triggered
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \ncode < 0: the last_used_position/last_used_tcp_speed/last_used_tcp_acc will not be modified
                \ncode >= 0: the last_used_position/last_used_tcp_speed/last_used_tcp_acc will be modified
        """
        return self.arm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, radius=radius,
                                      speed=speed, mvacc=mvacc, mvtime=mvtime, relative=relative,
                                      is_radian=is_radian, wait=wait, timeout=timeout, **kwargs)
  
    def set_servo_angle(self, servo_id=None, angle=None, speed=None, mvacc=None, mvtime=None,
                        relative=False, is_radian=None, wait=False, timeout=None, radius=None, **kwargs):
        """
        Set the servo angle, the API will modify self.last_used_angles value

        Note:
        \n   1. If the parameter angle you are passing is an radian unit, be sure to set the parameter is_radian to True.
        \n        ex: code = arm.set_servo_angle(servo_id=1, angle=1.57, is_radian=True)
        \n    2. If you want to wait for the robot to complete this action and then return, please set the parameter wait to True.
        \n        ex: code = arm.set_servo_angle(servo_id=1, angle=45, is_radian=False,wait=True)
        \n    3. This interface is only used in the base coordinate system.

        \n:param servo_id: 1-(Number of axes), None(8)
        \n    1. 1-(Number of axes) indicates the corresponding joint, the parameter angle should be a numeric value
        \n        ex: code = arm.set_servo_angle(servo_id=1, angle=45, is_radian=False)
        \n    2. None(8) means all joints, default is None, the parameter angle should be a list of values whose length is the number of joints
        \n        ex: code = arm.set_servo_angle(angle=[30, -45, 0, 0, 0, 0, 0], is_radian=False)
        \n:param angle: angle or angle list, (unit: rad if is_radian is True else °)
        \n    1. If servo_id is 1-(Number of axes), angle should be a numeric value
        \n        ex: code = arm.set_servo_angle(servo_id=1, angle=45, is_radian=False)
        \n    2. If servo_id is None or 8, angle should be a list of values whose length is the number of joints
        \n        like [axis-1, axis-2, axis-3, axis-4, axis-5, axis-6, axis-7]
        \n        ex: code = arm.set_servo_angle(angle=[30, -45, 0, 0, 0, 0, 0], is_radian=False)
        \n:param speed: move speed (unit: rad/s if is_radian is True else °/s), default is self.last_used_joint_speed
        \n:param mvacc: move acceleration (unit: rad/s^2 if is_radian is True else °/s^2), default is self.last_used_joint_acc
        \n:param mvtime: 0, reserved
        \n:param relative: relative move or not
        \n:param is_radian: the angle in radians or not, default is self.default_is_radian
        \n:param wait: whether to wait for the arm to complete, default is False
        \n:param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        \n:param radius: move radius, if radius is None or radius less than 0, will MoveJoint, else MoveArcJoint
        \n    Note: Only available if version > 1.5.20
        \n    Note: The blending radius cannot be greater than the track length.
        \n    MoveJoint: joint motion
        \n        ex: code = arm.set_servo_angle(..., radius=None)
        \n    MoveArcJoint: joint fusion motion with interpolation
        \n        ex: code = arm.set_servo_angle(..., radius=0)
        \n        Note: Need to set radius>=0
        \n:param kwargs: reserved
        \n:return: code
        \n    code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \ncode < 0: the last_used_angles/last_used_joint_speed/last_used_joint_acc will not be modified
                \ncode >= 0: the last_used_angles/last_used_joint_speed/last_used_joint_acc will be modified
        """
        return self.arm.set_servo_angle(servo_id=servo_id, angle=angle, speed=speed, mvacc=mvacc, mvtime=mvtime,
                                         relative=relative, is_radian=is_radian, wait=wait, timeout=timeout, radius=radius, **kwargs)
    
    def get_servo_angle(self, servo_id=None, is_radian=None, is_real=False):
        """
        returns the servo angle

        Note:
            1. if value returned should be in radians, please set is_radian to True
            2. If you want to return only the angle of a single joint, please set the parameter servo_id
                ex: code, angle = arm.get_servo_angle(servo_id=2)
            3. This interface is only used in the base coordinate system.

        :param servo_id: 1-(Number of axes), None(8), default is None
        :param is_radian: the returned value is in radians or not, default is self.default_is_radian
        :return: tuple((code, angle list if servo_id is None or 8 else angle)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_angle(servo_id=servo_id, is_radian=is_radian, is_real=is_real)

    def set_servo_angle_j(self, angles, speed=None, mvacc=None, mvtime=None, is_radian=None, **kwargs):
        """
        Set the servo angle, execute only the last instruction, need to be set to servo motion mode(self.set_mode(1))

        Note:
            1. This interface does not modify the value of last_used_angles/last_used_joint_speed/last_used_joint_acc
            2. This interface is only used in the base coordinate system.

        :param angles: angle list, (unit: rad if is_radian is True else °)
        :param speed: speed, reserved
        :param mvacc: acceleration, reserved
        :param mvtime: 0, reserved
        :param is_radian: if the angles are in radians or not, default is self.default_is_radian
        :param kwargs: reserved
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_servo_angle_j(angles, speed=speed, mvacc=mvacc, mvtime=mvtime, is_radian=is_radian, **kwargs)
    
    def set_servo_cartesian(self, mvpose, speed=None, mvacc=None, mvtime=0, is_radian=None, is_tool_coord=False, **kwargs):
        """
        Set the servo to cartesian, execute only the last instruction, needs servo motion set to mode(self.set_mode(1))

        :param mvpose: cartesian position, [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)]
        :param speed: move speed (mm/s), reserved
        :param mvacc: move acceleration (mm/s^2), reserved
        :param mvtime: 0, reserved
        :param is_radian: if the roll/pitch/yaw of mvpose are in radians or not, default is self.default_is_radian
        :param is_tool_coord: is tool coordinate or not
        :param kwargs: reserved
        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_servo_cartesian(mvpose, speed=speed, mvacc=mvacc, mvtime=mvtime, is_radian=is_radian,
                                             is_tool_coord=is_tool_coord, **kwargs)
    
    def move_circle(self, pose1, pose2, percent, speed=None, mvacc=None, mvtime=None, is_radian=None,
                    wait=False, timeout=None, is_tool_coord=False, is_axis_angle=False, **kwargs):
        """
        The motion calculates the trajectory of the space circle according to the three-point coordinates.
        The three-point coordinates are (current starting point, pose1, pose2).


        :param pose1: cartesian position, [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)]
        :param pose2: cartesian position, [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)]
        :param percent: the percentage of arc length and circumference of the movement
        :param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        :param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        :param mvtime: 0, reserved
        :param is_radian: if roll/pitch/yaw values are in radians or not, default is self.default_is_radian
        :param wait: whether to wait for the arm to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        :param is_tool_coord: is tool coord or not, default is False, only available if firmware_version >= 1.11.100
        :param is_axis_angle: is axis angle or not, default is False, only available if firmware_version >= 1.11.100
        :param kwargs: reserved
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \n    code < 0: the last_used_tcp_speed/last_used_tcp_acc will not be modified
            \n    code >= 0: the last_used_tcp_speed/last_used_tcp_acc will be modified
        """
        return self._arm.move_circle(pose1, pose2, percent, speed=speed, mvacc=mvacc, mvtime=mvtime,
                                     is_radian=is_radian, wait=wait, timeout=timeout,
                                     is_tool_coord=is_tool_coord, is_axis_angle=is_axis_angle, **kwargs)

    def move_gohome(self, speed=None, mvacc=None, mvtime=None, is_radian=None, wait=False, timeout=None, **kwargs):
        """
        Move to go home (Back to zero)

        Warning: without limit detection

        Note:
            1. If you want to wait for the robot to complete it's current action and then return, set wait to True.
                ex: code = arm.move_gohome(wait=True)
            2. This interface does not modify the value of last_used_joint_speed/last_used_joint_acc

        :param speed: gohome speed (unit: rad/s if is_radian is True else °/s), default is 50 °/s
        :param mvacc: gohome acceleration (unit: rad/s^2 if is_radian is True else °/s^2), default is 5000 °/s^2
        :param mvtime: reserved
        :param is_radian: if the speed and acceleration are in radians or not, default is self.default_is_radian
        :param wait: whether to wait for the arm to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.move_gohome(speed=speed, mvacc=mvacc, mvtime=mvtime, is_radian=is_radian, wait=wait, timeout=timeout, **kwargs)
    
    def emergency_stop(self):
        """
        Emergency stop (set_state(4) -> motion_enable(True) -> set_state(0))

        \nNote:
            1. This interface does not automatically clear errors. If there is an error, you will need to handle it according to the error code.
        """
        return self.arm.emergency_stop()
    
    def set_position_aa(self, axis_angle_pose, speed=None, mvacc=None, mvtime=None,
                        is_radian=None, is_tool_coord=False, relative=False, wait=False, timeout=None, radius=None, **kwargs):
        """
        Set the pose represented by the axis angle pose
        
        \n:param axis_angle_pose: the axis angle pose, [x(mm), y(mm), z(mm), rx(rad or °), ry(rad or °), rz(rad or °)]
        \n:param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        \n:param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        \n:param mvtime: 0, reserved 
        \n:param is_radian: if the rx/ry/rz of axis_angle_pose are in radians or not, default is self.default_is_radian
        \n:param is_tool_coord: is tool coordinate or not, if True, the relative parameter is no longer valid
        \n:param relative: relative move or not
        \n:param wait: whether to wait for the arm to complete, default is False
        \n:param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        \n:param radius: move radius, if radius is None or radius less than 0, will MoveLineAA, else MoveArcLineAA
        \n    only available if firmware_version >= 1.11.100
        \n    MoveLineAA: Linear motion
        \n        ex: code = arm.set_position_aa(..., radius=None)
        \n    MoveArcLineAA: Linear arc motion with interpolation
        \n        ex: code = arm.set_position_aa(..., radius=0)
        \n        Note: Need to set radius>=0
        \n:param kwargs: extra parameters
        \n    :param motion_type: motion planning type, default is 0
        \n        motion_type == 0: default, linear planning
        \n        motion_type == 1: prioritize linear planning, and turn to IK for joint planning when linear planning is not possible
        \n        motion_type == 2: direct transfer to IK using joint planning
        \n        Note: 
        \n            1. only available if firmware_version >= 1.11.100
        \n            2. when motion_type is 1 or 2, linear motion cannot be guaranteed
        \n            3. once IK is transferred to joint planning, the given Cartesian velocity and acceleration are converted into joint velocity and acceleration according to the percentage
        \n                speed = speed / max_tcp_speed * max_joint_speed
        \n                mvacc = mvacc / max_tcp_acc * max_joint_acc
        \n            4. if there is no suitable IK, a C40 error will be triggered
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_position_aa(axis_angle_pose, speed=speed, mvacc=mvacc, mvtime=mvtime,
                                         is_radian=is_radian, is_tool_coord=is_tool_coord, relative=relative,
                                         wait=wait, timeout=timeout, radius=radius, **kwargs)

    def set_servo_cartesian_aa(self, axis_angle_pose, speed=None, mvacc=None, is_radian=None, is_tool_coord=False, relative=False, **kwargs):
        """
        Set the servo cartesian represented by the axis angle pose, execute only the last instruction, needs servo motion set to mode(self.set_mode(1))

        Note:
            1. only available if firmware_version >= 1.4.7

        :param axis_angle_pose: the axis angle pose, [x(mm), y(mm), z(mm), rx(rad or °), ry(rad or °), rz(rad or °)]
        :param speed: move speed (mm/s), reserved
        :param mvacc: move acceleration (mm/s^2), reserved
        :param is_radian: if the rx/ry/rz of axis_angle_pose are in radians or not, default is self.default_is_radian
        :param is_tool_coord: is tool coordinate or not
        :param relative: relative move or not
        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """

        return self.arm.set_servo_cartesian_aa(axis_angle_pose, speed=speed, mvacc=mvacc, is_radian=is_radian,
                                                is_tool_coord=is_tool_coord, relative=relative, **kwargs)
    
    def vc_set_joint_velocity(self, speeds, is_radian=None, is_sync=True, duration=-1, **kwargs):
        """
        Joint velocity control, need to be in joint velocity control mode(self.set_mode(4))

        Note:
            1. only available if firmware_version >= 1.6.9
        
        :param speeds: [spd_J1, spd_J2, ..., spd_J7]
        :param is_radian: if the spd_Jx is in radians or not, default is self.default_is_radian
        :param is_sync: whether all joints accelerate and decelerate synchronously, default is True
        :param duration: The duration of this speed command, over this time will automatically set the speed to 0

            Note: only available if firmware_version >= 1.8.0

            duration > 0: seconds

            duration == 0: Always effective, will not stop automatically

            duration < 0: default value, only used to be compatible with the old protocol, equivalent to 0

        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.vc_set_joint_velocity(speeds, is_radian=is_radian, is_sync=is_sync, duration=duration, **kwargs)

    def vc_set_cartesian_velocity(self, speeds, is_radian=None, is_tool_coord=False, duration=-1, **kwargs):
        """
        Cartesian velocity control, need to be in cartesian velocity control mode(self.set_mode(5))
        
        Note:
            1. only available if firmware_version >= 1.6.9
            
        :param speeds: [spd_x, spd_y, spd_z, spd_rx, spd_ry, spd_rz]
        :param is_radian: if the spd_rx/spd_ry/spd_rz are in radians or not, default is self.default_is_radian
        :param is_tool_coord: is tool coordinate or not, default is False
        :param duration: the maximum duration of the speed, over this time will automatically set the speed to 0

            Note: only available if firmware_version >= 1.8.0

            duration > 0: seconds, indicates the maximum number of seconds that this speed can be maintained

            duration == 0: Always effective, will not stop automatically

            duration < 0: default value, only used to be compatible with the old protocol, equivalent to 0

        :return: code
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.vc_set_cartesian_velocity(speeds, is_radian=is_radian, is_tool_coord=is_tool_coord, duration=duration, **kwargs)
    
    def get_linear_motor_registers(self, **kwargs):
        """
        Get the status of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :return: tuple((code, status)), returned result is only corrent when code is 0.

            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: status, like
                {
                    'pos': 0,
                    'status': 0,
                    'error': 0,
                    'is_enabled': 0,
                    'on_zero': 0,
                    'sci': 1,
                    'sco': [0, 0],
                }
        """
        return self.arm.get_linear_motor_registers(**kwargs)

    def get_linear_motor_pos(self):
        """
        Get the pos of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0
        :return: tuple((code, position)) returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nposition: position
        """
        return self.arm.get_linear_motor_pos()

    def get_linear_motor_status(self):
        """
        Get the status of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0

        :return: tuple((code, status)), returned result is only corrent when code is 0.

            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: status

                status & 0x00: motion finish

                status & 0x01: in motion

                status & 0x02: has stop
        """
        return self.arm.get_linear_motor_status()

    def get_linear_motor_error(self):
        """
        Get the error code of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0

        :return: tuple((code, error)), returned result is only corrent when code is 0.

            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            error: See the [Linear Motor Error Code Documentation](./xarm_api_code.md#linear-motor-error-code) for details.
        """
        return self.arm.get_linear_motor_error()

    def get_linear_motor_is_enabled(self):
        """
        Get if the linear motor is enabled or not

        Note:
            1. only available if firmware_version >= 1.8.0

        :return: tuple((code, status)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: 
               0: linear motor is not enabled
               1: linear motor is enabled
        """
        return self.arm.get_linear_motor_is_enabled()

    def get_linear_motor_on_zero(self):
        """
        Get if the linear motor is on zero positon or not

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :return: tuple((code, status)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: 
                0: linear motor is not on zero
                1: linear motor is on zero
        """
        return self.arm.get_linear_motor_on_zero()

    def get_linear_motor_sci(self):
        """
        Get the sci1 value of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0

        :return: tuple((code, sci1)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_linear_motor_sci()

    def get_linear_motor_sco(self):
        """
        Get the sco value of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0

        :return: tuple((code, sco)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            sco: [sco0, sco1]
        """
        return self.arm.get_linear_motor_sco()
    
    def clean_linear_motor_error(self):
        """
        Clean the linear motor error

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_linear_motor_error()

    def set_linear_motor_enable(self, enable):
        """
        Set the linear motor enable/disable

        Note:
            1. only available if firmware_version >= 1.8.0

        :param enable: enable or not
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_motor_enable(enable)

    def set_linear_motor_speed(self, speed):
        """
        Set the speed of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :param speed: Integer between 1 and 1000mm/s.
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_motor_speed(speed)

    def set_linear_motor_back_origin(self, wait=True, **kwargs):
        """
        Set the linear motor to go back to the origin position

        Note:
            1. only available if firmware_version >= 1.8.0
            2. only useful when powering on for the first time
            3. this operation must be performed at the first power-on
            
        :param wait: wait to motion finish or not, default is True
        :param kwargs:
            auto_enable: enable after back to origin or not, default is True
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_motor_back_origin(wait=wait, **kwargs)

    def set_linear_motor_pos(self, pos, speed=None, wait=True, timeout=100, **kwargs):
        """
        Set the position of the linear motor

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :param pos: position. Integer between 0 and 700/1000/1500mm.

            If SN start with AL1300 the position range is 0~700mm.

            If SN start with AL1301 the position range is 0~1000mm.

            If SN start with AL1302 the position range is 0~1500mm.

        :param speed: speed of the linear motor. Integer between 1 and 1000mm/s. default is not set
        :param wait: wait to motion finish or not, default is True
        :param timeout: wait timeout, seconds, default is 100s.
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_motor_pos(pos, speed=speed, wait=wait, timeout=timeout, **kwargs)

    def set_linear_motor_stop(self):
        """
        Set the linear motor to stop

        Note:
            1. only available if firmware_version >= 1.8.0
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_motor_stop()
    
    def set_tool_position(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0,
                          speed=None, mvacc=None, mvtime=None, is_radian=None,
                          wait=False, timeout=None, radius=None, **kwargs):
        """
        Movement relative to the tool coordinate system

        Note:
            1. This interface is moving relative to the current tool coordinate system
            2. The tool coordinate system is not fixed and varies with position.
            3. This interface is only used in the tool coordinate system.


        \n:param x: the x coordinate relative to the current tool coordinate system, (unit: mm), default 0
        \n:param y: the y coordinate relative to the current tool coordinate system, (unit: mm), default 0
        \n:param z: the z coordinate relative to the current tool coordinate system, (unit: mm), default 0
        \n:param roll: the rotation around the X axis relative to the current tool coordinate system, (unit: rad if is_radian is True else °), default is 0
        \n:param pitch: the rotation around the Y axis relative to the current tool coordinate system, (unit: rad if is_radian is True else °), default is 0
        \n:param yaw: the rotation around the Z axis relative to the current tool coordinate system, (unit: rad if is_radian is True else °), default is 0
        \n:param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        \n:param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        \n:param mvtime: 0, reserved
        \n:param is_radian: if the roll/pitch/yaw are in radians or not, default is self.default_is_radian
        \n:param wait: whether to wait for the arm to complete, default is False
        \n:param timeout: maximum waiting time(unit: second), default is None(no timeout), only valid if wait is True
        \n:param radius: move radius, if radius is None or radius less than 0, will MoveToolLine, else MoveToolArcLine
        \n    only available if firmware_version >= 1.11.100
        \n    MoveToolLine: Linear motion
        \n        ex: code = arm.set_tool_position(..., radius=None)
        \n    MoveToolArcLine: Linear arc motion with interpolation
        \n        ex: code = arm.set_tool_position(..., radius=0)
        \n        Note: Need to set radius>=0
        \n:param kwargs: extra parameters
        \n    :param motion_type: motion planning type, default is 0
        \n        motion_type == 0: default, linear planning
        \n        motion_type == 1: prioritize linear planning, and turn to IK for joint planning when linear planning is not possible
        \n        motion_type == 2: direct transfer to IK using joint planning
        \n        Note: 
        \n            1. only available if firmware_version >= 1.11.100
        \n            2. when motion_type is 1 or 2, linear motion cannot be guaranteed
        \n            3. once IK is transferred to joint planning, the given Cartesian velocity and acceleration are converted into joint velocity and acceleration according to the percentage
        \n                speed = speed / max_tcp_speed * max_joint_speed
        \n                mvacc = mvacc / max_tcp_acc * max_joint_acc
        \n            4. if there is no suitable IK, a C40 error will be triggered
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.    
            \n    code < 0: the last_used_tcp_speed/last_used_tcp_acc will not be modified
            \n    code >= 0: the last_used_tcp_speed/last_used_tcp_acc will be modified
        """
        return self.arm.set_tool_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw, speed=speed, mvacc=mvacc, mvtime=mvtime, is_radian=is_radian, wait=wait, timeout=timeout, radius=radius, **kwargs)
    
    def move_arc_lines(self, paths, is_radian=None, times=1, first_pause_time=0.1, repeat_pause_time=0,
                       automatic_calibration=True, speed=None, mvacc=None, mvtime=None, wait=False):
        """
        Continuous linear motion with interpolation.

        Note:
            1. If an error occurs, it will return early.
            2. If the emergency_stop interface is called actively, it will return early.
            3. The last_used_position/last_used_tcp_speed/last_used_tcp_acc will be modified.
            4. The last_used_angles/last_used_joint_speed/last_used_joint_acc will not be modified.

        :param paths: cartesian path list
        \n    1. Specify arc radius: [[x, y, z, roll, pitch, yaw, radius], ....]
        \n    2. Do not specify arc radius (radius=0): [[x, y, z, roll, pitch, yaw], ....]
        \n    3. If you want to plan the continuous motion,set radius>0.

        :param is_radian: if roll/pitch/yaw of the paths are in radians or not, default is self.default_is_radian
        :param times: amount of times to repeat, 0 is infinite loop, default is 1
        :param first_pause_time: sleep time at first, purpose is to cache the commands and plan continuous motion, default is 0.1s
        :param repeat_pause_time: interval between repeated movements, unit: (s)second
        :param automatic_calibration: automatic calibration or not, default is True
        :param speed: move speed (mm/s, rad/s), default is self.last_used_tcp_speed
        :param mvacc: move acceleration (mm/s^2, rad/s^2), default is self.last_used_tcp_acc
        :param mvtime: 0, reserved
        :param wait: whether to wait for the arm to complete, default is False
        """
        return self.arm.move_arc_lines(paths, is_radian=is_radian, times=times, first_pause_time=first_pause_time,
                                        repeat_pause_time=repeat_pause_time, automatic_calibration=automatic_calibration,
                                        speed=speed, mvacc=mvacc, mvtime=mvtime, wait=wait)
    
    def get_trajectories(self):
        """
        Get the trajectories

        \nNote:
        \n    1. This interface relies on xArmStudio 1.2.0 or above
        \n    2. This interface relies on Firmware 1.2.0 or above

        \n:return: tuple((code, trajectories))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \ntrajectories: [{
            \n    'name'- name, # The name of the trajectory
            \n    'duration'- duration, # The duration of the trajectory (seconds)
            }]
        """
        return self.arm.get_trajectories()
    
    def set_world_offset(self, offset, is_radian=None, wait=True):
        """
        Set the base coordinate offset

        Note:
            1. This interface relies on Firmware 1.2.11 or above

        :param offset: [x, y, z, roll, pitch, yaw]
        :param is_radian: if the roll/pitch/yaw are in radians or not, default is self.default_is_radian
        :param wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed or cleared before setting
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_world_offset(offset, is_radian=is_radian, wait=wait)
    
    def get_pose_offset(self, pose1, pose2, orient_type_in=0, orient_type_out=0, is_radian=None):
        """
        Calculate the pose offset of two given points
        
        :param pose1: [x(mm), y(mm), z(mm), roll/rx(rad or °), pitch/ry(rad or °), yaw/rz(rad or °)]
        :param pose2: [x(mm), y(mm), z(mm), roll/rx(rad or °), pitch/ry(rad or °), yaw/rz(rad or °)]
        :param orient_type_in: input attitude notation, 0 is RPY(roll/pitch/yaw) (default), 1 is axis angle(rx/ry/rz)
        :param orient_type_out: notation of output attitude, 0 is RPY (default), 1 is axis angle
        :param is_radian: if the roll/rx/pitch/ry/yaw/rz of pose1/pose2/return_pose is radian or not
        :return: tuple((code, pose)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \npose: [x(mm), y(mm), z(mm), roll/rx(rad or °), pitch/ry(rad or °), yaw/rz(rad or °)]
        """
        return self.arm.get_pose_offset(pose1, pose2, orient_type_in=orient_type_in, orient_type_out=orient_type_out,
                                         is_radian=is_radian)
    
    def get_position_aa(self, is_radian=None):
        """
        Get the pose represented by the axis angle pose
        
        :param is_radian: the returned value (only rx/ry/rz) is in radians or not, default is self.default_is_radian
        :return: tuple((code, [x, y, z, rx, ry, rz])), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_position_aa(is_radian=is_radian)
    
    def set_cartesian_velo_continuous(self, on_off):
        """
        Set cartesian motion velocity continuous

        Note:
            1. only available if firmware_version >= 1.9.0
        
        :param on_off: continuous or not, True means continuous, default is False
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_cartesian_velo_continuous(on_off)