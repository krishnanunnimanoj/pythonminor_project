import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class VelocityTest(Node):

    def __init__(self):
        super().__init__("velocity_test")

        self.target_speed = float(self.declare_parameter(
            "target_speed", 0.2
        ).value)
        self.test_duration = 5.0

        self.start_time = self.get_clock().now()

        self.publisher = self.create_publisher(
            Twist,
            "/diff_drive_controller/cmd_vel_unstamped",
            10
        )

        self.subscription = self.create_subscription(
            Odometry,
            "/diff_drive_controller/odom",
            self.odom_callback,
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.latest_velocity = 0.0
        self.target_reached = False
        self.reach_time = None
        self.test_finished = False

        self.get_logger().info(
            f"Starting velocity test: {self.target_speed} m/s"
        )

    def odom_callback(self, msg):
        self.latest_velocity = msg.twist.twist.linear.x

        if (
            not self.target_reached
            and abs(self.latest_velocity) >= 0.99 * self.target_speed
        ):
            self.target_reached = True

            self.reach_time = (
                self.get_clock().now() - self.start_time
            ).nanoseconds / 1e9

            self.get_logger().info(
                f"Target velocity reached after "
                f"{self.reach_time:.3f} s"
            )

    def control_loop(self):

        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        if elapsed < self.test_duration:

            cmd = Twist()

            cmd.linear.x = self.target_speed
            cmd.angular.z = 0.0

            self.publisher.publish(cmd)

            self.get_logger().info(
                f"Target: {self.target_speed:.2f} m/s | "
                f"Actual: {self.latest_velocity:.3f} m/s"
            )

        else:

            cmd = Twist()

            self.publisher.publish(cmd)

            self.get_logger().info(
                "Velocity test finished."
            )

            self.get_logger().info(
                f"Final measured velocity: "
                f"{self.latest_velocity:.3f} m/s"
            )
            self.test_finished = True
            self.destroy_timer(self.timer)


def main(args=None):

    rclpy.init(args=args)

    node = VelocityTest()

    try:

        while rclpy.ok() and not node.test_finished:
            rclpy.spin_once(
                node,
                timeout_sec=0.1
            )

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
