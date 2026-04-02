from xarm.wrapper import XArmAPI

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

    def clean_warn(self):
        """
        Clean the warn

        \n:return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_warn()

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

    def emergency_stop(self):
        """
        Emergency stop (set_state(4) -> motion_enable(True) -> set_state(0))
        \nNote:
            1. This interface does not automatically clear errors. If there is an error, you will need to handle it according to the error code.
        """
        return self.arm.emergency_stop()
    
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
    
    def delete_blockly_app(self, name):
        """
        Delete blockly app
        
        :param name: blockly app name
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm._studio.delete_blockly_app(name)   
    
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
    
    def run_gcode_app(self, path, **kwargs):
        """
        Run gcode project file by xArmStudio software

        :param path: gcode file path
        
        :return: code, returned result is only corrent when code is 0.
        """
        return self.arm.run_gcode_app(self, path, **kwargs)