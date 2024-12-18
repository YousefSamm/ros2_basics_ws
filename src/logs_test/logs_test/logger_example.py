import rclpy
from rclpy.node import Node 

class LogDemo(Node):
    def __init__(self):
        super().__init__('logger_example')
        rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.INFO)
        # Logger level configuration - Uncomment 1 line to set a specific log level
        #rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.DEBUG)
        #rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.INFO)
        #rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.WARN)
        #rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.ERROR)
        #rclpy.logging.set_logger_level('logger_example', rclpy.logging.LoggingSeverity.FATAL)
        self.create_timer(0.2, self.timer_callback)
    def timer_callback(self):
        self.get_logger().debug("No shinobi nearby!")
        self.get_logger().info("Moe yo Byakugan! Kore ga watashi no nindō yo")
        self.get_logger().warn("Pain attacked the village!")
        self.get_logger().error("I have no more chakra!")
        self.get_logger().fatal("Don't die naruto-kun!")

def main(args=None):
    rclpy.init(args=args)
    log_demo=LogDemo()
    rclpy.spin(log_demo)
    rclpy.shutdown()
if __name__=='__main__':
    main()