# robotour
Main package for robotour competiton.

- [Overview](#overview)
- [How to use](#how-to-use)
- [Files](#files)
    - [Launch files](#launch-files)
    - [Scripts](#scripts)
- [License](#license)

## Overview
This ROS package contains all the necessary files for launching the robotour competition.

It contains several launch files and scripts.

## How to use
The main launch file is `robotour.launch` which launches all the necessary nodes for the competition.

There are numerous dependencies that need to be installed before running the competition. We recommend using the singularity image available [here](https://github.com/vras-robotour/deploy). It comes with all the necessary dependencies preinstalled. It also creates a workspace with all additional packages needed for the competition.

If you want to use the `map_data` package to publish the point cloud of the map, you need to create a `.mapdata` file of the area. Information on how to create the file can be found on the `map_data` package [website](https://github.com/vras-robotour/map_data).

To start the competition, run the following command:
```bash
roslaunch robotour robotour.launch
```

If you want to start the competition and visualize the command center in RViz, run the following command:
```bash
roslaunch robotour robotour.launch rviz:=true
```

More information about the launch files and started nodes can be found in the [Files](#files) section or in their respective packages.

## Files
The package contains two main file types launch files and scripts.

### Launch files
Here we provide a list of all the launch files in the package. They are listed in alphabetical order. It the launch file takes any arguments, they are also listed, and example usage is provided.

- fake_gps.launch
    - Provides fake GPS data for testing purposes.
    - Data is read from a file in `data` directory and file name is passed as an argument `file`.
    - Usage: `roslaunch robotour fake_gps.launch file:=<file_name>`
- follower.launch
    - Launches the follower node from naex package.
- geometric_traversability.launch
    - Launches nodes for calculating and publishing geometric traversability.
    - It has two arguments `nodelet_manager` and `nodelet_action`, we recommend not to change them.
- goal_parser.launch
    - Starts the goal parser node.
    - Depending on the argument `test`, it will either start the node in test mode or normal mode.
    - Normal mode is used during the competition it takes goal from detected QR codes. Test mode takes the goal from position clicked in RViz.
    - Usage: `roslaunch robotour goal_parser.launch test:=<true/false>`
- local_utm.launch
    - Launches the local_utm node.
    - It has two arguments `test` and `case`.
    - Argument `test` is used to switch between test and normal mode. Test mode is used for testing pusposes and publishes a static transformation.
    - Argument `case` is used to select the case for the test mode. If you want to add a new case, you need to modify the launch file.
    - Usage: `roslaunch robotour loca_utm.launch test:=<true/false> case:=<case_name>`
- planner.launch
    - Launches the planner node from naex package.
- point_cloud_color.launch
    - Launches the point cloud color node.
- robotour.launch
    - Main launch file for the competition.
    - It launches all the necessary nodes for the competition.
    - It has several arguments:
        - `robot` - specifies the robot used in the competition.
        - `localize` - sets whether the localization should be used.
        - `rviz` - sets whether the RViz should be launched.
        - `mapdata_path` - sets the path to the .mapdata file.
        - `mapdata_file` - sets the name of the .mapdata file.
        - `test` - sets whether the test mode should be used.
        - `test_case` - sets the case for the test mode.
    - We recommend not to change the `localize` and `mapdata_path` argument.
    - The `test` and `test_case` arguments are used for testing purposes and should not be used during the competition.
    - Usage: `roslaunch robotour robotour.launch robot:=<robot_name> rviz:=<true/false>  mapdata_file:=<file_name> test:=<true/false> test_case:=<case_name>`
- rviz.launch
    - Launches RViz with the necessary configuration for the competition.
    - It has one argument `robot` which specifies the robot used in the competition.
    - Usage: `roslaunch robotour rviz.launch robot:=<robot_name>`
- semantic_traversability.launch
    - Launches nodes for calculating and publishing semantic traversability.
- status_summary.launch
    - Launches the status summary node.
- transform_align.launch
    - Launches the transform align node.
- utm_odom.launch
    - Launches the utm odom node.

### Scripts
Each script file contains a ROS node that is started by the launch files. The nodes are listed in alphabetical order.

- goal_parser
- local_utm
- rviz_goal_parser
- status_summary
- transform_align
- utm_odom

## License

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/vras-robotour/robotour/blob/master/LICENSE)
