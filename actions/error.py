from xarm.wrapper import XArmAPI

class arm_errors():

    def __init__(self, arm:XArmAPI):
        self.arm = arm

    def get_err_warn_code(self, show=False, lang='en'):
        """
        Get the controller error and warn code

        Args:
            show: show the detail info if True
            
            lang: show language, en/cn, degault is en, only available if show is True

        Returns:
            out: tuple((code, [error_code, warn_code])), returned result is only corrent when code is 0.
        
            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            error_code: See the [Controller Error Code Documentation](./xarm_api_code.md#controller-error-code) for details.

            warn_code: See the [Controller Warn Code Documentation](./xarm_api_code.md#controller-warn-code) for details.
        """
        return self.arm.get_err_warn_code(show=show, lang=lang)
    
    def clean_error(self):
        """
        Clean the error, need to manually enable motion(arm.motion_enable(True)) and set state(arm.set_state(state=0)) after error cleaned

        Returns:
            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.
        """
        return self.arm.clean_error()
    
    def get_c31_error_info(self):
        """
        Get collision error (C31) info

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.
            
            err_info: [servo_id, theoratival tau, actual tau]
        """
        return self.arm.get_c31_error_info()
    
    def get_c37_error_info(self, is_radian=None):
        """
        Get payload error (C37) info

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info: [servo_id, angle]
        """
        return self.arm.get_c37_error_info(is_radian)
    
    def get_c23_error_info(self, is_radian=None):
        """
        Get joint angle limit error (C23) info

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out (tuple[int, tuple]): tuple((code, err_info)), returned result is only corrent when code is 0.

            code (int): See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info (tuple): [(servo_id, angle), ...]
        """
        return self.get_c23_error_info(is_radian)
    
    def get_c24_error_info(self, is_radian=None):
        """
        Get joint speed limit error (C24) info

        Note:
            Only available if firmware_version >= 2.3.0

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info: [servo_id, speed]
        """
        return self.arm.get_c24_error_info(is_radian)
    
    def get_c60_error_info(self):
        """
        Get linear speed limit error (C60) info

        Note:
            1. Only available if firmware_version >= 2.3.0
            2. Only available in mode 1

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info: [max_linear_speed, curr_linear_speed]
        """
        return self.arm.get_c60_error_info()
    
    def get_c38_error_info(self, is_radian=None):
        """
        Get joint hard angle limit error (C38) info

        Note:
            Only available if firmware_version >= 2.4.0

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info: [(servo_id, angle), ...]
        """
        return self.arm.get_c38_error_info(is_radian)
    
    def get_c54_error_info(self):
        """
        Get Six-axis Force Torque Sensor collision error (C54) info

        Note:
            Only available if firmware_version >= 2.6.103

        Returns:
            out: tuple((code, err_info)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](xarm_api_code.md#api-code) for details.

            err_info: [dir, tau threshold, actual tau]
        """
        return self.arm.get_c54_error_info()