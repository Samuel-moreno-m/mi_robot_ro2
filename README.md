# mi_robot

Robot diferencial en ROS 2 (Kilted) descrito con URDF/Xacro, visualizable en
RViz y simulable en Gazebo. Proyecto del curso RO2.

## Contenido

- `urdf/mi_robot.urdf.xacro`: robot completo (geometria, colisiones, inercias)
- `urdf/sensors.xacro`: IMU, Lidar y Camara
- `urdf/mi_robot.urdf`: URDF final generado con xacro
- `launch/display_launch.py`: abre el robot en RViz
- `launch/gazebo_launch.py`: abre Gazebo con un mundo vacio y crea el robot
- `rviz/urdf_config.rviz`: configuracion de RViz

## El robot

- Chasis: caja de 0.4 x 0.3 x 0.1 m, 5 kg
- Dos ruedas motrices: cilindros de radio 0.1 m y ancho 0.05 m, 0.5 kg cada una
- Rueda loca (caster): esfera de radio 0.05 m, 0.2 kg
- Sensores: IMU, Lidar y Camara, con geometria, colision e inercia (sin
  plugins de Gazebo: por ahora no publican datos)

Arbol de TF:

    base_footprint
    +-- base_link
        +-- left_wheel
        +-- right_wheel
        +-- caster_wheel
        +-- imu_link
        +-- lidar_link
        +-- camera_link

## Dependencias

    sudo apt install ros-$ROS_DISTRO-ros-gz ros-$ROS_DISTRO-xacro \
      ros-$ROS_DISTRO-robot-state-publisher \
      ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-rviz2

## Compilar

    cd ~/ros2_ws
    colcon build --packages-select mi_robot
    source install/setup.bash

## Uso

RViz:

    ros2 launch mi_robot display_launch.py

Gazebo:

    ros2 launch mi_robot gazebo_launch.py

Despues de editar un archivo xacro hay que volver a compilar.
