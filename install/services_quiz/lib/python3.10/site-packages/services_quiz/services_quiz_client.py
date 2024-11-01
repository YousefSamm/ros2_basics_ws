import rclpy
from rclpy.node import Node
from services_quiz_srv.srv import Turn

class Client(Node):
    def __init__(self):
        super().__init__('client')
        self.client = self.create_client(Turn, 'turn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = Turn.Request()

    def send_request(self):
        # Set all request parameters before calling async
        self.req.direction = "Right"
        self.req.angular_velocity = 0.2
        self.req.time = 10

        # Send the request and store the future
        self.future = self.client.call_async(self.req)
        self.get_logger().info("Request sent to server")

def main(args=None):
    rclpy.init(args=args)
    node = Client()
    node.send_request()
    
    # Spin to process events and wait for the future to complete
    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                response = node.future.result()
                if response.success:
                    node.get_logger().info("Turn executed successfully")
                else:
                    node.get_logger().info("Turn execution failed")
            except Exception as e:
                node.get_logger().error(f'Service call failed: {e}')
            break  # Exit the loop after the response is received

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
