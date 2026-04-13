# xArm-python-controls
Categorizes the functions from the xArm Python SDK

### Overview
Takes the arm controls from xArm's Python SDK and sorts them into categories of cartesian movement, gripper controls and utilities to allow for better ease of use

### Prerequisites
The xArm python SDK,  which can be installed through:
```
python3 -m pip install xarm-python-sdk
```
Note: the pip package currently contains an earlier version of the get_inverse_kinematics function which conflicts with this code, it is recommended to use the alternative methods

Alternative download methods can be found in xArm's SDK page: https://github.com/xArm-Developer/xArm-Python-SDK