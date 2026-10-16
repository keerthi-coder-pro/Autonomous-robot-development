import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    description_share = get_package_share_directory("virtual_robot_description")
    bringup_share = get_package_share_directory("virtual_robot_bringup")
    avoidance_share = get_package_share_directory("obstacle_avoidance")

    use_sim_time = LaunchConfiguration("use_sim_time")
    world = LaunchConfiguration("world")
    x_pose = LaunchConfiguration("x_pose")
    y_pose = LaunchConfiguration("y_pose")
    yaw = LaunchConfiguration("yaw")

    robot_description = ParameterValue(
        Command(["xacro ", os.path.join(description_share, "urdf", "robot.urdf.xacro")]),
        value_type=str,
    )

    # Stale gzserver causes exit 255 (address already in use) if only gzclient was closed.
    stop_old_gazebo = ExecuteProcess(
        cmd=[
            "bash",
            "-c",
            "pkill -9 gzclient 2>/dev/null; pkill -9 gzserver 2>/dev/null; "
            "killall -9 gzclient gzserver 2>/dev/null; sleep 3; true",
        ],
        output="screen",
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")
        ),
        launch_arguments={
            "world": world,
            "verbose": "false",
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time, "robot_description": robot_description}],
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity",
            "virtual_robot",
            "-topic",
            "robot_description",
            "-x",
            x_pose,
            "-y",
            y_pose,
            "-Y",
            yaw,
        ],
    )

    detector = Node(
        package="obstacle_avoidance",
        executable="obstacle_detector",
        output="screen",
        parameters=[os.path.join(avoidance_share, "config", "avoidance.yaml")],
    )

    avoider = Node(
        package="obstacle_avoidance",
        executable="obstacle_avoider",
        output="screen",
        parameters=[os.path.join(avoidance_share, "config", "avoidance.yaml")],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            DeclareLaunchArgument(
                "world",
                default_value=os.path.join(description_share, "worlds", "obstacles.world"),
            ),
            DeclareLaunchArgument("x_pose", default_value="-3.2"),
            DeclareLaunchArgument("y_pose", default_value="-3.2"),
            DeclareLaunchArgument("yaw", default_value="0.785"),
            stop_old_gazebo,
            TimerAction(period=4.0, actions=[gazebo]),
            robot_state_publisher,
            TimerAction(period=3.0, actions=[spawn_robot]),
            TimerAction(period=5.0, actions=[detector, avoider]),
        ]
    )
