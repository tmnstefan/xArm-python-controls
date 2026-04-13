from xarm.wrapper import XArmAPI

class arm_settings():
    def __init__(self, arm:XArmAPI):
        self.arm = arm
    
    def set_state(self, state=0):
        """
        Set the xArm state

        Args:
            state: default 0
                - 0: motion state
                - 3: pause state
                - 4: stop state
                - 6: deceleration stop state

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_state(state=state)

    def set_mode(self, mode=0, detection_param=0):
        """
        Set the xArm mode

        Args:
            mode: default 0

                0: position control

                1: servo motion

                    Note: the use of the set_servo_angle_j interface must first be set to this

                    Note: the use of the set_servo_cartesian interface must first be set to this

                2: joint teaching

                    Note: use this mode to ensure that the arm has been identified and the control box and arm used for identification are one-to-one.

                3: cartesian teaching (invalid)

                4: joint velocity control

                5: cartesian velocity control

                6: joint online trajectory planning

                7: cartesian online trajectory planning

            detection_param: Teaching detection parameters, default is 0

                0: motion detection on

                1: motion detection off

                Note:

                    1. only available if firmware_version >= 1.10.1

                    2. only available if set_mode(2)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_mode(mode=mode, detection_param=detection_param)
    
    def motion_enable(self, enable=True, servo_id=None):
        """
        Enable motion

        Args:
            enable: True/False

            servo_id: 1-(Number of axes), None(8)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.motion_enable(servo_id=servo_id, enable=enable)
    
    def set_pause_time(self, sltime, wait=False):
        """
        Set the arm pause time, xArm will pause sltime second

        Args:
            sltime: sleep time,unit:(s)second

            wait: wait or not, default is False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_pause_time(sltime=sltime, wait=wait)
    
    def get_version(self):
        """
        Get the xArm firmware version

        Returns:
            out: tuple((code, version)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_version()
    
    def get_state(self):
        """
        Get state

        Returns:
            out: tuple((code, state)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            state: state
                - 1: in motion
                - 2: sleeping
                - 3: suspended
                - 4: stopping
        """
        return self.arm.get_state()
    
    def get_is_moving(self):
        """
        Check if the arm is moving or not

        Returns:
            out: True/False
        """
        return self.arm.get_is_moving()
    
    def get_cmdnum(self):
        """
        Get the cmd count in cache

        Returns:
            out: tuple((code, cmd_num)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_cmdnum()
    
    def get_position(self, is_radian=None):
        """
        Get the cartesian position

        Note:
            1. If the value(roll/pitch/yaw) you want returned should be in radians, set is_radian to True
              ex: code, pos = arm.get_position(is_radian=True)

        Args:
            is_radian: if the returned value (only roll/pitch/yaw) is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, [x, y, z, roll, pitch, yaw])), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_position(is_radian=is_radian)
    
    def get_servo_angle(self, servo_id=None, is_radian=None, is_real=False):
        """
        Get the servo angle

        Note:
            1. If the value you want returned should be in radians, set is_radian to True
              ex: code, angles = arm.get_servo_angle(is_radian=True)
            2. If you want to return only the angle of a single joint, please set the parameter servo_id
              ex: code, angle = arm.get_servo_angle(servo_id=2)
            3. This interface is only used in the base coordinate system.

        Args:
            servo_id: 1-(Number of axes), None(8), default is None

            is_radian: the returned value is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, angle list if servo_id is None or 8 else angle)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_angle(servo_id=servo_id, is_radian=is_radian, is_real=is_real)
    
    def get_position_aa(self, is_radian=None):
        """
        Get the pose represented by the axis angle pose
        
        Args:
            is_radian: if the returned value (only rx/ry/rz) is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, [x, y, z, rx, ry, rz])), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_position_aa(is_radian=is_radian)
    
    def get_pose_offset(self, pose1, pose2, orient_type_in=0, orient_type_out=0, is_radian=None):
        """
        Calculate the pose offset of two given points

        Note:
            1. x, y, z are all in mm
            2. roll/rx, pitch/ry, yaw/rz are in either degrees or radians, can be selected by changing parameter is_radian
        
        Args:
            pose1: [x, y, z, roll/rx, pitch/ry, yaw/rz]
            
            pose2: [x, y, z, roll/rx, pitch/ry, yaw/rz]
            
            orient_type_in: input attitude notation, 0 is RPY(roll/pitch/yaw) (default), 1 is axis angle(rx/ry/rz)
            
            orient_type_out: notation of output attitude, 0 is RPY (default), 1 is axis angle
            
            is_radian: if the roll/rx/pitch/ry/yaw/rz of pose1/pose2/return_pose is in radians or not

        Returns:
            out: tuple((code, pose)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            pose: [x(mm), y(mm), z(mm), roll/rx(rad or °), pitch/ry(rad or °), yaw/rz(rad or °)]
        """
        return self.arm.get_pose_offset(pose1, pose2, orient_type_in=orient_type_in, orient_type_out=orient_type_out, is_radian=is_radian)
    
    def set_tcp_offset(self, offset, is_radian=None, wait=True, **kwargs):
        """
        Set the tool coordinate system offset at the end

        Note:
            1. Do not use if not required
            2. If not saved and you want to revert to the last saved value, please reset the offset by set_tcp_offset([0, 0, 0, 0, 0, 0])
            3. If not saved, it will be lost after reboot
            4. The save_conf interface can record the current settings and will not be lost after the restart.
            5. The clean_conf interface can restore system default settings

        Args:
            offset: [x, y, z, roll, pitch, yaw]
            
            is_radian: the roll/pitch/yaw in radians or not, defaults to self.default_is_radian
            
            wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed or cleared before setting

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_offset(offset, is_radian=is_radian, wait=wait, **kwargs)

    def set_tcp_jerk(self, jerk):
        """
        Set the translational jerk of Cartesian space
        
        Note:
            1. Do not use if not required
            2. If not saved, it will be lost after reboot
            3. The save_conf interface can record the current settings and will not be lost after the restart.
            4. The clean_conf interface can restore system default settings

        Args:
            jerk: jerk (mm/s^3)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_jerk(jerk)

    def set_tcp_maxacc(self, acc):
        """
        Set the max translational acceleration of Cartesian space
        
        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            acc: max acceleration (mm/s^2)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_maxacc(acc)

    def set_joint_jerk(self, jerk, is_radian=None):
        """
        Set the jerk of Joint space

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            jerk: jerk (°/s^3 or rad/s^3)
            
            is_radian: if the jerk is in radians or not, defaults to self.default_is_radian

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_joint_jerk(jerk, is_radian=is_radian)

    def set_joint_maxacc(self, acc, is_radian=None):
        """
        Set the max acceleration of Joint space

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            acc: max acceleration (°/s^2 or rad/s^2)
            
            is_radian: if the jerk is in radians or not, defaults to self.default_is_radian

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_joint_maxacc(acc, is_radian=is_radian)

    def set_tcp_load(self, weight, center_of_gravity, wait=False, **kwargs):
        """
        Set the end load of xArm

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            weight: load weight (unit: kg)
            
            center_of_gravity: load center of gravity, such as [x(mm), y(mm), z(mm)]
            
            wait: whether to wait for the command to be executed or for the robotic arm to stop

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_tcp_load(weight, center_of_gravity, wait=wait, **kwargs)

    def set_collision_sensitivity(self, value, wait=True):
        """
        Set the sensitivity to collision

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            value: sensitivity value, 0~5
            
            wait: reversed

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_sensitivity(value, wait=wait)

    def set_teach_sensitivity(self, value, wait=True):
        """
        Set the sensitivity of drag and teach

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            value: sensitivity value, 1~5
            
            wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed or cleared before setting

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_teach_sensitivity(value, wait=wait)

    def set_gravity_direction(self, direction, wait=True):
        """
        Set the gravity direction for proper torque compensation and collision detection.

        Note:
            1. Use only if necessary. Incorrect settings may affect torque compensation.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            direction: Gravity direction vector [x, y, z], e.g., [0, 0, -1] for a floor-mounted arm.
            
            wait: Whether to wait for the robotic arm to stop or clear all previous queued commands before applying the setting.

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gravity_direction(direction=direction, wait=wait)

    def set_mount_direction(self, base_tilt_deg, rotation_deg, is_radian=None):
        """
        Set the mount direction

        Note:
            1. Use only if necessary.
            2. Changes are not saved automatically. Call save_conf() to save the settings, otherwise they will be lost after a reboot.
            3. Use clean_conf() to restore the system default settings.

        Args:
            base_tilt_deg: tilt degree
            
            rotation_deg: rotation degree
            
            is_radian: if the base_tilt_deg/rotation_deg is in radians or not, defaults to self.default_is_radian

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_mount_direction(base_tilt_deg, rotation_deg, is_radian=is_radian)

    def get_inverse_kinematics(self, pose, input_is_radian=None, return_is_radian=None, limited=True, ref_angles=None):
        """
        Get inverse kinematics

        Note: the roll/pitch/yaw unit is radian if input_is_radian is True, else °

        Args:
            pose: [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)]
            
            input_is_radian: if the param pose value(only roll/pitch/yaw) is in radians or not, defaults to self.default_is_radian
            
            return_is_radian: if the returned value should be in radians or not, defaults to self.default_is_radian
            
            limited: if the result is limited to within ±180° or not, default is True(only available if firmware_version >= 2.7.103)
            
            ref_angles: reference values for joint angles
                Note: unit is radian if input_is_radian is True, else °
                Note: only available if firmware_version >= 2.7.103

        Returns:
            out: tuple((code, angles)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            angles: [angle-1(rad or °), angle-2, ..., angle-(Number of axes)] or []

                Note: the returned angle value is radians if return_is_radian is True, else °
        """
        return self.arm.get_inverse_kinematics(pose, input_is_radian=input_is_radian, return_is_radian=return_is_radian, limited=limited, ref_angles=ref_angles)

    def get_forward_kinematics(self, angles, input_is_radian=None, return_is_radian=None):
        """
        Get forward kinematics

        Args:
            angles: [angle-1, angle-2, ..., angle-n], n is the number of axes of the arm
            
            input_is_radian: the param angles value is in radians or not, defaults to self.default_is_radian
            
            return_is_radian: the returned value is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, pose)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            pose: [x(mm), y(mm), z(mm), roll(rad or °), pitch(rad or °), yaw(rad or °)] or []

                Note: the roll/pitch/yaw value is radians if return_is_radian is True, else °
        """
        return self.arm.get_forward_kinematics(angles, input_is_radian=input_is_radian, return_is_radian=return_is_radian)
    
    def set_tgpio_digital_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the digital value of the specified Tool GPIO when the robot has reached the specified xyz position           
        
        Args:
            ionum: 0 or 1
            
            value: value
            
            xyz: position xyz, as [x, y, z]
            
            fault_tolerance_radius: fault tolerance radius

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details. 
        """
        return self.arm.set_tgpio_digital_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def set_cgpio_digital_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the digital value of the specified Controller GPIO when the robot has reached the specified xyz position           
        
        Args:
            ionum: 0 ~ 15
            
            value: value
            
            xyz: position xyz, as [x, y, z]
            
            fault_tolerance_radius: fault tolerance radius

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.  
        """
        return self.arm.set_cgpio_digital_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def set_cgpio_analog_with_xyz(self, ionum, value, xyz, fault_tolerance_radius):
        """
        Set the analog value of the specified Controller GPIO when the robot has reached the specified xyz position           

        Args:
            ionum: 0 ~ 1
            
            value: value
            
            xyz: position xyz, as [x, y, z]
            
            fault_tolerance_radius: fault tolerance radius

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.  
        """
        return self.arm.set_cgpio_analog_with_xyz(ionum, value, xyz, fault_tolerance_radius)

    def config_tgpio_reset_when_stop(self, on_off):
        """
        Configure the Tool GPIO reset the digital output when the robot is in stop state
        
        Args:
            on_off: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.config_io_reset_when_stop(1, on_off)

    def config_cgpio_reset_when_stop(self, on_off):
        """
        Configure the Controller GPIO reset the digital output when the robot is in stop state

        Args:
            on_off: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.config_io_reset_when_stop(0, on_off)
    
    def set_report_tau_or_i(self, tau_or_i=0):
        """
        Set if torque or electric current is reported
        
        Args:
            tau_or_i: 
                - 0: torque
                - 1: electric current
        
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_report_tau_or_i(tau_or_i=tau_or_i)

    def get_report_tau_or_i(self):
        """
        Get the reported torque or electric current
        
        Returns:
            out: tuple((code, tau_or_i))

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            tau_or_i: 
                - 0: torque
                - 1: electric current
        """
        return self.arm.get_report_tau_or_i()

    def set_self_collision_detection(self, on_off):
        """
        Set whether to enable self-collision detection 
        
        Args:
            on_off: enable or not
        
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_self_collision_detection(on_off)

    def set_collision_tool_model(self, tool_type, *args, **kwargs):
        """
        Set the geometric model of the end effector for self collision detection
         
        Args:
            tool_type: the geometric model type
                - 0: No end effector, no additional parameters required
                - 1: xArm Gripper, no additional parameters required
                - 2: xArm Vacuum Gripper, no additional parameters required
                - 3: xArm Bio Gripper, no additional parameters required
                - 4: Robotiq-2F-85 Gripper, no additional parameters required
                - 5: Robotiq-2F-140 Gripper, no additional parameters required
                - 7: Lite Gripper, no additional parameters required
                - 8: Lite Vacuum Gripper, no additional parameters required
                - 9: xArm Gripper G2, no additional parameters required
                - 10: PGC-140-50 of the DH-ROBOTICS, no additional parameters required
                - 11: RH56DFX-2L of the INSPIRE-ROBOTS, no additional parameters required
                - 12: RH56DFX-2R of the INSPIRE-ROBOTS, no additional parameters required
                - 13: xArm Bio Gripper G2, no additional parameters required
                - 21: Cylinder, need additional parameters radius, height 
                    - ex: self.set_collision_tool_model(21, radius=45, height=137)
                    - radius: the radius of cylinder, (mm)
                    - height: the height of cylinder, (mm)
                    - x_offset: offset in the x direction, (mm)
                    - y_offset: offset in the y direction, (mm)
                    - z_offset: offset in the z direction, (mm)
                - 22: Cuboid, need additional parameters x, y, z
                    - ex: self.set_collision_tool_model(22, x=234, y=323, z=23)
                    - x: the length of the cuboid in the x coordinate direction, (mm)
                    - y: the length of the cuboid in the y coordinate direction, (mm)
                    - z: the length of the cuboid in the z coordinate direction, (mm)
                    - x_offset: offset in the x direction, (mm)
                    - y_offset: offset in the y direction, (mm)
                    - z_offset: offset in the z direction, (mm)
            
            args: additional parameters
            
            kwargs: additional parameters

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_tool_model(tool_type, *args, **kwargs)
    
    def get_robot_sn(self):
        """
        Gets the xArm sn

        Returns:
            out: tuple((code, sn)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_robot_sn()
    
    def get_reduced_mode(self):
        """
        Get reduced mode

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Returns:
            out: tuple((code, mode))

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            mode: 0 or 1, 1 means the reduced mode is on. 0 means the reduced mode is not on
        """
        return self.arm.get_reduced_mode()

    def get_reduced_states(self, is_radian=None):
        """
        Get states of the reduced mode

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Args:
            is_radian: if the max_joint_speed of the states is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, states))

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            states: [....]
            ```
                if version > 1.2.11:
                    states: [
                       reduced_mode_is_on,
                       [reduced_x_max, reduced_x_min, reduced_y_max, reduced_y_min, reduced_z_max, reduced_z_min],
                       reduced_max_tcp_speed,
                       reduced_max_joint_speed,
                       joint_ranges([joint-1-min, joint-1-max, ..., joint-7-min, joint-7-max]),
                       safety_boundary_is_on,
                       collision_rebound_is_on,
                    ]
                if version <= 1.2.11:
                    states: [
                       reduced_mode_is_on,
                       [reduced_x_max, reduced_x_min, reduced_y_max, reduced_y_min, reduced_z_max, reduced_z_min],
                       reduced_max_tcp_speed,
                       reduced_max_joint_speed,
                    ]
            ```
        """
        return self.arm.get_reduced_states(is_radian=is_radian)

    def set_reduced_max_tcp_speed(self, speed):
        """
        Set the maximum tcp speed of the reduced mode

        Note:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        Args:
            speed: speed (mm/s)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_max_tcp_speed(speed)

    def set_reduced_max_joint_speed(self, speed, is_radian=None):
        """
        Set the maximum joint speed of the reduced mode

        Note:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        Args:
            speed: speed (°/s or rad/s)
            
            is_radian: the speed is in radians or not, defaults to self.default_is_radian

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_max_joint_speed(speed, is_radian=is_radian)

    def set_reduced_tcp_boundary(self, boundary):
        """
        Set the boundary of the safety boundary mode

        Note:
            1. This interface relies on Firmware 1.2.0 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        Args:
            boundary: [x_max, x_min, y_max, y_min, z_max, z_min]

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_reduced_tcp_boundary(boundary)

    def set_reduced_joint_range(self, joint_range, is_radian=None):
        """
        Set the joint range of the reduced mode

        Note:
            1. This interface relies on Firmware 1.2.11 or above
            2. Only reset the reduced mode to take effect (`set_reduced_mode(True)`)

        Args:
            joint_range: [joint-1-min, joint-1-max, ..., joint-7-min, joint-7-max]
        
            is_radian: the param joint_range are in radians or not, defaults to self.default_is_radian

        Returns:

        """
        return self.arm.set_reduced_joint_range(joint_range, is_radian=is_radian)

    def set_fence_mode(self, on):
        """
        Turn on/off fence mode

        Note:
            1. This interface relies on Firmware 1.2.11 or above

        Args:
            on: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_fense_mode(on)
    
    def set_collision_rebound(self, on):
        """
        Turn on/off collision rebound

        Note:
            1. This interface relies on Firmware 1.2.11 or above

        Args:
            on: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_collision_rebound(on)
    
    def set_world_offset(self, offset, is_radian=None, wait=True):
        """
        Set the base coordinate offset

        Note:
            1. This interface relies on Firmware 1.2.11 or above

        Args:
            offset: [x, y, z, roll, pitch, yaw]
            
            is_radian: if the roll/pitch/yaw is in radians or not, defaults to self.default_is_radian
            
            wait: whether to wait for the robotic arm to stop or all previous queue commands to be executed/cleared before setting

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_world_offset(offset, is_radian=is_radian, wait=wait)

    def is_tcp_limit(self, pose, is_radian=None):
        """
        Check the tcp pose is within limit

        Args:
            pose: [x, y, z, roll, pitch, yaw]
            
            is_radian: roll/pitch/yaw value is radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, limit)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            limit: True/False/None, limit or not, or failed
        """
        return self.arm.is_tcp_limit(pose, is_radian=is_radian)
    
    def is_joint_limit(self, joint, is_radian=None):
        """
        Check the joint angle is within limit

        Args:
            joint: [angle-1, angle-2, ..., angle-n], n is the number of axes of the arm
            
            is_radian: angle value is radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, limit)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            limit: True/False/None, limit or not, or failed
        """
        return self.arm.is_joint_limit(joint, is_radian=is_radian)
    
    def get_servo_debug_msg(self, show=False, lang='en'):
        """
        Get the servo debug msg, used only for debugging

        Args:
            show: show the detail info if True
        
            lang: language, en/cn, default is en

        Returns:
            out: tuple((code, servo_info_list)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_debug_msg(show=show, lang=lang)
    
    def get_gripper_version(self):
        """
        Get gripper version, only for debug

        Returns:
            out: (code, version)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_gripper_version()

    def get_servo_version(self, servo_id=1):
        """
        Get servo version, only for debug

        Args:
            servo_id: servo id(1~7)

        Returns:
            out: (code, version)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_servo_version(servo_id=servo_id)

    def get_tgpio_version(self):
        """
        Get tool gpio version, only for debug

        Returns:
            out: (code, version)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_tgpio_version()
    
    def get_harmonic_type(self, servo_id=1):
        """
        Get harmonic type, only for debug

        Returns:
            out: (code, type)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_harmonic_type(servo_id=servo_id)

    def get_hd_types(self):
        """
        Get harmonic types, only for debug

        Returns:
            out: (code, types)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_hd_types()
    
    def set_counter_reset(self):
        """
        Reset counter value

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_counter_reset()

    def set_counter_increase(self, val=1):
        """
        Set counter plus value, only supports increasing by 1

        Args:
            val: reversed

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_counter_increase(val)
    
    def get_joints_torque(self):
        """
        Get joint torque
        
        Returns:
            out: tuple((code, joints_torque))

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            joints_torque: joint torque
        """
        return self.arm.get_joints_torque()
    
    def set_timeout(self, timeout):
        """
        Set the timeout of cmd response

        Args:
            timeout: seconds
        """
        return self.arm.set_timeout(timeout)
    
    def set_baud_checkset_enable(self, enable):
        """
        Enable auto checkset the baudrate of the end IO board or not

        Note:
            only available in the API of gripper/bio/robotiq/linear_motor.
            
        Args:
            enable: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_baud_checkset_enable(enable)

    def set_checkset_default_baud(self, type_, baud):
        """
        Set the checkset baud value
        
        Args:
            type_: checkset type
                - 1: xarm gripper
                - 2: bio gripper
                - 3: robotiq gripper
                - 4: linear motor
            
            baud: checkset baud value, less than or equal to 0 means disable checkset

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_checkset_default_baud(type_, baud)

    def get_checkset_default_baud(self, type_):
        """
        Get the checkset baud value

        Args:
            type_: checkset type
                - 1: xarm gripper
                - 2: bio gripper
                - 3: robotiq gripper
                - 4: linear motor

        Returns:
            out: tuple((code, baud))

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            baud: the checkset baud value
        """
        return self.arm.get_checkset_default_baud(type_)
    
    def calibrate_tcp_coordinate_offset(self, four_points, is_radian=None):
        """
        Four-point method to calibrate tool coordinate system position offset
        Note:
            1. only available if firmware_version >= 1.6.9

        Args:
            four_points: a list of four teaching coordinate positions [x, y, z, roll, pitch, yaw]
            
            is_radian: if the roll/pitch/yaw value of each point is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, xyz_offset)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            xyz_offset: calculated xyz(mm) TCP offset, [x, y, z] 
        """
        return self.arm.calibrate_tcp_coordinate_offset(four_points, is_radian=is_radian)
    
    def calibrate_tcp_orientation_offset(self, rpy_be, rpy_bt, input_is_radian=None, return_is_radian=None):
        """
        An additional teaching point to calibrate the tool coordinate system attitude offset

        Note:
            1. only available if firmware_version >= 1.6.9

        Args:
            rpy_be: the rpy value of the teaching point without TCP offset [roll, pitch, yaw]
            
            rpy_bt: the rpy value of the teaching point with TCP offset [roll, pitch, yaw]
            
            input_is_radian: if the roll/pitch/yaw value of rpy_be and rpy_bt is in radians or not, defaults to self.default_is_radian
            
            return_is_radian: if the roll/pitch/yaw value of result is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, rpy_offset)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            rpy_offset: calculated rpy TCP offset, [roll, pitch, yaw]
        """
        return self.arm.calibrate_tcp_orientation_offset(rpy_be, rpy_bt, input_is_radian=input_is_radian, return_is_radian=return_is_radian)

    def calibrate_user_orientation_offset(self, three_points, mode=0, trust_ind=0, input_is_radian=None, return_is_radian=None):
        """
        Three-point method teaches user coordinate system posture offset

        Note:
            1. only available if firmware_version >= 1.6.9
            2. First determine a point in the working space, move along the desired coordinate system x+ to determine the second point,
            and then move along the desired coordinate system y+ to determine the third point. 
            3. Note that the x+ direction is as accurate as possible. 
            4. If the y+ direction is not completely perpendicular to x+, it will be corrected in the calculation process.

        Args:
            three_points: a list of teaching TCP coordinate positions [x, y, z, roll, pitch, yaw]
            
            input_is_radian: if the roll/pitch/yaw value of each point is in radians or not, defaults to self.default_is_radian
            
            return_is_radian: if the roll/pitch/yaw value of the result should be in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, rpy_offset)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            rpy_offset: calculated rpy user offset, [roll, pitch, yaw]
        """
        return self.arm.calibrate_user_orientation_offset(three_points, mode=mode, trust_ind=trust_ind, input_is_radian=input_is_radian, return_is_radian=return_is_radian)
    
    def calibrate_user_coordinate_offset(self, rpy_ub, pos_b_uorg, is_radian=None):
        """
        An additional teaching point determines the position offset of the user coordinate system.
        Note:
            1. only available if firmware_version >= 1.6.9

        Args:
            rpy_ub: the confirmed offset of the base coordinate system in the user coordinate system [roll, pitch, yaw], the result of calibrate_user_orientation_offset()
            
            pos_b_uorg: the position of the teaching point in the base coordinate system [x, y, z], if the arm cannot reach the target position, the user can manually input the position of the target in the base coordinate.
            
            is_radian: if the roll/pitch/yaw value of rpy_ub is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, xyz_offset)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            xyz_offset: calculated xyz(mm) user offset, [x, y, z] 
        """
        return self.arm.calibrate_user_coordinate_offset(rpy_ub, pos_b_uorg, is_radian=is_radian)
    
    def set_simulation_robot(self, on_off):
        """
        Set the simulation robot
        
        Args:
            on_off: True/False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_simulation_robot(on_off)
    
    def get_base_board_version(self, board_id=10):
        """
         Get base board version

        Args:
            board_id: int

        Returns:
            out: (code, version)

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_base_board_version(board_id)
    
    def iden_tcp_load(self, estimated_mass=0):
        """
        Identification the tcp load with current

        Note:
            1. only available if firmware_version >= 1.8.0
        
        Args:
            estimated_mass: estimated mass

                Note: this parameter is only available on the lite6 model manipulator, and this parameter must be specified for the lite6 model manipulator

        Returns:
            out: tuple((code, load)) returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            load: [mass, x_centroid, y_centroid, z_centroid]

        """
        return self.arm.iden_tcp_load(estimated_mass)
    
    def get_initial_point(self):
        """
        Get the initial point from studio
        
        Returns:
            out: tuple((code, point)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            point: initial point, [J1, J2, ..., J7]
        """
        return self.arm._studio.get_initial_point()
    
    def set_initial_point(self, point):
        """
        Set the initial point
        
        Args:
            point: initial point, [J1, J2, ..., J7]
        
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details. 
        """
        return self.arm._studio.set_initial_point(point)
    
    def get_mount_direction(self):
        """
        Get the mount degrees from studio

        Returns:
            out: tuple((code, degrees)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            degrees: mount degrees, [tilt angle, rotate angle]
        """
        return self.arm._studio.get_mount_direction()
    
    def set_cartesian_velo_continuous(self, on_off):
        """
        Set cartesian motion velocity continuous

        Note:
            1. only available if firmware_version >= 1.9.0
        
        Args:
            on_off: whether motion is continuous or not, True: continuous, defaults to False
        
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_cartesian_velo_continuous(on_off)

    def set_allow_approx_motion(self, on_off):
        """
        Settings to allow avoiding overspeed near some singularities using approximate solutions
        
        Note:
            1. only available if firmware_version >= 1.9.0

        Args:
            on_off: whether to allow or not, True: allow, default is False

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_allow_approx_motion(on_off)
    
    def get_allow_approx_motion(self):
        """
        Obtain whether to enable approximate solutions to avoid certain singularities

        Note:
            1. only available if firmware_version >= 1.9.0

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_allow_approx_motion()
    
    def get_joint_states(self, is_radian=None, num=3):
        """
        Get the joint states

        Note:
            1. only available if firmware_version >= 1.9.0

        Args:
            is_radian: if the returned value(position and velocity) is in radians or not, defaults to self.default_is_radian

        Returns:
            out: tuple((code, [position, velocity, effort])), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            position: the angles of joints, like [angle-1, ..., angle-7]

            velocity: the velocities of joints, like [velo-1, ..., velo-7]

            effort: the efforts of joints, like [effort-1, ..., effort-7]
        """
        return self.arm.get_joint_states(is_radian=is_radian, num=num)
    
    def iden_joint_friction(self, sn=None):
        """
        Identification of the friction

        Note:
            1. only available if firmware_version >= 1.9.0
        
        Args:
            sn: sn value

        Returns:
            out: tuple((code, result)) returned result is only corrent when code is 0.

            code:  See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            result: 
                - 0: success
                - -1: failure
        """
        return self.arm.iden_joint_friction(sn)
    
    def set_only_check_type(self, only_check_type=0):
        """
        Set the motion process detection type (valid for all motion interfaces of the current SDK instance)

        Note:
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

        Args:
            only_check_type: Motion Detection Type
                - only_check_type == 0: Restore the original function of the motion interface, it will move, the default is 0
                - only_check_type == 1: Only check the self-collision without moving, take the actual state of the manipulator as the initial planned path, and check whether the path has self-collision (the intermediate state will be updated at this time)
                - only_check_type == 2: Only check the self-collision without moving, use the intermediate state as the starting planning path, check whether the path has self-collision (the intermediate state will be updated at this time), and restore the intermediate state to the actual state after the end
                - only_check_type == 3: Only check the self-collision without moving, use the intermediate state as the starting planning path, and check whether the path has self-collision (the intermediate state will be updated at this time)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_only_check_type(only_check_type)
    
    def get_dh_params(self):
        """
        Get the DH parameters
        
        Note:
            1. only available if firmware_version >= 2.0.0
        
        Returns:
            out: tuple((code, dh_params)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            dh_params: DH parameters
               - dh_params[0:4]: DH parameters of Joint-1
               - dh_params[4:8]: DH parameters of Joint-2
               - ...
               - dh_params[24:28]: DH parameters of Joint-7
        """
        return self.arm.get_dh_params()
    
    def set_dh_params(self, dh_params, flag=0):
        """
        Set the DH parameters

        Note:
            1. only available if firmware_version >= 2.0.0
            2. this interface is only provided for users who need to use external DH parameters, ordinary users should not try to modify DH parameters.
        
        Args:
            dh_params: DH parameters
            
            flag: 
                - 0: Use the set DH parameters, but do not write to the configuration file
                - 1: Use the set DH parameters and write to the configuration file
                - 2: Use the set DH parameters and delete the DH parameters of the configuration file
                - 3: Use the default DH parameters, but will not delete the DH parameters of the configuration file
                - 4: Use the default DH parameters and delete the DH parameters of the configuration file

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_dh_params(dh_params, flag) 
    
    def set_feedback_type(self, feedback_type):
        """
        Set the feedback type

        Note:
            1. only available if firmware_version >= 2.1.0
            2. only works in position mode
            3. the setting will only affect subsequent tasks and will not affect previously cached tasks
            4. only valid for the current connection
        
        Args:
            feedback_type:
                - 0: disable feedback
                - 1: feedback when the motion task starts executing
                - 2: feedback when the motion task execution ends or motion task is discarded(usually when the distance is too close to be planned)
                - 4: feedback when the non-motion task is triggered

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_feedback_type(feedback_type)
    
    def set_linear_spd_limit_factor(self, factor):
        """
        Set linear speed limit factor (default is 1.2)

        Note:
            1. only available if firmware_version >= 2.3.0
            2. only available in mode 1

        Args:
            factor: speed limit factor

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_linear_spd_limit_factor(factor)
    
    def set_cmd_mat_history_num(self, num):
        """
        Set cmd mat history num

        Note:
            Only available if firmware_version >= 2.3.0

        Args:
            num: history num

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_cmd_mat_history_num(num)
    
    def set_fdb_mat_history_num(self, num):
        """
        Set fdb mat history num

        Note:
            Only available if firmware_version >= 2.3.0

        Args:
            num: history num

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_fdb_mat_history_num(num)
    
    def get_linear_spd_limit_factor(self):
        """
        Get linear speed limit factor

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, factor)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            factor: linear speed limit factor
        """
        return self.arm.get_linear_spd_limit_factor()
    
    def get_cmd_mat_history_num(self):
        """
        Get cmd mat history num

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, num)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            num: cmd mat history num
        """
        return self.arm.get_cmd_mat_history_num()
    
    def get_fdb_mat_history_num(self):
        """
        Get fdb mat history num

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, num)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            num: fdb mat history num
        """
        return self.arm.get_fdb_mat_history_num()
    
    def get_poe_status(self):
        """
        Get poe status

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, status)), returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: 1 means poe is valid, 0 means poe is invalid
        """
        return self.arm.get_poe_status()
    
    def get_iden_status(self):
        """
        Get iden status

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, status)), returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status: 1 means in identifying, 0 means not in identifying
        """
        return self.arm.get_iden_status()    
    
    def set_external_device_monitor_params(self, dev_type, frequency):
        """
        Set the monitor params of the external device

        Note:
            1. only available if firmware_version >= 2.7.100
            2. after it is turned on, the position/speed/current information of the external device will be reported through port 30000
            3. once an error occurs, you need to re call to monitor

        Args:
            dev_type: the type of the external device
                - 0: Turn off monitoring
                - 1: xArm Gripper
                - 2: xArm Gripper G2
                - 3: BIO Gripper G2
                - 4: Robotiq 2F-85/Robotiq 2F-140
            
            frequency: the frequency of communication with the external device

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_external_device_monitor_params(dev_type, frequency)
    
    def get_external_device_monitor_params(self):
        """
        Get the monitor params of the external device

        Note:
            1. only available if firmware_version >= 2.7.100

        Returns:
            out: tuple((code, params)), returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            params: [dev_type, frequency]
        """
        return self.arm.get_external_device_monitor_params()