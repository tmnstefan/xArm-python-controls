from xarm.wrapper import XArmAPI

class trajectory_recording():

    def __init__(self, arm:XArmAPI):
        self.arm = arm

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
    
    def delete_trajectory(self, name):
        """
        Delete trajectory
        
        :param name: trajectory name
        
        :return: code
            \ncode: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm._studio.delete_trajectory(name)