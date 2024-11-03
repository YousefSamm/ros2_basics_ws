import rclpy
from rclpy.node import Node
from custom_interfaces.srv import MyCustomServiceMessage
import sys
class CLientAsync(Node):
    def __init__(self):
        super().__init__('movement_client')
        self.client=self.create_client(MyCustomServiceMessage, 'movement')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service is not available, waiting again...')
        self.req=MyCustomServiceMessage.Request()
    def send_request(self):
        self.req.move=sys.argv[1]
        self.future=self.client.call_async(self.req)
def main(args=Node):
    rclpy.init()
    client=CLientAsync()
    client.send_request()
    while rclpy.ok():
        rclpy.spin(client)
        if client.future.done():
            try:
                response=client.futire.result()
            except Exception as e:
                client.get_logger().info('Service call failed %r' % (e,))
        else:
            client.get_logger().info('Response State %r' % (response.success,))
        break
    client.destroy_node()
    rclpy.shutdown()
if __name__ =='__main__':
    main()