import rclpy
from rclpy.node import Node
from services_quiz_srv.srv import Turn
class Client(Node):
    def __init__(self):
        super().__init__('client')
        self.client=self.create_client(Turn, 'turn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again..')
        self.req=Turn.Request()
    def send_request(self):
        self.req.direction="Right"
        self.future=self.client.call_async(self.req)
        self.req.angular_velocity=0.2
        self.future=self.client.call_async(self.req)
        self.req.time=10
        self.future=self.client.call_async(self.req)
def main(args=None):
    rclpy.init(args=args)
    node=Client()
    node.send_request()
    while rclpy.ok():
        rclpy.spin(node)
        if node.future.done():
            try:
                response=node.future.result()
            except Exception as e:
                node.get_logger().info('Service call Failed %r' % (e,))
        else:
            node.get_logger().info('Response state %r' % (response.success,))
        break
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()