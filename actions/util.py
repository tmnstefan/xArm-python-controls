from xarm import XArmAPI

class arm_utilities():
    def __init__(self, arm:XArmAPI):
        self.arm = arm

    def connect(self, port=None, baudrate=None, timeout=None, axis=None, **kwargs):
        """
        Connect to arm

        \n:param port: port name or ip address, default is the value when initializing an instance
        \n:param baudrate: baudrate, only available in serial, default is the value when initializing an instance
        \n:param timeout: timeout, only available in serial, default is the value when initializing an instance
        \n:param axis: number of axes, only required when using a serial port connection, default is 7
        """
        self.arm.connect(port=port, baudrate=baudrate, timeout=timeout, axis=axis, **kwargs)

    def disconnect(self):
        """
        Disconnect
        """
        self.arm.disconnect()

    def set_servo_attach(self, servo_id=None):
        """
        Attach the servo

        \n:param servo_id: 1-(Number of axes), 8, if servo_id is 8, will attach all servo
        \n    1. 1-(Number of axes): attach only one joint
        \n        ex: arm.set_servo_attach(servo_id=1)
        \n    2: 8: attach all joints
        \n        ex: arm.set_servo_attach(servo_id=8)
        \n:return: code
        \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_servo_attach(servo_id=servo_id)

    def set_servo_detach(self, servo_id=None):
        """
        Detaches the servo, be sure to do protective work before unlocking to avoid injury or damage.

        \n:param servo_id: 1-(Number of axes), 8, if servo_id is 8, will detach all servo
        \n    1. 1-(Number of axes): detach only one joint
        \n        ex: arm.set_servo_detach(servo_id=1)
        \n    2: 8: detach all joints, please
        \n        ex: arm.set_servo_detach(servo_id=8)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_servo_detach(servo_id=servo_id)
    
    def set_state(self, state=0):
        """
        Set the xArm state

        \n:param state: default 0
        \n    0: motion state
        \n    3: pause state
        \n    4: stop state
        \n    6: deceleration stop state
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_state(state=state)

    def set_mode(self, mode=0, detection_param=0):
        """
        Set the xArm mode

        \n:param mode: default 0
        \n    0: position control
        \n    1: servo motion
        \n        Note: the use of the set_servo_angle_j interface must first be set to this
        \n        Note: the use of the set_servo_cartesian interface must first be set to this
        \n    2: joint teaching
        \n        Note: use this mode to ensure that the arm has been identified and the control box and arm used for identification are one-to-one.
        \n    3: cartesian teaching (invalid)
        \n    4: joint velocity control
        \n    5: cartesian velocity control
        \n    6: joint online trajectory planning
        \n    7: cartesian online trajectory planning
        \n:param detection_param: Teaching detection parameters, default is 0
        \n    0: motion detection on
        \n    1: motion detection off
        \n    Note:
        \n        1. only available if firmware_version >= 1.10.1
        \n        2. only available if set_mode(2)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_mode(mode=mode, detection_param=detection_param)
    
    def motion_enable(self, enable=True, servo_id=None):
        """
        Enable motion

        \n:param enable: True/False
        \n:param servo_id: 1-(Number of axes), None(8)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.motion_enable(servo_id=servo_id, enable=enable)
    
    def set_pause_time(self, sltime, wait=False):
        """
        Set the arm pause time, xArm will pause sltime second

        \n:param sltime: sleep time,unit:(s)second
        \n:param wait: wait or not, default is False
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_pause_time(sltime=sltime, wait=wait)
    
    def get_version(self):
        """
        Get the xArm firmware version

        \n:return: tuple((code, version)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_version()
    
    def get_state(self):
        """
        Get state

        \n:return: tuple((code, state)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstate:
            \n1: in motion
            \n2: sleeping
            \n3: suspended
            \n4: stopping
        """
        return self.arm.get_state()
    
    def get_is_moving(self):
        """
        Check if the arm is moving or not

        \n:return: True/False
        """
        return self.arm.get_is_moving()
    
    def get_cmdnum(self):
        """
        Get the cmd count in cache

        \n:return: tuple((code, cmd_num)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_cmdnum()

    def get_err_warn_code(self, show=False, lang='en'):
        """
        Get the controller error and warn code

        \n:param show: show the detail info if True
        \n:param lang: show language, en/cn, degault is en, only available if show is True
        \n:return: tuple((code, [error_code, warn_code])), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerror_code: See the [Controller Error Code Documentation](./xarm_api_code.md#controller-error-code) for details.
            \nwarn_code: See the [Controller Warn Code Documentation](./xarm_api_code.md#controller-warn-code) for details.
        """
        return self.arm.get_err_warn_code(show=show, lang=lang)
    
    def clean_error(self):
        """
        Clean the error, need to manually enable motion(arm.motion_enable(True)) and set state(arm.set_state(state=0)) after error cleaned

        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_error()

    def clean_warn(self):
        """
        Clean the warn

        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_warn()
    
    def get_position(self, is_radian=None):
        """
        Get the cartesian position

        \nNote:
        \n1. If the value(roll/pitch/yaw) you want returned should be in radians, set is_radian to True
        \n ex: code, pos = arm.get_position(is_radian=True)

        \n:param is_radian: if the returned value (only roll/pitch/yaw) is in radians or not, defaults to self.default_is_radian
        \n:return: tuple((code, [x, y, z, roll, pitch, yaw])), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_position(is_radian=is_radian)
    
    def get_servo_angle(self, servo_id=None, is_radian=None, is_real=False):
        """
        Get the servo angle
        \nNote:
        \n1. If the value you want returned should be in radians, set is_radian to True
        \n  ex: code, angles = arm.get_servo_angle(is_radian=True)
        \n2. If you want to return only the angle of a single joint, please set the parameter servo_id
        \n  ex: code, angle = arm.get_servo_angle(servo_id=2)
        \n3. This interface is only used in the base coordinate system.

        \n:param servo_id: 1-(Number of axes), None(8), default is None
        \n:param is_radian: the returned value is in radians or not, defaults to self.default_is_radian
        \n:return: tuple((code, angle list if servo_id is None or 8 else angle)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_angle(servo_id=servo_id, is_radian=is_radian, is_real=is_real)
    
    def get_position_aa(self, is_radian=None):
        """
        Get the pose represented by the axis angle pose
        
        \n:param is_radian: if the returned value (only rx/ry/rz) is in radians or not, defaults to self.default_is_radian
        \n:return: tuple((code, [x, y, z, rx, ry, rz])), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_position_aa(is_radian=is_radian)
    
    def get_pose_offset(self, pose1, pose2, orient_type_in=0, orient_type_out=0, is_radian=None):
        """
        Calculate the pose offset of two given points

        \nNote:
        \n1. x, y, z are all in mm
        \n2. roll/rx, pitch/ry, yaw/rz are in either degrees or radians, can be selected by changing parameter is_radian
        
        \n:param pose1: [x, y, z, roll/rx, pitch/ry, yaw/rz]
        \n:param pose2: [x, y, z, roll/rx, pitch/ry, yaw/rz]
        \n:param orient_type_in: input attitude notation, 0 is RPY(roll/pitch/yaw) (default), 1 is axis angle(rx/ry/rz)
        \n:param orient_type_out: notation of output attitude, 0 is RPY (default), 1 is axis angle
        \n:param is_radian: if the roll/rx/pitch/ry/yaw/rz of pose1/pose2/return_pose is in radians or not
        \n:return: tuple((code, pose)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \npose: [x(mm), y(mm), z(mm), roll/rx(rad or °), pitch/ry(rad or °), yaw/rz(rad or °)]
        """
        return self.arm.get_pose_offset(pose1, pose2, orient_type_in=orient_type_in, orient_type_out=orient_type_out, is_radian=is_radian)
    
    def set_tcp_offset(self, offset, is_radian=None, wait=True, **kwargs):
        """
        Set the tool coordinate system offset at the end

        \nNote:
        \n1. Do not use if not required
        \n2. If not saved and you want to revert to the last saved value, please reset the offset by set_tcp_offset([0, 0, 0, 0, 0, 0])
        \n3. If not saved, it will be lost after reboot
        \n4. The save_conf interface can record the current settings and will not be lost after the restart.
        \n5. The clean_conf interface can restore system default settings

        \n:param offset: [x, y, z, roll, pitch, yaw]
        \n:param is_radian: the roll/pitch/yaw in radians or not, defaults to self.default_is_radian
        \n:param wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed or cleared before setting
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_offset(offset, is_radian=is_radian, wait=wait, **kwargs)

    def set_tcp_jerk(self, jerk):
        """
        Set the translational jerk of Cartesian space
        
        \nNote:
        \n1. Do not use if not required
        \n2. If not saved, it will be lost after reboot
        \n3. The save_conf interface can record the current settings and will not be lost after the restart.
        \n4. The clean_conf interface can restore system default settings

        \n:param jerk: jerk (mm/s^3)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_jerk(jerk)

    def set_tcp_maxacc(self, acc):
        """
        Set the max translational acceleration of Cartesian space
        
        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param acc: max acceleration (mm/s^2)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_maxacc(acc)

    def set_joint_jerk(self, jerk, is_radian=None):
        """
        Set the jerk of Joint space

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param jerk: jerk (°/s^3 or rad/s^3)
        \n:param is_radian: if the jerk is in radians or not, defaults to self.default_is_radian
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_joint_jerk(jerk, is_radian=is_radian)

    def set_joint_maxacc(self, acc, is_radian=None):
        """
        Set the max acceleration of Joint space

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param acc: max acceleration (°/s^2 or rad/s^2)
        \n:param is_radian: if the jerk is in radians or not, defaults to self.default_is_radian
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_joint_maxacc(acc, is_radian=is_radian)

    def set_tcp_load(self, weight, center_of_gravity, wait=False, **kwargs):
        """
        Set the end load of xArm

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param weight: load weight (unit: kg)
        \n:param center_of_gravity: load center of gravity, such as [x(mm), y(mm), z(mm)]
        \n:param wait: whether to wait for the command to be executed or for the robotic arm to stop
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_load(weight, center_of_gravity, wait=wait, **kwargs)

    def set_collision_sensitivity(self, value, wait=True):
        """
        Set the sensitivity to collision

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param value: sensitivity value, 0~5
        \n:param wait: reversed
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_sensitivity(value, wait=wait)

    def set_teach_sensitivity(self, value, wait=True):
        """
        Set the sensitivity of drag and teach

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param value: sensitivity value, 1~5
        \n:param wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed or cleared before setting
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_teach_sensitivity(value, wait=wait)

    def set_gravity_direction(self, direction, wait=True):
        """
        Set the gravity direction for proper torque compensation and collision detection.

        \nNote:
        \n1. Use only if necessary. Incorrect settings may affect torque compensation.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.

        \n:param direction: Gravity direction vector [x, y, z], e.g., [0, 0, -1] for a floor-mounted arm.
        \n:param wait: Whether to wait for the robotic arm to stop or clear all previous queued commands before applying the setting.
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gravity_direction(direction=direction, wait=wait)

    def set_mount_direction(self, base_tilt_deg, rotation_deg, is_radian=None):
        """
        Set the mount direction

        \nNote:
        \n1. Use only if necessary.
        \n2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
        \n3. Use clean_conf() to restore the system default settings.
        \n:param base_tilt_deg: tilt degree
        \n:param rotation_deg: rotation degree
        \n:param is_radian: if the base_tilt_deg/rotation_deg is in radians or not, defaults to self.default_is_radian
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_mount_direction(base_tilt_deg, rotation_deg, is_radian=is_radian)

    def clean_conf(self):
        """
        Clean current config and restore system default settings

        \nNote:
        \n1. This interface will clear the current settings and restore to the system default settings

        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_conf()

    def save_conf(self):
        """
        Save config

        \nNote:
        \n1. This interface can record the current settings and will not be lost after the restart.
        \n2. The clean_conf interface can restore system default settings

        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.save_conf()

    def get_inverse_kinematics(self, pose, input_is_radian=None, return_is_radian=None, limited=True, ref_angles=None):
        """
        Get inverse kinematics

        \nNote: the roll/pitch/yaw unit is radian if input_is_radian is True, else °

        \n:param pose: [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)]
        \n:param input_is_radian: if the param pose value(only roll/pitch/yaw) is in radians or not, defaults to self.default_is_radian
        \n:param return_is_radian: if the returned value should be in radians or not, defaults to self.default_is_radian
        \n:param limited: if the result is limited to within ±180° or not, default is True(only available if firmware_version >= 2.7.103)
        \n:param ref_angles: reference values for joint angles
            \nNote: unit is radian if input_is_radian is True, else °
            \nNote: only available if firmware_version >= 2.7.103
        \n:return: tuple((code, angles)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nangles: [angle-1(rad or °), angle-2, ..., angle-(Number of axes)] or []
                \nNote: the returned angle value is radians if return_is_radian is True, else °
        """
        return self.arm.get_inverse_kinematics(pose, input_is_radian=input_is_radian, return_is_radian=return_is_radian, limited=limited, ref_angles=ref_angles)

    def get_forward_kinematics(self, angles, input_is_radian=None, return_is_radian=None):
        """
        Get forward kinematics

        \n:param angles: [angle-1, angle-2, ..., angle-n], n is the number of axes of the arm
        \n:param input_is_radian: the param angles value is in radians or not, defaults to self.default_is_radian
        \n:param return_is_radian: the returned value is in radians or not, defaults to self.default_is_radian
        \n:return: tuple((code, pose)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \npose: [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)] or []
            \nNote: the roll/pitch/yaw value is radians if return_is_radian is True, else °
        """
        return self.arm.get_forward_kinematics(angles, input_is_radian=input_is_radian, return_is_radian=return_is_radian)
    
    def set_tgpio_digital_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the digital value of the specified Tool GPIO when the robot has reached the specified xyz position           
        
        :param ionum: 0 or 1
        :param value: value
        :param xyz: position xyz, as [x, y, z]
        :param fault_tolerance_radius: fault tolerance radius
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details. 
        """
        return self.arm.set_tgpio_digital_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def set_cgpio_digital_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the digital value of the specified Controller GPIO when the robot has reached the specified xyz position           
        
        :param ionum: 0 ~ 15
        :param value: value
        :param xyz: position xyz, as [x, y, z]
        :param fault_tolerance_radius: fault tolerance radius
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.  
        """
        return self.arm.set_cgpio_digital_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def set_cgpio_analog_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the analog value of the specified Controller GPIO when the robot has reached the specified xyz position           

        :param ionum: 0 ~ 1
        :param value: value
        :param xyz: position xyz, as [x, y, z]
        :param fault_tolerance_radius: fault tolerance radius
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.  
        """
        return self.arm.set_cgpio_analog_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def config_tgpio_reset_when_stop(self, on_off):
        """
        Configure the Tool GPIO reset the digital output when the robot is in stop state
        
        :param on_off: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.config_io_reset_when_stop(1, on_off)

    def config_cgpio_reset_when_stop(self, on_off):
        """
        Configure the Controller GPIO reset the digital output when the robot is in stop state

        :param on_off: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.config_io_reset_when_stop(0, on_off)
    
    def set_report_tau_or_i(self, tau_or_i=0):
        """
        Set if torque or electric current is reported
        
        :param tau_or_i: 
            0: torque
            1: electric current
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_report_tau_or_i(tau_or_i=tau_or_i)

    def get_report_tau_or_i(self):
        """
        Get the reported torque or electric current
        
        :return: tuple((code, tau_or_i))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            tau_or_i: 
                0: torque
                1: electric current
        """
        return self.arm.get_report_tau_or_i()

    def set_self_collision_detection(self, on_off):
        """
        Set whether to enable self-collision detection 
        
        :param on_off: enable or not
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_self_collision_detection(on_off)

    def set_collision_tool_model(self, tool_type, *args, **kwargs):
        """
        Set the geometric model of the end effector for self collision detection
         
        :param tool_type: the geometric model type
        \n    0: No end effector, no additional parameters required
        \n    1: xArm Gripper, no additional parameters required
        \n    2: xArm Vacuum Gripper, no additional parameters required
        \n    3: xArm Bio Gripper, no additional parameters required
        \n    4: Robotiq-2F-85 Gripper, no additional parameters required
        \n    5: Robotiq-2F-140 Gripper, no additional parameters required
        \n    7: Lite Gripper, no additional parameters required
        \n    8: Lite Vacuum Gripper, no additional parameters required
        \n    9: xArm Gripper G2, no additional parameters required
        \n    10: PGC-140-50 of the DH-ROBOTICS, no additional parameters required
        \n    11: RH56DFX-2L of the INSPIRE-ROBOTS, no additional parameters required
        \n    12: RH56DFX-2R of the INSPIRE-ROBOTS, no additional parameters required
        \n    13: xArm Bio Gripper G2, no additional parameters required
        \n    21: Cylinder, need additional parameters radius, height 
        \n        ex: self.set_collision_tool_model(21, radius=45, height=137)
        \n        radius: the radius of cylinder, (mm)
        \n        height: the height of cylinder, (mm)
        \n        x_offset: offset in the x direction, (mm)
        \n        y_offset: offset in the y direction, (mm)
        \n        z_offset: offset in the z direction, (mm)
        \n    22: Cuboid, need additional parameters x, y, z
        \n        ex: self.set_collision_tool_model(22, x=234, y=323, z=23)
        \n        x: the length of the cuboid in the x coordinate direction, (mm)
        \n        y: the length of the cuboid in the y coordinate direction, (mm)
        \n        z: the length of the cuboid in the z coordinate direction, (mm)
        \n        x_offset: offset in the x direction, (mm)
        \n        y_offset: offset in the y direction, (mm)
        \n        z_offset: offset in the z direction, (mm)
        \n:param args: additional parameters
        \n:param kwargs: additional parameters
        \n:return: code
        \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_tool_model(tool_type, *args, **kwargs)
    
    def get_robot_sn(self):
        """
        Gets the xArm sn

        :return: tuple((code, sn)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_robot_sn()
    
    def check_verification(self):
        """
        checks verification

        :return: tuple((code, status)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            status:
                0: verified
                other: not verified
        """
        return self.arm.check_verification()
    
    def system_control(self, value=1):
        """
        Control the xArm controller system

        :param value: 1: shutdown, 2: reboot
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.system_control(value=value)
    
    def get_record_seconds(self):
        """
        Get record seconds
        \nNote:
            1. Only available if firmware_version >= 2.4.0
            2. Only valid during recording or after recording but before saving

        :return: tuple((code, seconds)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            seconds: The actual duration of the recorded trajectory
        """
        ret = self.arm.get_common_info(50, return_val=True)
        return ret
    
    def save_record_trajectory(self, filename, wait=True, timeout=5, **kwargs):
        """
        Save the trajectory you just recorded

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        :param filename: The name to save
        \n    1. Only strings consisting of standard English characters or numbers are supported, with a maximum length of 50.
        \n    2. The trajectory will be saved in the controller box.
        \n    3. This action will overwrite a trajectory with the same name
        \n    4. Empty the trajectory in memory after saving, so repeated calls will cause the recorded trajectory to be covered by an empty trajectory.
        \n:param wait: Whether to wait for saving, default is True
        \n:param timeout: Timeout waiting for saving to complete
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.save_record_trajectory(filename, wait=wait, timeout=timeout, **kwargs)
    
    def start_record_trajectory(self):
        """
        Start trajectory recording, only in teach mode, so joint teaching mode must already be set.

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above
            2. set joint teaching mode: set_mode(2);set_state(0)

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.start_record_trajectory()

    def stop_record_trajectory(self, filename=None, **kwargs):
        """
        Stop trajectory recording

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        :param filename: The name to save
        \n    1. Only strings consisting of standard English characters or numbers are supported, with a maximum length of 50.
        \n    2. The trajectory will be saved in the controller box.
        \n    3. If the filename is None stop recording and do not save, you need to manually call `save_record_trajectory` save before changing the mode. otherwise the recording will be lost
        \n    4. This action will overwrite a trajectory with the same name
        \n    5. Empty the trajectory in memory after saving
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.stop_record_trajectory(filename=filename, **kwargs)
    
    def load_trajectory(self, filename, wait=True, timeout=None, **kwargs):
        """
        Load a trajectory

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        :param filename: The name of the trajectory to load
        :param wait: Whether to wait for loading, default is True
        :param timeout: Timeout waiting for loading to complete
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.load_trajectory(filename, wait=wait, timeout=timeout, **kwargs)
    
    def playback_trajectory(self, times=1, filename=None, wait=True, double_speed=1, **kwargs):
        """
        Playback trajectory

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        \n:param times: Number of playbacks,
        \n    1. Only valid when the current position of the arm is the end position of the trajectory, otherwise it will only be played once.
        \n:param filename: The name of the trajectory to play back
        \n    1. If filename is None, you will need to manually call `load_trajectory` to load the trajectory.
        \n:param wait: whether to wait for the arm to complete, default is False
        \n:param double_speed: double speed, only support 1/2/4, default is 1, only available if version > 1.2.11
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.playback_trajectory(times=times, filename=filename, wait=wait, double_speed=double_speed, **kwargs)
    
    def get_trajectory_rw_status(self):
        """
        Get trajectory read/write status

        :return: (code, status)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstatus:
            \n0: no read/write
            \n1: loading
            \n2: load success
            \n3: load failed
            \n4: saving
            \n5: save success
            \n6: save failed
        """
        return self.arm.get_trajectory_rw_status()
    
    
    def get_reduced_mode(self):
        """
        Get reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        :return: tuple((code, mode))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            mode: 0 or 1, 1 means the reduced mode is on. 0 means the reduced mode is not on
        """
        return self.arm.get_reduced_mode()

    def get_reduced_states(self, is_radian=None):
        """
        Get states of the reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        :param is_radian: if the max_joint_speed of the states is in radians or not, defaults to self.default_is_radian
        :return: tuple((code, states))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstates: [....]
            \n    if version > 1.2.11:
            \n        states: [
            \n           reduced_mode_is_on,
            \n           [reduced_x_max, reduced_x_min, reduced_y_max, reduced_y_min, reduced_z_max, reduced_z_min],
            \n           reduced_max_tcp_speed,
            \n           reduced_max_joint_speed,
            \n           joint_ranges([joint-1-min, joint-1-max, ..., joint-7-min, joint-7-max]),
            \n           safety_boundary_is_on,
            \n           collision_rebound_is_on,
            \n        ]
            \n    if version <= 1.2.11:
            \n        states: [
            \n           reduced_mode_is_on,
            \n           [reduced_x_max, reduced_x_min, reduced_y_max, reduced_y_min, reduced_z_max, reduced_z_min],
            \n           reduced_max_tcp_speed,
            \n           reduced_max_joint_speed,
            \n        ]
        """
        return self.arm.get_reduced_states(is_radian=is_radian)

    def set_reduced_mode(self, on):
        """
        Turn on/off reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above

        \n:param on: True/False
        \n           such as: Turn on the reduced mode : code=arm.set_reduced_mode(True)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_mode(on)

    def set_reduced_max_tcp_speed(self, speed):
        """
        Set the maximum tcp speed of the reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        :param speed: speed (mm/s)
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_max_tcp_speed(speed)

    def set_reduced_max_joint_speed(self, speed, is_radian=None):
        """
        Set the maximum joint speed of the reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        :param speed: speed (°/s or rad/s)
        :param is_radian: the speed is in radians or not, defaults to self.default_is_radian
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_max_joint_speed(speed, is_radian=is_radian)

    def set_reduced_tcp_boundary(self, boundary):
        """
        Set the boundary of the safety boundary mode

        \nNote:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        :param boundary: [x_max, x_min, y_max, y_min, z_max, z_min]
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_tcp_boundary(boundary)

    def set_reduced_joint_range(self, joint_range, is_radian=None):
        """
        Set the joint range of the reduced mode

        \nNote:
            1. This interface relies on Firmware 1.2.11 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        :param joint_range: [joint-1-min, joint-1-max, ..., joint-7-min, joint-7-max]
        :param is_radian: the param joint_range are in radians or not, defaults to self.default_is_radian
        :return:
        """
        return self.arm.set_reduced_joint_range(joint_range, is_radian=is_radian)
    

    def set_fence_mode(self, on):
        """
        Turn on/off fence mode

        \nNote:
            1. This interface relies on Firmware 1.2.11 or above

        :param on: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_fense_mode(on)
    
    def set_collision_rebound(self, on):
        """
        Turn on/off collision rebound

        \nNote:
            1. This interface relies on Firmware 1.2.11 or above

        :param on: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_rebound(on)
    
    def set_world_offset(self, offset, is_radian=None, wait=True):
        """
        Set the base coordinate offset

        \nNote:
            1. This interface relies on Firmware 1.2.11 or above

        :param offset: [x, y, z, roll, pitch, yaw]
        :param is_radian: if the roll/pitch/yaw is in radians or not, defaults to self.default_is_radian
        :param wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed/cleared before setting
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_world_offset(offset, is_radian=is_radian, wait=wait)
    
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

    def is_tcp_limit(self, pose, is_radian=None):
        """
        Check the tcp pose is within limit

        :param pose: [x, y, z, roll, pitch, yaw]
        :param is_radian: roll/pitch/yaw value is radians or not, defaults to self.default_is_radian
        :return: tuple((code, limit)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nlimit: True/False/None, limit or not, or failed
        """
        return self.arm.is_tcp_limit(pose, is_radian=is_radian)
    
    def is_joint_limit(self, joint, is_radian=None):
        """
        Check the joint angle is within limit

        :param joint: [angle-1, angle-2, ..., angle-n], n is the number of axes of the arm
        :param is_radian: angle value is radians or not, defaults to self.default_is_radian
        :return: tuple((code, limit)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nlimit: True/False/None, limit or not, or failed
        """
        return self.arm.is_joint_limit(joint, is_radian=is_radian)

    def emergency_stop(self):
        """
        Emergency stop (set_state(4) -> motion_enable(True) -> set_state(0))
        \nNote:
            1. This interface does not automatically clear errors. If there is an error, you will need to handle it according to the error code.
        """
        return self.arm.emergency_stop()
    
    def register_report_callback(self, callback=None, report_cartesian=True, report_joints=True,
                                 report_state=True, report_error_code=True, report_warn_code=True,
                                 report_mtable=True, report_mtbrake=True, report_cmd_num=True):
        """
        Register the report callback, only available if enable_report is True

        :param callback:
            callback data:
            \n{
            \n   'cartesian': [], # if report_cartesian is True
            \n   'joints': [], # if report_joints is True
            \n   'error_code': 0, # if report_error_code is True
            \n   'warn_code': 0, # if report_warn_code is True
            \n   'state': state, # if report_state is True
            \n   'mtbrake': mtbrake, # if report_mtbrake is True, and available if enable_report is True and the connection method is socket
            \n   'mtable': mtable, # if report_mtable is True, and available if enable_report is True and the connection method is socket
            \n   'cmdnum': cmdnum, # if report_cmd_num is True
            \n}
        \n:param report_cartesian: report cartesian or not, default is True
        \n:param report_joints: report joints or not, default is True
        \n:param report_state: report state or not, default is True
        \n:param report_error_code: report error or not, default is True
        \n:param report_warn_code: report warn or not, default is True
        \n:param report_mtable: report motor enable states or not, default is True
        \n:param report_mtbrake: report motor brake states or not, default is True
        \n:param report_cmd_num: report cmdnum or not, default is True
        \n:return: True/False
        """
        return self.arm.register_report_callback(callback=callback,
                                                  report_cartesian=report_cartesian,
                                                  report_joints=report_joints,
                                                  report_state=report_state,
                                                  report_error_code=report_error_code,
                                                  report_warn_code=report_warn_code,
                                                  report_mtable=report_mtable,
                                                  report_mtbrake=report_mtbrake,
                                                  report_cmd_num=report_cmd_num)

    def register_report_location_callback(self, callback=None, report_cartesian=True, report_joints=True):
        """
        Register the report location callback, only available if enable_report is True

        \n:param callback:
            \ncallback data:
            \n{
            \n   "cartesian": [x, y, z, roll, pitch, yaw], ## if report_cartesian is True
            \n   "joints": [angle-1, angle-2, angle-3, angle-4, angle-5, angle-6, angle-7], ## if report_joints is True
            \n}
        \n:param report_cartesian: report or not, True/False, default is True
        \n:param report_joints: report or not, True/False, default is True
        \n:return: True/False
        """
        return self.arm.register_report_location_callback(callback=callback,
                                                           report_cartesian=report_cartesian,
                                                           report_joints=report_joints)

    def register_connect_changed_callback(self, callback=None):
        """
        Register the connect status changed callback

        :param callback:
            callback data:
            {
                "connected": connected,
                "reported": reported,
            }
        :return: True/False
        """
        return self.arm.register_connect_changed_callback(callback=callback)

    def register_state_changed_callback(self, callback=None):
        """
        Register the state status changed callback, only available if enable_report is True

        :param callback:
            callback data:
            {
                "state": state,
            }
        :return: True/False
        """
        return self.arm.register_state_changed_callback(callback=callback)

    def register_mode_changed_callback(self, callback=None):
        """
        Register the mode changed callback, only available if enable_report is True and the connection method is socket

        :param callback:
            callback data:
            {
                "mode": mode,
            }
        :return: True/False
        """
        return self.arm.register_mode_changed_callback(callback=callback)

    def register_mtable_mtbrake_changed_callback(self, callback=None):
        """
        Register the motor enable states or motor brake states changed callback, only available if enable_report is True and the connection method is socket

        :param callback:
            \ncallback data:
            \n{
            \n   "mtable": [motor-1-motion-enable, motor-2-motion-enable, ...],
            \n   "mtbrake": [motor-1-brake-enable, motor-1-brake-enable,...],
            \n}
        \n:return: True/False
        """
        return self.arm.register_mtable_mtbrake_changed_callback(callback=callback)

    def register_error_warn_changed_callback(self, callback=None):
        """
        Register the error code or warn code changed callback, only available if enable_report is True

        :param callback:
            callback data:
            {
                "error_code": error_code,
                "warn_code": warn_code,
            }
        :return: True/False
        """
        return self.arm.register_error_warn_changed_callback(callback=callback)

    def register_cmdnum_changed_callback(self, callback=None):
        """
        Register the cmdnum changed callback, only available if enable_report is True

        :param callback:
            callback data:
            {
                "cmdnum": cmdnum
            }
        :return: True/False
        """
        return self.arm.register_cmdnum_changed_callback(callback=callback)

    def register_temperature_changed_callback(self, callback=None):
        """
        Register the temperature changed callback, only available if enable_report is True

        :param callback:
            callback data:
            {
                "temperatures": [servo-1-temperature, ...., servo-7-temperature]
            }
        :return: True/False
        """
        return self.arm.register_temperature_changed_callback(callback=callback)

    def register_count_changed_callback(self, callback=None):
        """
        Register the counter value changed callback, only available if enable_report is True

        :param callback:
            callback data:
            {
                "count": counter value
            }
        :return: True/False
        """
        return self.arm.register_count_changed_callback(callback=callback)

    def register_iden_progress_changed_callback(self, callback=None):
        """
        Register the Identification progress value changed callback, only available if enable_report is True
        
        :param callback: 
            callback data:
            {
                "progress": progress value
            }
        :return: True/False
        """
        return self.arm.register_iden_progress_changed_callback(callback=callback)
    
    def release_report_callback(self, callback=None):
        """
        Release the report callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_report_callback(callback)
    

    def release_report_location_callback(self, callback=None):
        """
        Release the location report callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_report_location_callback(callback)
    
    def release_connect_changed_callback(self, callback=None):
        """
        Release the connect changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_connect_changed_callback(callback)

    def release_state_changed_callback(self, callback=None):
        """
        Release the state changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_state_changed_callback(callback)

    def release_mode_changed_callback(self, callback=None):
        """
        Release the mode changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_mode_changed_callback(callback)

    def release_mtable_mtbrake_changed_callback(self, callback=None):
        """
        Release the motor enable states or motor brake states changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_mtable_mtbrake_changed_callback(callback)

    def release_error_warn_changed_callback(self, callback=None):
        """
        Release the error warn changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_error_warn_changed_callback(callback)

    def release_cmdnum_changed_callback(self, callback=None):
        """
        Release the cmdnum changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_cmdnum_changed_callback(callback)

    def release_temperature_changed_callback(self, callback=None):
        """
        Release the temperature changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_temperature_changed_callback(callback=callback)

    def release_count_changed_callback(self, callback=None):
        """
        Release the counter value changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_count_changed_callback(callback=callback)

    def release_iden_progress_changed_callback(self, callback=None):
        """
        Release the Identification progress value changed callback

        :param callback:
        :return: True/False
        """
        return self.arm.release_iden_progress_changed_callback(callback=callback)
    
    def get_servo_debug_msg(self, show=False, lang='en'):
        """
        Get the servo debug msg, used only for debugging

        :param show: show the detail info if True
        :param lang: language, en/cn, default is en
        :return: tuple((code, servo_info_list)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_debug_msg(show=show, lang=lang)
    
    def run_blockly_app(self, path, **kwargs):
        """
        Run the app generated by xArmStudio software
        
        :param path: app path
        """
        return self.arm.run_blockly_app(path, **kwargs)
    
    def run_gcode_file(self, path, **kwargs):
        """
        Run the gcode file
        
        :param path: gcode file path
        """
        return self.arm.run_gcode_file(path, **kwargs)
    
    def get_gripper_version(self):
        """
        Get gripper version, only for debug

        :return: (code, version)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_gripper_version()

    def get_servo_version(self, servo_id=1):
        """
        Get servo version, only for debug

        :param servo_id: servo id(1~7)
        :return: (code, version)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_version(servo_id=servo_id)

    def get_tgpio_version(self):
        """
        Get tool gpio version, only for debug

        :return: (code, version)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_tgpio_version()
    
    def get_harmonic_type(self, servo_id=1):
        """
        Get harmonic type, only for debug

        :return: (code, type)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_harmonic_type(servo_id=servo_id)

    def get_hd_types(self):
        """
        Get harmonic types, only for debug

        :return: (code, types)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_hd_types()
    
    def set_counter_reset(self):
        """
        Reset counter value

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_counter_reset()

    def set_counter_increase(self, val=1):
        """
        Set counter plus value, only supports increasing by 1

        :param val: reversed
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_counter_increase(val)
    
    def get_joints_torque(self):
        """
        Get joint torque
        
        :return: tuple((code, joints_torque))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \njoints_torque: joint torque
        """
        return self.arm.get_joints_torque()
    
    def set_timeout(self, timeout):
        """
        Set the timeout of cmd response

        :param timeout: seconds
        """
        return self.arm.set_timeout(timeout)
    
    def set_baud_checkset_enable(self, enable):
        """
        Enable auto checkset the baudrate of the end IO board or not
        \nNote:
            only available in the API of gripper/bio/robotiq/linear_motor.
            
        :param enable: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_baud_checkset_enable(enable)

    def set_checkset_default_baud(self, type_, baud):
        """
        Set the checkset baud value
        
        \n:param type_: checkset type
        \n   1: xarm gripper
        \n   2: bio gripper
        \n   3: robotiq gripper
        \n   4: linear motor
        \n:param baud: checkset baud value, less than or equal to 0 means disable checkset
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_checkset_default_baud(type_, baud)

    def get_checkset_default_baud(self, type_):
        """
        Get the checkset baud value

        \n:param type_: checkset type
        \n   1: xarm gripper
        \n   2: bio gripper
        \n   3: robotiq gripper
        \n   4: linear motor
        \n:return: tuple((code, baud))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nbaud: the checkset baud value
        """
        return self.arm.get_checkset_default_baud(type_)
    
    def calibrate_tcp_coordinate_offset(self, four_points, is_radian=None):
        """
        Four-point method to calibrate tool coordinate system position offset
        \nNote:
            1. only available if firmware_version >= 1.6.9

        :param four_points: a list of four teaching coordinate positions [x, y, z, roll, pitch, yaw]
        :param is_radian: if the roll/pitch/yaw value of each point is in radians or not, defaults to self.default_is_radian
        :return: tuple((code, xyz_offset)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nxyz_offset: calculated xyz(mm) TCP offset, [x, y, z] 
        """
        return self.arm.calibrate_tcp_coordinate_offset(four_points, is_radian=is_radian)
    
    def calibrate_tcp_orientation_offset(self, rpy_be, rpy_bt, input_is_radian=None, return_is_radian=None):
        """
        An additional teaching point to calibrate the tool coordinate system attitude offset
        \nNote:
            1. only available if firmware_version >= 1.6.9

        :param rpy_be: the rpy value of the teaching point without TCP offset [roll, pitch, yaw]
        :param rpy_bt: the rpy value of the teaching point with TCP offset [roll, pitch, yaw]
        :param input_is_radian: if the roll/pitch/yaw value of rpy_be and rpy_bt is in radians or not, defaults to self.default_is_radian
        :param return_is_radian: if the roll/pitch/yaw value of result is in radians or not, defaults to self.default_is_radian
        :return: tuple((code, rpy_offset)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrpy_offset: calculated rpy TCP offset, [roll, pitch, yaw]
        """
        return self.arm.calibrate_tcp_orientation_offset(rpy_be, rpy_bt, input_is_radian=input_is_radian, return_is_radian=return_is_radian)

    def calibrate_user_orientation_offset(self, three_points, mode=0, trust_ind=0, input_is_radian=None, return_is_radian=None):
        """
        Three-point method teaches user coordinate system posture offset
        \nNote:
            1. only available if firmware_version >= 1.6.9
            2. First determine a point in the working space, move along the desired coordinate system x+ to determine the second point,
            and then move along the desired coordinate system y+ to determine the third point. 
            3. Note that the x+ direction is as accurate as possible. 
            4. If the y+ direction is not completely perpendicular to x+, it will be corrected in the calculation process.

        :param three_points: a list of teaching TCP coordinate positions [x, y, z, roll, pitch, yaw]
        :param input_is_radian: if the roll/pitch/yaw value of each point is in radians or not, defaults to self.default_is_radian
        :param return_is_radian: if the roll/pitch/yaw value of the result should be in radians or not, defaults to self.default_is_radian
        :return: tuple((code, rpy_offset)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrpy_offset: calculated rpy user offset, [roll, pitch, yaw]
        """
        return self.arm.calibrate_user_orientation_offset(three_points, mode=mode, trust_ind=trust_ind, input_is_radian=input_is_radian, return_is_radian=return_is_radian)
    
    def calibrate_user_coordinate_offset(self, rpy_ub, pos_b_uorg, is_radian=None):
        """
        An additional teaching point determines the position offset of the user coordinate system.
        \nNote:
            1. only available if firmware_version >= 1.6.9

        :param rpy_ub: the confirmed offset of the base coordinate system in the user coordinate system [roll, pitch, yaw], the result of calibrate_user_orientation_offset()
        :param pos_b_uorg: the position of the teaching point in the base coordinate system [x, y, z], if the arm cannot reach the target position, the user can manually input the position of the target in the base coordinate.
        :param is_radian: if the roll/pitch/yaw value of rpy_ub is in radians or not, defaults to self.default_is_radian
        :return: tuple((code, xyz_offset)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nxyz_offset: calculated xyz(mm) user offset, [x, y, z] 
        """
        return self.arm.calibrate_user_coordinate_offset(rpy_ub, pos_b_uorg, is_radian=is_radian)
    
    def set_simulation_robot(self, on_off):
        """
        Set the simulation robot
        
        :param on_off: True/False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_simulation_robot(on_off)
    
    def get_base_board_version(self, board_id=10):
        """
         Get base board version

        :param board_id: int
        :return: (code, version)
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_base_board_version(board_id)
    
    def iden_tcp_load(self, estimated_mass=0):
        """
        Identification the tcp load with current
        \nNote:
            1. only available if firmware_version >= 1.8.0
        
        :param estimated_mass: estimated mass
            \nNote: this parameter is only available on the lite6 model manipulator, and this parameter must be specified for the lite6 model manipulator
        :return: tuple((code, load)) returned result is only corrent when code is 0.
            \ncode:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nload:  [mass, x_centroid, y_centroid, z_centroid]
        """
        return self.arm.iden_tcp_load(estimated_mass)
    
    def delete_blockly_app(self, name):
        """
        Delete blockly app
        
        :param name: blockly app name
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self._studio.delete_blockly_app(name)
    
    def delete_trajectory(self, name):
        """
        Delete trajectory
        
        :param name: trajectory name
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self._studio.delete_trajectory(name)
    
    def get_initial_point(self):
        """
        Get the initial point from studio
        
        :return: tuple((code, point)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \npoint: initial point, [J1, J2, ..., J7]
        """
        return self._studio.get_initial_point()
    
    def set_initial_point(self, point):
        """
        Set the initial point
        
        :param point: initial point, [J1, J2, ..., J7]
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details. 
        """
        return self._studio.set_initial_point(point)
    
    def get_mount_direction(self):
        """
        Get the mount degrees from studio

        :return: tuple((code, degrees)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \ndegrees: mount degrees, [tilt angle, rotate angle]
        """
        return self._studio.get_mount_direction()
    
    def set_cartesian_velo_continuous(self, on_off):
        """
        Set cartesian motion velocity continuous
        \nNote:
            1. only available if firmware_version >= 1.9.0
        
        :param on_off: whether motion is continuous or not, True: continuous, defaults to False
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_cartesian_velo_continuous(on_off)

    def set_allow_approx_motion(self, on_off):
        """
        Settings to allow avoiding overspeed near some singularities using approximate solutions
        
        \nNote:
            1. only available if firmware_version >= 1.9.0

        :param on_off: whether to allow or not, True: allow, default is False
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_allow_approx_motion(on_off)
    
    def get_allow_approx_motion(self):
        """
        Obtain whether to enable approximate solutions to avoid certain singularities
        \nNote:
            1. only available if firmware_version >= 1.9.0

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_allow_approx_motion()
    
    def get_joint_states(self, is_radian=None, num=3):
        """
        Get the joint states
        \nNote:
            1. only available if firmware_version >= 1.9.0

        :param is_radian: if the returned value(position and velocity) is in radians or not, defaults to self.default_is_radian
        :return: tuple((code, [position, velocity, effort])), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nposition: the angles of joints, like [angle-1, ..., angle-7]
            \nvelocity: the velocities of joints, like [velo-1, ..., velo-7]
            \neffort: the efforts of joints, like [effort-1, ..., effort-7]
        """
        return self.arm.get_joint_states(is_radian=is_radian, num=num)
    
    def iden_joint_friction(self, sn=None):
        """
        Identification of the friction
        \nNote:
            1. only available if firmware_version >= 1.9.0
        
        :param sn: sn value
        :return: tuple((code, result)) returned result is only corrent when code is 0.
            \ncode:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nresult: 
            \n0: success
            \n-1: failure
        """
        return self.arm.iden_joint_friction(sn)
    
    def set_only_check_type(self, only_check_type=0):
        """
        Set the motion process detection type (valid for all motion interfaces of the current SDK instance)

        \nNote:
            1. only available if firmware_version >= 1.11.100
            2. This interface is a global configuration item of the current SDK, and affects all motion-related interfaces
            3. Generally, you only need to call when you don't want to move the robotic arm and only check whether some paths will have self-collision/angle-limit/cartesian-limit/overspeed.
            4. Currently only self-collision/angle-limit/cartesian-limit/overspeed are detected
            5. If only_check_type is set to be greater than 0, and the return value of calling the motion interface is not 0, you can view arm.only_check_result to view the specific error code
        
        Example: (Common scenarios, here is an example of the set_position interface)
            1. Check whether the process from point A to point B is normal (no self-collision and overspeed triggered)
                1.1 Move to point A
                    arm.set_only_check_type(0)
                    code = arm.set_position(A)
                1.2 Check if the process from point A to point B is normal (no self-collision and overspeed triggered)
                    arm.set_only_check_type(1)
                    code = arm.set_position(B)
                    If code is not equal to 0, it means that the path does not pass. You can check the specific error code through arm.only_check_result
                    arm.set_only_check_type(0)
                    
            2. Check whether the process from point A to point B, C, and D to point E is normal (no self-collision and overspeed are triggered)
                2.1 Move to point A
                    arm.set_only_check_type(0)
                    code = arm.set_position(A)
                2.2 Check whether the process of point A passing through points B, C, D to point E is normal (no self-collision and overspeed are triggered)
                    arm.set_only_check_type(3)
                    code = arm.set_position(B)
                    If code is not equal to 0, it means that the path does not pass. You can check the specific error code through arm.only_check_result
                    code = arm.set_position(C)
                    If code is not equal to 0, it means that the path does not pass. You can check the specific error code through arm.only_check_result
                    code = arm.set_position(D)
                    If code is not equal to 0, it means that the path does not pass. You can check the specific error code through arm.only_check_result
                    code = arm.set_position(E)
                    If code is not equal to 0, it means that the path does not pass. You can check the specific error code through arm.only_check_result
                    arm.set_only_check_type(0)

        \n:param only_check_type: Motion Detection Type
            \nonly_check_type == 0: Restore the original function of the motion interface, it will move, the default is 0
            \nonly_check_type == 1: Only check the self-collision without moving, take the actual state of the manipulator as the initial planned path, and check whether the path has self-collision (the intermediate state will be updated at this time)
            \nonly_check_type == 2: Only check the self-collision without moving, use the intermediate state as the starting planning path, check whether the path has self-collision (the intermediate state will be updated at this time), and restore the intermediate state to the actual state after the end
            \nonly_check_type == 3: Only check the self-collision without moving, use the intermediate state as the starting planning path, and check whether the path has self-collision (the intermediate state will be updated at this time)
        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_only_check_type(only_check_type)
    
    def get_dh_params(self):
        """
        Get the DH parameters
        \nNote:
            1. only available if firmware_version >= 2.0.0
        
        :return: tuple((code, dh_params)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \ndh_params: DH parameters
            \n   dh_params[0:4]: DH parameters of Joint-1
            \n   dh_params[4:8]: DH parameters of Joint-2
            \n   ...
            \n   dh_params[24:28]: DH parameters of Joint-7
        """
        return self.arm.get_dh_params()
    
    def set_dh_params(self, dh_params, flag=0):
        """
        Set the DH parameters
        \nNote:
            1. only available if firmware_version >= 2.0.0
            2. this interface is only provided for users who need to use external DH parameters, ordinary users should not try to modify DH parameters.
        
        :param dh_params: DH parameters
        :param flag: 
        \n0: Use the set DH parameters, but do not write to the configuration file
        \n1: Use the set DH parameters and write to the configuration file
        \n2: Use the set DH parameters and delete the DH parameters of the configuration file
        \n3: Use the default DH parameters, but will not delete the DH parameters of the configuration file
        \n4: Use the default DH parameters and delete the DH parameters of the configuration file
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_dh_params(dh_params, flag) 
    
    def set_feedback_type(self, feedback_type):
        """
        Set the feedback type
        \nNote:
            1. only available if firmware_version >= 2.1.0
            2. only works in position mode
            3. the setting will only affect subsequent tasks and will not affect previously cached tasks
            4. only valid for the current connection
        
        :param feedback_type:
            \n0: disable feedback
            \n1: feedback when the motion task starts executing
            \n2: feedback when the motion task execution ends or motion task is discarded(usually when the distance is too close to be planned)
            \n4: feedback when the non-motion task is triggered
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_feedback_type(feedback_type)
    
    def register_feedback_callback(self, callback=None):
        """
        Register the callback of feedback
        \nNote:
            1. only available if firmware_version >= 2.1.0

        \n:param callback:
        \n    callback data: bytes data
        \n        data[0:2]: transaction id, (Big-endian conversion to unsigned 16-bit integer data), command ID corresponding to the feedback, consistent with issued instructions
        \n            \nNote: this can be used to distinguish which instruction the feedback belongs to
        \n        data[4:6]: feedback_length, feedback_length == len(data) - 6, (Big-endian conversion to unsigned 16-bit integer data)
        \n        data[8]: feedback type
        \n            1: the motion task starts executing
        \n            2: the motion task execution ends or motion task is discarded(usually when the distance is too close to be planned)
        \n            4: the non-motion task is triggered
        \n        data[9]: feedback funcode, command code corresponding to feedback, consistent with issued instructions
        \n            \nNote: this can be used to distinguish what instruction the feedback belongs to
        \n        data[10:12]: feedback taskid, (Big-endian conversion to unsigned 16-bit integer data)
        \n        data[12]: feedback code, execution status code, generally only meaningful when the feedback type is end, normally 0, 2 means discarded
        \n        data[13:21]: feedback us, (Big-endian conversion to unsigned 64-bit integer data), time when feedback triggers (microseconds)
        \n            \nNote: this time is the corresponding controller system time when the feedback is triggered
        \n:return: True/False
        """
        return self.arm.register_feedback_callback(callback=callback)

    def release_feedback_callback(self, callback=None):
        """
        Release the callback of feedback

        \nNote:
            1. only available if firmware_version >= 2.1.0

        :param callback:
        :return: True/False
        """
        return self.arm.release_feedback_callback(callback=callback)
    
    def read_coil_bits(self, addr, quantity):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Coils (0x01)
        
        :param addr: the starting address of the register to be read
        :param quantity: number of registers
        :return: tuple((code, bits)) returned result is only corrent when code is 0.
            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_coil_bits(addr, quantity)

    def read_input_bits(self, addr, quantity):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Discrete Inputs (0x02)
        
        :param addr: the starting address of the register to be read
        :param quantity: number of registers
        :return: tuple((code, bits)) returned result is only corrent when code is 0.
            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_input_bits(addr, quantity)
    
    def read_holding_registers(self, addr, quantity, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Holding Registers (0x03)
        
        :param addr: the starting address of the register to be read
        :param quantity: number of registers
        :param is_signed: whether to convert the read register value into a signed form
        :return: tuple((code, bits)) returned result is only corrent when code is 0.
            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_holding_registers(addr, quantity, is_signed)
    
    def read_input_registers(self, addr, quantity, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Input Registers (0x04)
        
        :param addr: the starting address of the register to be read
        :param quantity: number of registers
        :param is_signed: whether to convert the read register value into a signed form
        :return: tuple((code, bits)) returned result is only corrent when code is 0.
            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_input_registers(addr, quantity, is_signed)
    
    def write_single_coil_bit(self, addr, bit_val):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Single Coil (0x05)
        
        :param addr: register address
        :param bit_val: the value to write (0/1)
        :return: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_single_coil_bit(addr, bit_val)
    
    def write_single_holding_register(self, addr, reg_val):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Single Holding Register (0x06)
        
        :param addr: register address
        :param bit_val: the value to write
        :return: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_single_holding_register(addr, reg_val)

    def write_multiple_coil_bits(self, addr, bits):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Multiple Coils (0x0F)
        
        :param addr: the starting address of the register to be written
        :param bits: array of values to write
        :return: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_multiple_coil_bits(addr, bits)

    def write_multiple_holding_registers(self, addr, regs):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Multiple Holding Registers (0x10)
        
        :param addr: the starting address of the register to be written
        :param regs: array of values to write
        :return: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_multiple_holding_registers(addr, regs)
    
    def mask_write_holding_register(self, addr, and_mask, or_mask):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Mask Write Holding Register (0x16)
        
        :param addr: register address
        :param and_mask: mask to be AND with
        :param or_mask: mask to be OR with
        :return: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.mask_write_holding_register(addr, and_mask, or_mask)

    def write_and_read_holding_registers(self, r_addr, r_quantity, w_addr, w_regs, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write and Read Holding Registers (0x17)
        
        :param r_addr: the starting address of the register to be read
        :param r_quantity: number of registers to read
        :param w_addr: the starting address of the register to be written
        :param w_regs: array of values to write
        :param is_signed: whether to convert the read register value into a signed form
        :return: tuple((code, regs)) returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_and_read_holding_registers(r_addr, r_quantity, w_addr, w_regs, is_signed)
    
    def send_hex_cmd(self, datas, **kwargs):
        """
        Hexadecimal communication protocol instruction

        :param datas: Hexadecimal data_list
        :param timeout: timeout: wait timeout, seconds, default is 10s.
        :return: Hexadecimal data_list or code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
                \nNote: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.send_hex_cmd(datas, **kwargs)
    
    def set_linear_spd_limit_factor(self, factor):
        """
        Set linear speed limit factor (default is 1.2)
        \nNote:
            1. only available if firmware_version >= 2.3.0
            2. only available in mode 1

        :param factor: speed limit factor
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_spd_limit_factor(self, factor)
    
    def set_cmd_mat_history_num(self, num):
        """
        Set cmd mat history num
        \nNote:
            Only available if firmware_version >= 2.3.0

        :param num: history num
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_cmd_mat_history_num(self, num)
    
    def set_fdb_mat_history_num(self, num):
        """
        Set fdb mat history num
        \nNote:
            Only available if firmware_version >= 2.3.0

        :param num: history num
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_fdb_mat_history_num(self, num)
    
    def get_linear_spd_limit_factor(self):
        """
        Get linear speed limit factor
        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, factor)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            factor: linear speed limit factor
        """
        return self.arm.get_linear_spd_limit_factor(self)
    
    def get_cmd_mat_history_num(self):
        """
        Get cmd mat history num
        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, num)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nnum: cmd mat history num
        """
        return self.arm.get_cmd_mat_history_num(self)
    
    def get_fdb_mat_history_num(self):
        """
        Get fdb mat history num
        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, num)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nnum: fdb mat history num
        """
        return self.arm.get_fdb_mat_history_num(self)
    
    def get_poe_status(self):
        """
        Get poe status

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, status)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstatus: 1 means poe is valid, 0 means poe is invalid
        """
        return self.arm.get_poe_status(self)
    
    def get_iden_status(self):
        """
        Get iden status

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, status)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstatus: 1 means in identifying, 0 means not in identifying
        """
        return self.arm.get_iden_status(self)
    
    def get_c31_error_info(self):
        """
        Get collision error (C31) info

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [servo_id, theoratival tau, actual tau]
        """
        return self.arm.get_c31_error_info(self)
    
    def get_c37_error_info(self, is_radian=None):
        """
        Get payload error (C37) info

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [servo_id, angle]
        """
        return self.arm.get_c37_error_info(self, is_radian)
    
    def get_c23_error_info(self, is_radian=None):
        """
        Get joint angle limit error (C23) info

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [(servo_id, angle), ...]
        """
        return self.get_c23_error_info(self, is_radian)
    
    def get_c24_error_info(self, is_radian=None):
        """
        Get joint speed limit error (C24) info

        \nNote:
            Only available if firmware_version >= 2.3.0

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [servo_id, speed]
        """
        return self.arm.get_c24_error_info(self, is_radian)
    
    def get_c60_error_info(self):
        """
        Get linear speed limit error (C60) info

        \nNote:
            1. Only available if firmware_version >= 2.3.0
            2. Only available in mode 1

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [max_linear_speed, curr_linear_speed]
        """
        return self.arm.get_c60_error_info(self)
    
    def get_c38_error_info(self, is_radian=None):
        """
        Get joint hard angle limit error (C38) info

        \nNote:
            Only available if firmware_version >= 2.4.0

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [(servo_id, angle), ...]
        """
        return self.arm.get_c38_error_info(self, is_radian)
    
    def get_c54_error_info(self):
        """
        Get (Six-axis Force Torque Sensor) collision error (C54) info

        \nNote:
            Only available if firmware_version >= 2.6.103

        :return: tuple((code, err_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_info: [dir, tau threshold, actual tau]
        """
        return self.arm.get_c54_error_info(self)
    
    def run_gcode_app(self, path, **kwargs):
        """
        Run gcode project file by xArmStudio software

        :param path: gcode file path
        
        :return: code, returned result is only corrent when code is 0.
        """
        return self.arm.run_gcode_app(self, path, **kwargs)
    
    def get_traj_speeding(self, rate):
        """
        Obtain the joint and velocity values of joint overspeed during trajectory recording

        :param rate: speed rate, only 1/2/4

        :return: tuple((code, speed_info)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nspeed_info: [result_code, servo_id, servo_speed]
            \n           result_code: 0: Pass, -1: Fail, >0: abnormal(1:Trajectory not loaded or incorrect status;2:The input magnification is incorrect)
            \n           servo_id: Effective only when result_code is -1
            \n           servo_speed: Effective only when result_code is -1
        """
        return self.arm.get_traj_speeding(self, rate)
    
    def set_external_device_monitor_params(self, dev_type, frequency):
        """
        Set the monitor params of the external device

        \nNote:
            1. only available if firmware_version >= 2.7.100
            2. after it is turned on, the position/speed/current information of the external device will be reported through port 30000
            3. once an error occurs, you need to re call to monitor

        :param dev_type: the type of the external device
            0: Turn off monitoring
            1: xArm Gripper
            2: xArm Gripper G2
            3: BIO Gripper G2
            4: Robotiq 2F-85/Robotiq 2F-140
        :param frequency: the frequency of communication with the external device

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_external_device_monitor_params(self, dev_type, frequency)
    
    def get_external_device_monitor_params(self):
        """
        Get the monitor params of the external device

        \nNote:
            1. only available if firmware_version >= 2.7.100

        :return: tuple((code, params)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            params: [dev_type, frequency]
        """
        return self.arm.get_external_device_monitor_params(self)