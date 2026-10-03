import os

from analyzer import PhysicsAnalyzer
from config_loader import ConfigLoader
from robot_loader import RobotLoader
from operating_envelope import OperatingEnvelopeAnalyzer
from result_view import ResultView


class Application:

    def __init__(self):

        self.config = None
        self.robot = None
        self.analyzer = None
        self.envelope_analyzer = None

        self.result_view = ResultView()

    def load_configuration(self):

        config_loader = ConfigLoader(
            "configs/robot.yaml"
        )

        try:

            self.config = config_loader.load()

        except (FileNotFoundError, ValueError) as error:

            print(f"\n{error}")
            return False

        return True

    def load_robot(self, urdf_path):

        robot_loader = RobotLoader(
            urdf_path,
            self.config
        )

        try:

            self.robot = robot_loader.load()

        except (FileNotFoundError, ValueError) as error:

            print(f"\n{error}")
            return False

        print(
            f"\nRobot mass: "
            f"{self.robot.robot_mass:.2f} kg"
        )

        print(
            f"Wheel radius: "
            f"{self.robot.wheel_radius:.2f} m"
        )

        print(
            f"Wheel count: "
            f"{self.robot.number_of_motors}"
        )

        return True

    def create_analyzers(self):

        self.analyzer = PhysicsAnalyzer(
            self.robot
        )

        self.envelope_analyzer = (
            OperatingEnvelopeAnalyzer(
                self.analyzer
            )
        )
    def run_analysis(
        self,
        min_payload,
        max_payload,
        payload_step,
        min_speed,
        max_speed,
        speed_step,
        slope_angle
    ):

        payloads = self.generate_range(
            min_payload,
            max_payload,
            payload_step
        )

        speeds = self.generate_range(
            min_speed,
            max_speed,
            speed_step
        )

        results = self.envelope_analyzer.calculate(
            payloads,
            speeds,
            slope_angle
        )

        return payloads, speeds, results
    def generate_range(self, min_value, max_value, step):

        values = []

        current_value = min_value

        while current_value <= max_value:

            values.append(round(current_value, 2))

            current_value += step

        return values

    def get_user_inputs(self):

        print("\n========================================")
        print("   ROBOT OPERATING ENVELOPE ANALYZER")
        print("========================================")

        print("\nEnter payload range")

        min_payload = float(
            input("Minimum payload (kg): ")
        )

        max_payload = float(
            input("Maximum payload (kg): ")
        )

        payload_step = float(
            input("Payload step (kg): ")
        )

        print("\nEnter speed range")

        min_speed = float(
            input("Minimum speed (m/s): ")
        )

        max_speed = float(
            input("Maximum speed (m/s): ")
        )

        speed_step = float(
            input("Speed step (m/s): ")
        )

        print("\nEnter environment")

        slope_angle = float(
            input("Slope angle (degrees): ")
        )

        return (
            min_payload,
            max_payload,
            payload_step,
            min_speed,
            max_speed,
            speed_step,
            slope_angle
        )

    def get_urdf_path():

        while True:

            print("\nRobot configuration")

            urdf_path = input("URDF file path: ")

            if os.path.isfile(urdf_path):
                return urdf_path

            print(f"\nURDF file not found: {urdf_path}")
            print("Please enter a valid URDF file path.")

    def run(self):

        if not self.load_configuration():
            return

        urdf_path = self.get_urdf_path()

        if not self.load_robot(urdf_path):
            return

        self.create_analyzers()

        (
            min_payload,
            max_payload,
            payload_step,
            min_speed,
            max_speed,
            speed_step,
            slope_angle
        ) = self.get_user_inputs()

        (
            payloads,
            speeds,
            envelope_results
        ) = self.run_analysis(
            min_payload,
            max_payload,
            payload_step,
            min_speed,
            max_speed,
            speed_step,
            slope_angle
        )

        self.result_view.print_results(
            envelope_results[
                "analytical_payload_by_speed"
            ],
            envelope_results[
                "analytical_cruise_payload_by_speed"
            ],
            envelope_results[
                "safe_payload_by_speed"
            ],
            envelope_results[
                "limiting_constraint_by_speed"
            ],
            speeds,
            min_payload
        )

        self.result_view.plot_results(
            envelope_results[
                "analytical_payload_by_speed"
            ],
            envelope_results[
                "tested_boundary_by_speed"
            ],
            speeds
        )