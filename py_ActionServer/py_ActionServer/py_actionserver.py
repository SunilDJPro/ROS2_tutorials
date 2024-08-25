import rclpy
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import String
from action_tutorials_interfaces.action import Fibonacci #This pkg and node required action-tutorial-py pkg !

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        
        # Create an action server and register the execute callback
        self.callback_group = ReentrantCallbackGroup()
        self._action_server = ActionServer(self, Fibonacci, 'fibonacci', 
            self.execute_callback, callback_group=self.callback_group)
        
    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        # Calculate the Fibonacci sequence
        feedback_msg = String()
        feedback_msg.data = 'Starting fibonacci sequence...'
        goal_handle.publish_feedback(feedback_msg)
        self.get_logger().info('Feedback: {0}'.format(feedback_msg.data))
        
        sequence = [0, 1]
        for i in range(2, goal_handle.request.order):
            sequence.append(sequence[i-1] + sequence[i-2])
            
        result = Fibonacci.Result()
        result.sequence = sequence
        
        self.get_logger().info('Returning result: {0}'.format(result.sequence))
        goal_handle.succeed()
        return result
    
def main():
    rclpy.init()
    fibonacci_action_server = FibonacciActionServer()
    
    executor = MultiThreadedExecutor()
    executor.add_node(fibonacci_action_server)
    executor.spin()
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
