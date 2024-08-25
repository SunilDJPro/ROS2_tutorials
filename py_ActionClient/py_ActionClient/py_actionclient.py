import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        
        # Create an action client and wait for the server to become available
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')
        while not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for action server...')
            
    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        # Send the goal and wait for the result
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self, self._send_goal_future)
        
        # Get the result and print it
        goal_handle = self._send_goal_future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        get_result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, get_result_future)
        
        result = get_result_future.result().result
        self.get_logger().info('Result: {0}'.format(result.sequence))
    
    def feedback_callback(self, feedback):
        self.get_logger().info('Feedback: {0}'.format(feedback.feedback.data))
        
def main():
    rclpy.init()
    fibonacci_action_client = FibonacciActionClient()
    
    executor = MultiThreadedExecutor()
    executor.add_node(fibonacci_action_client)
    executor.spin()
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
