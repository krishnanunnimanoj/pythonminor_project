import os
from analyzer import PhysicsAnalyzer
from config_loader import ConfigLoader
from robot_loader import RobotLoader
from operating_envelope import OperatingEnvelopeAnalyzer
from result_view import ResultView

def get_urdf_path():

    while True:

        print("\nRobot configuration")

        urdf_path = input("URDF file path: ")

        if os.path.isfile(urdf_path):
            return urdf_path

        print(f"\nURDF file not found: {urdf_path}")
        print("Please enter a valid URDF file path.")

def get_user_inputs():

    print("\n========================================")
    print("   ROBOT OPERATING ENVELOPE ANALYZER")
    print("========================================")

   

    print("\nEnter payload range")

    min_payload = float(input("Minimum payload (kg): "))
    max_payload = float(input("Maximum payload (kg): "))
    payload_step = float(input("Payload step (kg): "))

    print("\nEnter speed range")

    min_speed = float(input("Minimum speed (m/s): "))
    max_speed = float(input("Maximum speed (m/s): "))
    speed_step = float(input("Speed step (m/s): "))

    print("\nEnter environment")

    slope_angle = float(input("Slope angle (degrees): "))

   
    return (min_payload,max_payload,payload_step,min_speed,max_speed,speed_step,slope_angle)

config_loader = ConfigLoader("configs/robot.yaml")

try:
    config = config_loader.load()

except (FileNotFoundError, ValueError) as error:
    print(f"\n{error}")
    exit()
urdf_path = get_urdf_path()

robot_loader = RobotLoader(urdf_path, config)

try:
    robot = robot_loader.load()

except (FileNotFoundError, ValueError) as error:
    print(f"\n{error}")
    exit()

print(f"\nRobot mass: {robot.robot_mass:.2f} kg")
print(f"Wheel radius: {robot.wheel_radius:.2f} m")
print(f"Wheel count: {robot.number_of_motors}")

analyzer = PhysicsAnalyzer(robot)

(min_payload,max_payload,payload_step,min_speed,max_speed,speed_step,slope_angle) = get_user_inputs()


def generate_range(min_value, max_value, step):

    values = []

    current_value = min_value

    while current_value <= max_value:

        values.append(round(current_value, 2))

        current_value += step

    return values



payloads = generate_range(min_payload,max_payload,payload_step)

speeds = generate_range(min_speed,max_speed,speed_step)

envelope_analyzer = OperatingEnvelopeAnalyzer(analyzer)

envelope_results = envelope_analyzer.calculate(payloads,speeds,slope_angle)

analytical_payload_by_speed = (
    envelope_results["analytical_payload_by_speed"]
)

analytical_cruise_payload_by_speed = (
    envelope_results["analytical_cruise_payload_by_speed"]
)

safe_payload_by_speed = (
    envelope_results["safe_payload_by_speed"]
)

tested_boundary_by_speed = (
    envelope_results["tested_boundary_by_speed"]
)

limiting_constraint_by_speed = (
    envelope_results["limiting_constraint_by_speed"]
)

operating_envelope_matrix = (
    envelope_results["operating_envelope_matrix"]
)

result_view = ResultView()

result_view.print_results(
    analytical_payload_by_speed,
    analytical_cruise_payload_by_speed,
    safe_payload_by_speed,
    limiting_constraint_by_speed,
    speeds,
    min_payload
)

result_view.plot_results(
    analytical_payload_by_speed,
    tested_boundary_by_speed,
    speeds
)
