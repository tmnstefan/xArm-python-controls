from xarm import XArmAPI

class gripper_control():

    def __init__(self, arm:XArmAPI):
        self.arm = arm


    def set_gripper_enable(self, enable, **kwargs):
        """
        Enable the gripper

        :param enable: enable or not

            Note: such as code = arm.set_gripper_enable(True) to turn on the Gripper
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gripper_enable(enable, **kwargs)

    def set_gripper_mode(self, mode, **kwargs):
        """
        Set the gripper mode

        :param mode: 0: location mode
            
            Note: such as code = arm.set_gripper_mode(0)
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gripper_mode(mode, **kwargs)
    
    def set_gripper_speed(self, speed, **kwargs):
        """
        Set the gripper speed

        :param speed:
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gripper_speed(speed, **kwargs)
    
    def set_gripper_position(self, pos, wait=False, speed=None, auto_enable=False, timeout=None, **kwargs):
        """
        Set the gripper position

        :param pos: position
        :param wait: wait or not, default is False
        :param speed: speed, unit: r/min
        :param auto_enable: auto enable or not, default is False
        :param timeout: wait time, unit: second, default is 10s
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gripper_position(pos, wait=wait, speed=speed, auto_enable=auto_enable, timeout=timeout, **kwargs)
    
    def get_gripper_position(self, **kwargs):
        """
        Get the gripper position (pulse)

        :return: tuple((code, pos)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_gripper_position(**kwargs)
    
    def get_gripper_err_code(self, **kwargs):
        """
        Get the gripper error code

        :return: tuple((code, err_code)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerr_code: See the [Gripper Error Code Documentation](./xarm_api_code.md#gripper-error-code) for details.
        """
        return self.arm.get_gripper_err_code(**kwargs)
    
    def clean_gripper_error(self, **kwargs):
        """
        Clean the gripper error

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_gripper_error(**kwargs)
    
    def get_gripper_status(self):
        """
        Get the status of the xArm Gripper

        Note:
            1. Only available if gripper_version >= 3.4.3

        :return: tuple((code, status)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstatus:
            \n    status & 0x03 == 0: stop state
            \n    status & 0x03 == 1: move state 
            \n    status & 0x03 == 2: grasp state
        """
        return self.arm.get_gripper_status()
    
    def get_gripper_g2_position(self, **kwargs):
        """
        Get the position (mm) of the xArm Gripper G2

        :return: tuple((code, pos)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_gripper_g2_position(**kwargs)
    
    def set_gripper_g2_position(self, pos, speed=100, force=50, wait=False, timeout=None, **kwargs):
        """
        Set the position of the xArm Gripper G2

        :param pos: gripper pos between 0 and 84, (unit: mm)
        :param speed: gripper speed between 15 and 225, default is 100, (unit: mm/s)
        :param force: gripper force between 1 and 100, default is 50
        :param wait: whether to wait for the xArm Gripper G2 motion to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is 10s, only valid if wait is True
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_gripper_g2_position(pos, speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)
    
    def set_bio_gripper_enable(self, enable=True, wait=True, timeout=3):
        """
        Enable the bio gripper
        
        :param enable: enable or not
        :param wait: whether to wait for the bio gripper enable to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 3, only available if wait=True
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_bio_gripper_enable(enable, wait=wait, timeout=timeout)

    def set_bio_gripper_speed(self, speed):
        """
        Set the speed of the bio gripper
        
        :param speed: speed
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_bio_gripper_speed(speed)

    def set_bio_gripper_control_mode(self, mode):
        """
        Set the bio gripper control mode

        Note:
            1. Only available in the new version of BIO Gripper

        :param mode: mode
            0: bio gripper opening and closing mode
            1: position loop mode

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        
        return self.arm.set_bio_gripper_control_mode(mode)

    def set_bio_gripper_force(self, force):
        """
        Set the bio gripper force

        Note:
            1. Only available in the new version of BIO Gripper

        :param force: gripper force between 10 and 100

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """

        return self.arm.set_bio_gripper_force(force)

    def get_bio_gripper_g2_position(self, **kwargs):
        """
        Get the position (mm) of the BIO Gripper G2

        :return: tuple((code, pos)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.get_bio_gripper_g2_position(**kwargs)

    def set_bio_gripper_g2_position(self, pos, speed=2000, force=100, wait=True, timeout=5, **kwargs):
        """
        Set the position of BIO Gripper G2

        :param pos: gripper pos between 71 and 150, (unit: mm)
        :param speed: gripper speed between 500 and 4500, default is 2000, (unit: pulse/s)
        :param force: gripper force between 1 and 100, default is 100
        :param wait: whether to wait for the BIO Gripper G2 motion to complete, default is False
        :param timeout: maximum waiting time(unit: second), default is 5, only available if wait=True

        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            robotiq_response: See the robotiq documentation
        """
        return self.arm.set_bio_gripper_g2_position(pos, speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)

    def open_bio_gripper(self, speed=0, wait=True, timeout=5, **kwargs):
        """
        Open the bio gripper
        
        :param speed: speed value, default is 0 (speed not set)
        :param wait: whether to wait for the bio gripper motion to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 5, only available if wait=True
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.open_bio_gripper(speed=speed, wait=wait, timeout=timeout, **kwargs)

    def close_bio_gripper(self, speed=0, wait=True, timeout=5, **kwargs):
        """
        Close the bio gripper
        
        :param speed: speed value, default is 0 (speed not set)
        :param wait: whether to wait for the bio gripper motion complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 5, only available if wait=True
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.close_bio_gripper(speed=speed, wait=wait, timeout=timeout, **kwargs)

    def get_bio_gripper_status(self):
        """
        Get the status of the bio gripper
        
        :return: tuple((code, status))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstatus: status
            \n    status & 0x03 == 0: stop
            \n    status & 0x03 == 1: motion
            \n    status & 0x03 == 2: catch
            \n    status & 0x03 == 3: error
            \n    (status >> 2) & 0x03 == 0: not enabled
            \n    (status >> 2) & 0x03 == 1: enabling
            \n    (status >> 2) & 0x03 == 2: enabled
        """
        return self.arm.get_bio_gripper_status()

    def get_bio_gripper_error(self):
        """
        Get the error code of the bio gripper
        
        :return: tuple((code, error_code))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nerror_code: See the [Bio Gripper Error Code Documentation](./xarm_api_code.md#bio-gripper-error-code) for details. 
        """
        return self.arm.get_bio_gripper_error()

    def clean_bio_gripper_error(self):
        """
        Clean the error code of the bio gripper
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_bio_gripper_error()
    
    def robotiq_reset(self):
        """
        Reset the robotiq gripper (clear previous activation if any)
        
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation
        """
        return self.arm.robotiq_reset()

    def robotiq_set_activate(self, wait=True, timeout=3):
        """
        Activate the robotiq gripper if it is not already active
        
        :param wait: whether to wait for the robotiq activate to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 3, only available if wait=True
        
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation 
        """
        return self.arm.robotiq_set_activate(wait=wait, timeout=timeout)

    def robotiq_set_position(self, pos, speed=0xFF, force=0xFF, wait=True, timeout=5, **kwargs):
        """
        Go to the position with determined speed and force.
        
        :param pos: position of the gripper. Integer between 0 and 255. 0 being the open position and 255 being the close position.
        :param speed: gripper speed between 0 and 255
        :param force: gripper force between 0 and 255
        :param wait: whether to wait for the robotiq motion complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 5, only available if wait=True
        
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation 
        """
        return self.arm.robotiq_set_position(pos, speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)

    def robotiq_open(self, speed=0xFF, force=0xFF, wait=True, timeout=5, **kwargs):
        """
        Open the robotiq gripper
        
        :param speed: gripper speed between 0 and 255
        :param force: gripper force between 0 and 255
        :param wait: whether to wait for the robotiq motion to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 5, only available if wait=True
        
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation 
        """
        return self.arm.robotiq_open(speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)

    def robotiq_close(self, speed=0xFF, force=0xFF, wait=True, timeout=5, **kwargs):
        """
        Close the robotiq gripper
        
        :param speed: gripper speed between 0 and 255
        :param force: gripper force between 0 and 255
        :param wait: whether to wait for the robotiq motion to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 3, only available if wait=True
        
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation
        """
        return self.arm.robotiq_close(speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)

    def robotiq_get_status(self, number_of_registers=3):
        """
        Reading the status of robotiq gripper
        
        :param number_of_registers: number of registers, 1/2/3, default is 3
        
            number_of_registers=1: reading the content of register 0x07D0

            number_of_registers=2: reading the content of register 0x07D0/0x07D1
            
            number_of_registers=3: reading the content of register 0x07D0/0x07D1/0x07D2
            
            Note: 
                \nregister 0x07D0: Register GRIPPER STATUS
                \nregister 0x07D1: Register FAULT STATUS and register POSITION REQUEST ECHO
                \nregister 0x07D2: Register POSITION and register CURRENT
        :return: tuple((code, robotiq_response))
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nrobotiq_response: See the robotiq documentation
        """
        return self.arm.robotiq_get_status(number_of_registers=number_of_registers)
    
    def get_vacuum_gripper(self, hardware_version=1):
        """
        Get the state of the Vacuum Gripper

        :param hardware_version: hardware version
            \n1: Plug-in Connection, default
            \n2: Contact Connection
        \n:return: tuple((code, state)), returned result is only corrent when code is 0.
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
            \nstate: state of the Vacuum Gripper
            \n -1: Vacuum Gripper is off  
            \n 0: Object not picked by vacuum gripper 
            \n 1: Object picked by vacuum gripper
        """
        return self.arm.get_vacuum_gripper(hardware_version=hardware_version, check_on=True)

    def set_vacuum_gripper(self, on, wait=False, timeout=3, delay_sec=None, sync=True, hardware_version=1):
        """
        Set the Vacuum Gripper ON/OFF

        :param on: open or not

            on=True: equivalent to calling `set_tgpio_digital(0, 1)` and `set_tgpio_digital(1, 0)`

            on=False: equivalent to calling `set_tgpio_digital(0, 0)` and `set_tgpio_digital(1, 1)`

        :param wait: wait the object picked by the vacuum gripper or not, default is False
        :param timeout: wait time, unit:second, default is 3s
        :param delay_sec: delay effective time from the current start, in seconds, default is None(effective immediately)
        :param sync: whether to execute in the motion queue, set to False to execute immediately(default is True)

            1. only available if firmware_version >= 2.4.101

            2. only available if delay_sec <= 0

        :param hardware_version: hardware version

            1: Plug-in Connection, default

            2: Contact Connection

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_vacuum_gripper(on, wait=wait, timeout=timeout, delay_sec=delay_sec, sync=sync, hardware_version=hardware_version)
    
    def set_dhpgc_gripper_activate(self, wait=True, timeout=3):
        """
        Activate the DH-PGC-140-50 gripper if it is not already active

        :param wait: whether to wait for the DH-PGC-140-50  gripper activate complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 3, only available if wait=True

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_dhpgc_gripper_activate(wait=wait, timeout=timeout)
        
    def set_dhpgc_gripper_position(self, pos, speed=50, force=50, wait=True, timeout=5, **kwargs):
        """
        Set the position of the DH-PGC-140-50 gripper

        :param pos: gripper pos between 0 and 1000
        :param speed: gripper speed between 1 and 100
        :param force: gripper force between 20 and 100
        :param wait: whether to wait for the DH-PGC-140-50 gripper motion to complete, default is True
        :param timeout: maximum waiting time(unit: second), default is 5s, only available if wait=True

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.set_dhpgc_gripper_position(pos, speed=speed, force=force, wait=wait, timeout=timeout, **kwargs)
    
    def open_lite6_gripper(self, sync=True):
        """
        Open the gripper of Lite6 series robotic arms

        Note:
            1. only available if firmware_version >= 1.10.0
            2. this API can only be used on Lite6 series robotic arms

        :param sync: whether to execute in the motion queue, set to False to execute immediately(default is True)

            1. only available if firmware_version >= 2.4.101
            
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details. 
        """
        return self.arm.open_lite6_gripper(sync=sync)

    def close_lite6_gripper(self, sync=True):
        """
        Close the gripper of Lite6 series robotic arms

        Note:
            1. only available if firmware_version >= 1.10.0
            2. this API can only be used on Lite6 series robotic arms

        :param sync: whether to execute in the motion queue, set to False to execute immediately(default is True)

            1. only available if firmware_version >= 2.4.101

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.close_lite6_gripper(sync=sync)

    def stop_lite6_gripper(self, sync=True):
        """
        Stop the gripper of Lite6 series robotic arms

        Note:
            1. only available if firmware_version >= 1.10.0
            2. this API can only be used on Lite6 series robotic arms

        :param sync: whether to execute in the motion queue, set to False to execute immediately(default is True)

            1. only available if firmware_version >= 2.4.101

        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.stop_lite6_gripper(sync=sync)