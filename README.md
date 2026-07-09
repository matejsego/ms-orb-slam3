# Localization of the AgileX Scout Mini Mobile Robot Using Monocular and Stereo SLAM

Implementation of monocular and stereo visual SLAM (ORB-SLAM3) on the AgileX Scout Mini mobile robot, using two Arduino Nicla Vision cameras connected via Wi-Fi/UDP in a ROS2 Jazzy environment. The system compares the monocular configuration (scale ambiguity) with the stereo configuration (metrically accurate scale derived from a known camera baseline).

**Environment:** Ubuntu 24.04, ROS2 Jazzy

A full list of dependencies is available in the `dependencies/` folder.

## 1. Camera Setup

Firmware updated following the [Nicla Vision tutorial](https://docs.arduino.cc/tutorials/nicla-vision/getting-started/) via the Arduino IDE. Camera functionality tested in [OpenMV IDE](https://openmv.io/pages/download) using the [`red_detect.py`](OpenMVIDE/red_detect.py) script.

Streaming configuration (IP, network credentials, protocol, resolution) is set in `config.h`, located at `nicla_vision_drivers/arduino/main/`. To get the local IPv4 address of the host machine:

```bash
python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()"
```

The configuration in `nicla_vision_drivers/arduino/main/` must be flashed individually to each Nicla Vision camera via the Arduino IDE. Each camera requires a **unique port** (defined in `main.ino`, lines 80–81) so that both cameras can stream independently to the host — e.g. `8002`/`9001` for the first camera (`nicla1`) and `8003`/`9002` for the second (`nicla2`). All other configuration values are identical across both cameras.

## 2. Launching the Stream and ROS2 Bridge

Replace `<HOST_IP>` below with the host machine's local IPv4 address obtained in Step 1.

```bash
cd ~/ms-orb-slam3/ros2_ws
colcon build --packages-select nicla_vision_ros2 --symlink-install
source install/setup.bash

# terminal 1
ros2 launch nicla_vision_ros2 nicla_receiver.launch \
  receiver_ip:="<HOST_IP>" connection_type:="udp" \
  nicla_name:="nicla1" receiver_port:=8002

# terminal 2
ros2 launch nicla_vision_ros2 nicla_receiver.launch \
  receiver_ip:="<HOST_IP>" connection_type:="udp" \
  nicla_name:="nicla2" receiver_port:=8003

# terminal 3 and 4 — image decompression
python3 ~/ms-orb-slam3/auxiliary_scripts/nicla_compressed_to_raw.py --ros-args -p nicla_name:=nicla1
python3 ~/ms-orb-slam3/auxiliary_scripts/nicla_compressed_to_raw.py --ros-args -p nicla_name:=nicla2
```

## 3. Camera Calibration

```bash
# monocular calibration (per camera)
ros2 run camera_calibration cameracalibrator --size 4x6 --square 0.0375 \
  --no-service-check --ros-args --remap image:=/nicla1/camera/image_raw

# stereo calibration
ros2 run camera_calibration cameracalibrator --size 4x6 --square 0.0375 \
  --approximate 0.1 --no-service-check --ros-args \
  --remap left:=/nicla2/camera/image_raw --remap right:=/nicla1/camera/image_raw
```

Calibration results and checkerboard templates: [`calib/checkboards/`](calib/checkboards).

## 4. Running ORB-SLAM3

```bash
cd ~/ms-orb-slam3/ros2_ws
MAKEFLAGS="-j2 --load-average=3.0" colcon build \
  --symlink-install --packages-select ros2_orb_slam3 \
  --executor sequential --parallel-workers 1 --cmake-args \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-O2"
source install/setup.bash

ros2 launch ros2_orb_slam3 mono.launch.py     # monocular SLAM

ros2 launch ros2_orb_slam3 stereo.launch.py   # stereo SLAM
```

## Acknowledgments

This project builds upon the following open-source repositories:
- [nicla_vision_drivers](https://github.com/ADVRHumanoids/nicla_vision_drivers) — firmware for camera streaming
- [nicla_vision_ros2](https://github.com/ADVRHumanoids/nicla_vision_ros2) — bridge to ROS2 topics
- [slam-wrapper-v2](https://github.com/BubbleRobotics/slam-wrapper-v2) (fork of [ros2_orb_slam3](https://github.com/Mechazo11/ros2_orb_slam3)) — ORB-SLAM3 ROS2 integration
