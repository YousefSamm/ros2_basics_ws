import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 
from rclpy.qos import ReliabilityPolicy, QoSProfile
class exercise31(Node):
    def __init__(self):
        super().__init__('exercise31')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(LaserScan, '/scan', self.subscriber_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
    def subscriber_callback(self, msg):
        cmd=Twist()
        if (msg.ranges[359]>5):
            cmd.linear.x=1.0
            cmd.linear.y=0.0
            cmd.linear.z=0.0
            cmd.angular.x=0.0
            cmd.angular.y=0.0
            cmd.angular.z=1.0
        elif (msg.ranges[359]>0.5):
            cmd.linear.x=0.5
            cmd.linear.y=0.0
            cmd.linear.z=0.0
            cmd.angular.x=0.0
            cmd.angular.y=0.0
            cmd.angular.z=0.0
        elif (msg.ranges[359]<0.5):
            cmd.linear.x=0.0
            cmd.linear.y=0.0
            cmd.linear.z=0.0
            cmd.angular.x=0.0
            cmd.angular.y=0.0
            cmd.angular.z=0.0
        self.publisher_.publish(cmd)
def main(args=None):
    rclpy.init(args=args)
    node=exercise31()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__name__':
    main()