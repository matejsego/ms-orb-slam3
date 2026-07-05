#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class NiclaCompressedToRaw(Node):
    def __init__(self):
        super().__init__('nicla_compressed_to_raw')
        self.bridge = CvBridge()
        self.pub = self.create_publisher(Image, '/nicla/camera/image_raw', 10)
        self.sub = self.create_subscription(
            CompressedImage,
            '/nicla/camera/image_raw/compressed',
            self.cb,
            10
        )

    def cb(self, msg: CompressedImage):
        arr = np.frombuffer(msg.data, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            self.get_logger().warn('Failed to decode compressed image')
            return

        out = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        out.header = msg.header
        self.pub.publish(out)

def main():
    rclpy.init()
    node = NiclaCompressedToRaw()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
