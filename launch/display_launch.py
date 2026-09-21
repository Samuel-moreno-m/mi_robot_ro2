import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('mi_robot')
    xacro_file = os.path.join(pkg_share, 'urdf', 'mi_robot.urdf.xacro')
    rviz_config = os.path.join(pkg_share, 'rviz', 'urdf_config.rviz')

    # Convierte el xacro a URDF cada vez que se lanza
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str
    )

    # Si ya existe la configuracion de RViz la usa; si no, abre RViz vacio
    rviz_args = ['-d', rviz_config] if os.path.exists(rviz_config) else []

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=rviz_args,
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        rviz,
    ])
