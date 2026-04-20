# xArm Python Controls

This is the documentation for the xArm Python Controls project, otherwise found on this [GitHub](https://github.com/tmnstefan/xArm-python-controls) page. As of time of writing the main function of the project is to categorize the functions that ufactory provides for their variety of robotic arms and provide a guide for less technical users on how to use the provided functions while being complete enough that technical users can find their own ways around interacting with the arm or writing their own functions.

Please note that this documentation and project are still ongoing and so there will likely be mistakes or incomplete function descriptions.

## Categorized xArm functions

These pages, when complete, will contain clear descriptions and explanations of all functions provided by ufactory based on how they have been categorized by the project, the categories are as follows:

- [Errors and error handling](error.md)
- [Gripper controls](gripper.md)
- [Cartesian(and other) movement](move_cartesian.md)
- [Reading from and writing to registers](read_write.md)
- [Callback functions](register_release.md)
- [Settings](settings.md)
- [Recording and playback of trajectories](trajectory_recording.md)
- [Utilities](util.md)


## Known issues

- Type annotations: there are currently no type annotations for the majority of functions, these will be added over time

- Vague Descriptions: many of the original function descriptions are too vague so until more testing has been done to determine the exact purpose of the function these will remain as they are

- Function description layout: as a result of how mkdocstrings parses python docstrings there are many descriptions for arguments and return values that have less than ideal formatting, this part is still a work in progress so expect to see some incorrect looking formatting