import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from services_quiz_srv.srv import Turn
import time
class Server(Node):
    def __init__(self):
        super().__init__('server')
        self.publisher_=self.create_publisher(Twist,'cmd_vel', 10)
        self.srvr=self.create_service(Turn, 'turn', self.srvr_callback)
    def srvr_callback(self, request,response):
        msg=Twist()
        if request.direction == "Right":
            msg.angular.z=-request.angular_velocity
            self.publisher_.publish(msg)
            response.success=True
            time.sleep(request.time)
            msg.angular.z=0.0
            self.publisher_.publish(msg)
        elif request.direction=="left":
            msg.angular.z=request.angular_velocity
            self.publisher_.publish(msg)
            response.success=True
            time.sleep(request.timer)
        else:
            response.success=False
        return response
def main(args=None):
    rclpy.init(args=args)
    node=Server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown
if __name__=='__main__':
    main()
    
