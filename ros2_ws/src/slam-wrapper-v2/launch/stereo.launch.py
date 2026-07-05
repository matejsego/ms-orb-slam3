from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    package_dir = get_package_share_directory("ros2_orb_slam3")

    stereo_node = Node(
        package='ros2_orb_slam3',
        executable='stereo_node_cpp',
        name='stereo_node',
        namespace='ORB_SLAM3',
        output='screen',
        parameters=[
            {'settings_file': package_dir + '/orb_slam3/config/Stereo/nicla_stereo.yaml'},
            {'voc_file': package_dir + '/orb_slam3/Vocabulary/ORBvoc.txt.bin'},
            {'img0_topic': '/nicla2/camera/image_raw'}, # lijeva kamera
            {'img1_topic': '/nicla1/camera/image_raw'}, # desna kamera
            {'enable_debug_window': True},
            {'is_inertial': False},  # čisti stereo bez IMU-a
        ]
    )

    return LaunchDescription([stereo_node])
