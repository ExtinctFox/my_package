import serial
import struct

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__("minimal_subscriber")
        self.subscription = self.create_subscription(
            Joy,
            "joy",
            self.listener_callback,
            10)
        self.subscription
        self.s = serial.Serial("/dev/ttyUSB0", 115200, timeout = 10)

    def listener_callback(self, msg):
        buff = struct.pack("=BBff", 40, 60, msg.axes[1], msg.axes[3])
        self.s.write(buff)

        receved = self.s.read(20)
        index = receved.find(b"\x3C\x3C")
        sorted = receved[2:10]
        unpacked = struct.unpack(")ff", sorted)

    def main(args=None):
        rclpy.init(args=args)

        minimal_subscriber = MinimalSubscriber()

        rclpy.spin(minimal_subscriber)

        minimal_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()