import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
class StopClient(Node):
    def __init__ (self):
        super().__init__('stop_client')
        self.stop_client=self.create_client(Empty, "stop")
        while not self.stop_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req=Empty.Request()
    def send_request(self):
        self.future= self.stop_client.call_async(self.req)
def main(args=None):
    rclpy.init(args=args)
    client=StopClient()
    client.send_request()
    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            try:
                response=client.future.result()
            except Exception as e:
                client.get_logger().info('Service call failed %r' % (e,))
        else:
            client.get_logger().info('the robot has stopped')
        break
    client.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()