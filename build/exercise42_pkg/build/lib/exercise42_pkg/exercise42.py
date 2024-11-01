import rclpy 
from rclpy.node import Node
from std_srvs.srv import SetBool
from geometry_msgs.msg import Twist
class ExerciseNode(Node):
    def __init__(self):
        super().__init__('Exercise42')
        self.publisher_=self.create_publisher(Twist, '/cmd_vel', 10)
        self.service_=self.create_service(SetBool,'exercise42', self.srv_callback)
    def srv_callback(self, request, response):
        msg=Twist()
        if request.data==True:
            msg.linear.x=0.3
            msg.angular.z=-0.3
            self.publisher_.publish(msg)
            response.success=True
            response.message='MOVING THE ROBOT! :)'
        else:
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.publisher_.publish(msg)
            response.success=False
            response.message='It is time to stop:('
        return response
def main(args=None):
    rclpy.init(args=args)
    service=ExerciseNode()
    rclpy.spin(service)
    service.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()
