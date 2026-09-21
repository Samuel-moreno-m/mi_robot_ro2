import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('mi_robot')
    gz_share = get_package_share_directory('ros_gz_sim')
    xacro_file = os.path.join(pkg_share, 'urdf', 'mi_robot.urdf.xacro')

    # Convierte el xacro a URDF cada vez que se lanza
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str
    )

    # 1. Gazebo con un mundo vacio, simulacion corriendo (-r)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items(),
    )

    # 2. Publica el modelo y los TF del robot
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    # 3. Crea el robot en Gazebo. Espera 6 s a que Gazebo termine de abrir.
    spawn_robot = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-topic', 'robot_description',
                    '-name', 'mi_robot',
                    '-z', '0.02',
                ],
                output='screen',
            )
        ],
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_robot,
    ])
