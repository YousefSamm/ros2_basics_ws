import rclpy 
from rclpy.node import Node 
from geometry_msgs.msg import Twist
from actions_quiz_msg.action import Distance
from rclpy.action import ActionServer
import time
from rclpy.qos import ReliabilityPolicy, QoSProfile
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from std_msgs.msg import Float64

class MyActionServer(Node):
    def __init__(self):
        super().__init__('actionserver')
        self.call_back_group_1=MutuallyExclusiveCallbackGroup()
        self.call_back_group_2=MutuallyExclusiveCallbackGroup()
        self.feedback_publisher=self.create_publisher(Float64, '/total_distance', QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self._action_server=ActionServer(self, Distance,'distance_as', self.execute_callback, callback_group=self.call_back_group_1)
        self.subscription_=self.create_subscription(Twist, '/cmd_vel', self.twist_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE), callback_group=self.call_back_group_2)
        self.current_distance_in_twist = 0.0
        self.current_distance = 0.0
    def twist_callback(self, msg):
        self.current_distance_in_twist=msg.linear.x
    def execute_callback(self, goal_handle):
        self.get_logger().info('Measuring the Distance...')
        feedback_msg=Distance.Feedback()
        for i in range(0, goal_handle.request.seconds):
            feedback_msg.current_dist = self.current_distance
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.current_dist))
            goal_handle.publish_feedback(feedback_msg)
            float_feedback_msg = Float64()
            float_feedback_msg.data = self.current_distance
            self.feedback_publisher.publish(float_feedback_msg)
            self.current_distance += abs(self.current_distance_in_twist)
            time.sleep(1)
        self.total_measured_distance=self.current_distance 
        goal_handle.succeed()
        result=Distance.Result()
        result.total_dist=self.total_measured_distance
        result.status=True
        return result
def main(args=None):
    rclpy.init(args=args)
    action_server=MyActionServer()
    executor=MultiThreadedExecutor(num_threads=2)
    executor.add_node(action_server)
    try:
        executor.spin()
    finally:
        action_server.destroy_node()
        rclpy.shutdown()
if __name__=='__main__':
    main()