from xarm.wrapper import XArmAPI

class register_release_control():

    def __init__(self, arm:XArmAPI):
        self.arm = arm

    def register_report_callback(self, callback=None, report_cartesian=True, report_joints=True,
                                 report_state=True, report_error_code=True, report_warn_code=True,
                                 report_mtable=True, report_mtbrake=True, report_cmd_num=True):
        """
        Register the report callback, only available if enable_report is True

        Args: 
            callback:

                callback data

                {
                
                'cartesian': [], # if report_cartesian is True

                'joints': [], # if report_joints is True

                'error_code': 0, # if report_error_code is True

                'warn_code': 0, # if report_warn_code is True

                'state': state, # if report_state is True

                'mtbrake': mtbrake, # if report_mtbrake is True, and available if enable_report is True and the connection method is socket

                'mtable': mtable, # if report_mtable is True, and available if enable_report is True and the connection method is socket

                'cmdnum': cmdnum, # if report_cmd_num is True
                
                }

            report_cartesian: report cartesian or not, default is True
        
            report_joints: report joints or not, default is True
        
            report_state: report state or not, default is True
        
            report_error_code: report error or not, default is True
        
            report_warn_code: report warn or not, default is True
        
            report_mtable: report motor enable states or not, default is True
        
            report_mtbrake: report motor brake states or not, default is True
        
            report_cmd_num: report cmdnum or not, default is True
                
        Returns:
            out: True/False
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

        Args:
            callback:

                callback data:

                {
                
                "cartesian": [x, y, z, roll, pitch, yaw], ## if report_cartesian is True

                "joints": [angle-1, angle-2, angle-3, angle-4, angle-5, angle-6, angle-7], ## if report_joints is True
                
                }

            report_cartesian: report or not, True/False, default is True
            
            report_joints: report or not, True/False, default is True
        
        Returns:
            out: True/False
        """
        return self.arm.register_report_location_callback(callback=callback,
                                                           report_cartesian=report_cartesian,
                                                           report_joints=report_joints)

    def register_connect_changed_callback(self, callback=None):
        """
        Register the connect status changed callback

        Args:
            callback:

                callback data:

                {
                
                "connected": connected,

                "reported": reported,
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_connect_changed_callback(callback=callback)

    def register_state_changed_callback(self, callback=None):
        """
        Register the state status changed callback, only available if enable_report is True

        Args:
            callback:

                callback data:

                {
                
                "state": state,
                
                }

        
        Returns:
            out: True/False
        """
        return self.arm.register_state_changed_callback(callback=callback)

    def register_mode_changed_callback(self, callback=None):
        """
        Register the mode changed callback, only available if enable_report is True and the connection method is socket

        Args:
            callback:

                callback data:

                {
                
                "mode": mode,
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_mode_changed_callback(callback=callback)

    def register_mtable_mtbrake_changed_callback(self, callback=None):
        """
        Register the motor enable states or motor brake states changed callback, only available if enable_report is True and the connection method is socket

        Args:
            callback:

                callback data:

                {
                
                "mtable": [motor-1-motion-enable, motor-2-motion-enable, ...],
                
                "mtbrake": [motor-1-brake-enable, motor-1-brake-enable,...],
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_mtable_mtbrake_changed_callback(callback=callback)

    def register_error_warn_changed_callback(self, callback=None):
        """
        Register the error code or warn code changed callback, only available if enable_report is True

        Args:
            callback:

                callback data:

                {

                "error_code": error_code,

                "warn_code": warn_code,

                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_error_warn_changed_callback(callback=callback)

    def register_cmdnum_changed_callback(self, callback=None):
        """
        Register the cmdnum changed callback, only available if enable_report is True

        Args:
            callback:

                callback data:

                {
                
                "cmdnum": cmdnum
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_cmdnum_changed_callback(callback=callback)

    def register_temperature_changed_callback(self, callback=None):
        """
        Register the temperature changed callback, only available if enable_report is True

        Args:
            callback:

                callback data:

                {
                
                "temperatures": [servo-1-temperature, ...., servo-7-temperature]
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_temperature_changed_callback(callback=callback)

    def register_count_changed_callback(self, callback=None):
        """
        Register the counter value changed callback, only available if enable_report is True

        Args:
            callback:

                callback data:

                {
                
                "count": counter value
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_count_changed_callback(callback=callback)

    def register_iden_progress_changed_callback(self, callback=None):
        """
        Register the Identification progress value changed callback, only available if enable_report is True
        
        Args:
            callback: 

                callback data:
                
                {
                
                "progress": progress value
                
                }
        
        Returns:
            out: True/False
        """
        return self.arm.register_iden_progress_changed_callback(callback=callback)
    
    def release_report_callback(self, callback=None):
        """
        Release the report callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_report_callback(callback)
    

    def release_report_location_callback(self, callback=None):
        """
        Release the location report callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_report_location_callback(callback)
    
    def release_connect_changed_callback(self, callback=None):
        """
        Release the connect changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_connect_changed_callback(callback)

    def release_state_changed_callback(self, callback=None):
        """
        Release the state changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_state_changed_callback(callback)

    def release_mode_changed_callback(self, callback=None):
        """
        Release the mode changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_mode_changed_callback(callback)

    def release_mtable_mtbrake_changed_callback(self, callback=None):
        """
        Release the motor enable states or motor brake states changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_mtable_mtbrake_changed_callback(callback)

    def release_error_warn_changed_callback(self, callback=None):
        """
        Release the error warn changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_error_warn_changed_callback(callback)

    def release_cmdnum_changed_callback(self, callback=None):
        """
        Release the cmdnum changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_cmdnum_changed_callback(callback)

    def release_temperature_changed_callback(self, callback=None):
        """
        Release the temperature changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_temperature_changed_callback(callback=callback)

    def release_count_changed_callback(self, callback=None):
        """
        Release the counter value changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_count_changed_callback(callback=callback)

    def release_iden_progress_changed_callback(self, callback=None):
        """
        Release the Identification progress value changed callback

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_iden_progress_changed_callback(callback=callback)
    
    def register_feedback_callback(self, callback=None):
        """
        Register the callback of feedback

        Note:
            1. only available if firmware_version >= 2.1.0

        Args:
            callback:

                callback data: bytes data:

                data[0:2]: transaction id, (Big-endian conversion to unsigned 16-bit integer data), command ID corresponding to the feedback, consistent with issued instructions

                    Note: this can be used to distinguish which instruction the feedback belongs to

                data[4:6]: feedback_length, feedback_length == len(data) - 6, (Big-endian conversion to unsigned 16-bit integer data)

                data[8]: feedback type

                    1: the motion task starts executing

                    2: the motion task execution ends or motion task is discarded(usually when the distance is too close to be planned)

                    4: the non-motion task is triggered

                data[9]: feedback funcode, command code corresponding to feedback, consistent with issued instructions

                    Note: this can be used to distinguish what instruction the feedback belongs to

                data[10:12]: feedback taskid, (Big-endian conversion to unsigned 16-bit integer data)

                data[12]: feedback code, execution status code, generally only meaningful when the feedback type is end, normally 0, 2 means discarded

                data[13:21]: feedback us, (Big-endian conversion to unsigned 64-bit integer data), time when feedback triggers (microseconds)

                    Note: this time is the corresponding controller system time when the feedback is triggered
        
        Returns:
            out: True/False
        """
        return self.arm.register_feedback_callback(callback=callback)

    def release_feedback_callback(self, callback=None):
        """
        Release the callback of feedback

        Note:
            1. only available if firmware_version >= 2.1.0

        Args:
            callback:
        
        Returns:
            out: True/False
        """
        return self.arm.release_feedback_callback(callback=callback)

