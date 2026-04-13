from xarm.wrapper import XArmAPI

class trajectory_recording():

    def __init__(self, arm:XArmAPI):
        self.arm = arm

    def get_record_seconds(self):
        """
        Get record seconds

        Note:
            1. Only available if firmware_version >= 2.4.0
            2. Only valid during recording or after recording but before saving

        Returns:
            out: tuple((code, seconds)), returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            seconds: The actual duration of the recorded trajectory
        """
        ret = self.arm.get_common_info(50, return_val=True)
        return ret
    
    def save_record_trajectory(self, filename, wait=True, timeout=5, **kwargs):
        """
        Save the trajectory you just recorded

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Args:
            filename: The name to save

                1. Only strings consisting of standard English characters or numbers are supported, with a maximum length of 50.

                2. The trajectory will be saved in the controller box.

                3. This action will overwrite a trajectory with the same name
                
                4. Empty the trajectory in memory after saving, so repeated calls will cause the recorded trajectory to be covered by an empty trajectory.

            wait: Whether to wait for saving, default is True

            timeout: Timeout waiting for saving to complete

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.save_record_trajectory(filename, wait=wait, timeout=timeout, **kwargs)
    
    def start_record_trajectory(self):
        """
        Start trajectory recording, only in teach mode, so joint teaching mode must already be set.

        Note:
            1. This interface relies on Firmware 1.2.0 or above
            2. set joint teaching mode: set_mode(2);set_state(0)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.start_record_trajectory()

    def stop_record_trajectory(self, filename=None, **kwargs):
        """
        Stop trajectory recording

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Args:
            filename: The name to save

                1. Only strings consisting of standard English characters or numbers are supported, with a maximum length of 50.

                2. The trajectory will be saved in the controller box.

                3. If the filename is None stop recording and do not save, you need to manually call `save_record_trajectory` save before changing the mode. otherwise the recording will be lost

                4. This action will overwrite a trajectory with the same name

                5. Empty the trajectory in memory after saving
    
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.stop_record_trajectory(filename=filename, **kwargs)
    
    def load_trajectory(self, filename, wait=True, timeout=None, **kwargs):
        """
        Load a trajectory

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Args:
            filename: The name of the trajectory to load

            wait: Whether to wait for loading, default is True

            timeout: Timeout waiting for loading to complete

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.load_trajectory(filename, wait=wait, timeout=timeout, **kwargs)
    
    def playback_trajectory(self, times=1, filename=None, wait=True, double_speed=1, **kwargs):
        """
        Playback trajectory

        Note:
            1. This interface relies on Firmware 1.2.0 or above

        Args:
            times: Number of playbacks,

                1. Only valid when the current position of the arm is the end position of the trajectory, otherwise it will only be played once.

            filename: The name of the trajectory to play back

                1. If filename is None, you will need to manually call `load_trajectory` to load the trajectory.

            wait: whether to wait for the arm to complete, default is False

            double_speed: double speed, only support 1/2/4, default is 1, only available if version > 1.2.11

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm.playback_trajectory(times=times, filename=filename, wait=wait, double_speed=double_speed, **kwargs)
    
    def get_trajectory_rw_status(self):
        """
        Get trajectory read/write status

        Returns: (code, status)
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            status:

                0: no read/write

                1: loading

                2: load success

                3: load failed

                4: saving

                5: save success

                6: save failed
        """
        return self.arm.get_trajectory_rw_status()
    
    def delete_trajectory(self, name):
        """
        Delete trajectory
        
        Args:
            name: trajectory name
        
        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.
        """
        return self.arm._studio.delete_trajectory(name)
    
    def get_traj_speeding(self, rate):
        """
        Obtain the joint and velocity values of joint overspeed during trajectory recording

        Args:
            rate: speed rate, only 1/2/4

        Returns:
            out: tuple((code, speed_info)), returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

            speed_info: [result_code, servo_id, servo_speed]

                result_code: 0: Pass, -1: Fail, >0: abnormal(1:Trajectory not loaded or incorrect status;2:The input magnification is incorrect)

                servo_id: Effective only when result_code is -1
                
                servo_speed: Effective only when result_code is -1
        """
        return self.arm.get_traj_speeding(self, rate)