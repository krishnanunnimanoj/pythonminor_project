from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import os


def launch_setup(context, *args, **kwargs):

    project_path = os.path.expanduser(
        "~/python_project/robot_envelope_analyzer"
    )

    urdf_file = LaunchConfiguration("urdf_file").perform(context)

    urdf_path = os.path.join(
        project_path,
        "robots",
        urdf_file
    )

    gazebo_launch = os.path.join(
        "/opt/ros/humble/share/gazebo_ros/launch",
        "gazebo.launch.py"
    )

    with open(urdf_path, "r") as file:
        robot_description = file.read()

    return [

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                gazebo_launch
            )
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[
                {
                    "robot_description": robot_description
                }
            ]
        ),

        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=[
                "-topic",
                "robot_description",
                "-entity",
                "envelope_test_robot"
            ],
            output="screen"
        )

    ]


def generate_launch_description():

    return LaunchDescription([

        DeclareLaunchArgument(
            "urdf_file",
            default_value="my_robot.urdf",
            description="URDF file to use for the robot"
        ),

        OpaqueFunction(
            function=launch_setup
        )


    ])