import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.qos import ReliabilityPolicy, QoSProfile
from sensor_msgs.msg import LaserScan
import numpy as np
import time
class QuizNode(Node):
    def __init__(self):
        super().__init__('topics_quiz_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(
            Odometry, '/odom', self.subscriber_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.scan_subscriber=self.create_subscription(LaserScan,'/scan', self.scan_callback,
         QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.scanner=0
    def euler_from_quaternion(self, quaternion):
        """
        Converts quaternion (w in last place) to euler roll, pitch, yaw
        quaternion = [x, y, z, w]
        """
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)
        return roll, pitch, yaw

    def subscriber_callback(self, msg: Odometry):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        euler = self.euler_from_quaternion(orientation)
        cmd_msg = Twist()
        if(self.scanner<=4.0 and position.x<1.0 and euler[2]<0.1):
            cmd_msg.linear.x=0.9
        else:
                cmd_msg.linear.x=0.0
                cmd_msg.angular.z=0.5
                if(euler[2]>1.33): 
                    cmd_msg.angular.z=0.0
                    cmd_msg.linear.x=0.6
                    if(position.x>=0.8 and position.y>=0.8):
                        cmd_msg.linear.x=0.0
                        
        self.get_logger().info('the robots orientation is at %s' % str(euler[2]))
        self.publisher_.publish(cmd_msg)
    def scan_callback(self, msg: LaserScan):
        self.scanner=msg.ranges[90]
        self.get_logger().info('the wall is "%s" away' % str(msg.ranges[90]) )
        
def main(args=None):
    rclpy.init(args=args)
    node = QuizNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
