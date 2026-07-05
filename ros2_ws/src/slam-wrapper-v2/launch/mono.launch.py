from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    package_dir = get_package_share_directory("ros2_orb_slam3")
    
    mono_inertial_node = Node(
        package='ros2_orb_slam3',
        executable='mono_node_cpp',
        name='mono_inertial_node',
        namespace='ORB_SLAM3',
        output='screen',
        parameters=[
            {'settings_file': package_dir + '/orb_slam3/config/Monocular-Inertial/parameters.yaml'},
            {'voc_file': package_dir + '/orb_slam3/Vocabulary/ORBvoc.txt.bin'},
            {'img_topic': '/nicla1/camera/image_raw'},
            {'imu_topic': '/nicla1/imu'},
            {'enable_debug_window': True},
            {'is_inertial': False}, # čisti mono bez IMU-a
            {'manual_time_sync': False},
            {'camera_frame_id': 'nicla_camera'},
            {'imu_frame_id': 'nicla_imu'},
        ]
    )
    
    # Transformacija između kamere i IMU-a (ne koristimo jer je 'is_inertial': False)
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_to_imu_tf_publisher',
        output='screen',
        arguments=[
            '--x', '0.012', '--y', '0.005', '--z', '-0.006',
            '--qx', '-0.7071068', '--qy', '0', '--qz', '0.7071068', '--qw', '0.0',
            '--frame-id', 'nicla_camera',
            '--child-frame-id', 'nicla_imu'
        ]
    )
    
    return LaunchDescription([static_tf_node, mono_inertial_node])
