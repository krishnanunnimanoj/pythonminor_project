from html import parser
import os
import matplotlib.pyplot as plt
from analyzer import RobotParameters, PhysicsAnalyzer
from urdf_parser import URDFParser

def load_robot(urdf_path):

    if not os.path.isfile(urdf_path):
        print(f"\nURDF file not found: {urdf_path}")
        return None

    try:
        parser = URDFParser(urdf_path)

        robot_data = parser.get_robot_parameters()

        robot = RobotParameters(
            robot_mass=robot_data["robot_mass"],
            wheel_radius=robot_data["wheel_radius"]
        )

        return robot

    except ValueError as error:
        print(f"\nURDF error: {error}")
        return None

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

urdf_path = get_urdf_path()

robot = load_robot(urdf_path)

if robot is None:
    exit()

print(f"\nRobot mass: {robot.robot_mass:.2f} kg")
print(f"Wheel radius: {robot.wheel_radius:.2f} m")

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

analytical_payload_by_speed = {}

for speed in speeds:

    maximum_payload = analyzer.calculate_max_safe_payload(speed,slope_angle)

    analytical_payload_by_speed[speed] = maximum_payload

analytical_cruise_payload_by_speed = {}

for speed in speeds:
    maximum_payload = analyzer.calculate_max_cruise_payload(speed,slope_angle)
    analytical_cruise_payload_by_speed[speed] = maximum_payload


scenarios = []

for payload in payloads:
    
    for speed in speeds:

        scenario = analyzer.analyze_scenario(payload, speed, slope_angle)

        scenarios.append(scenario)

results = analyzer.analyze_operating_envelope(scenarios,speeds)

safe_payload_by_speed = results["safe_payload_by_speed"]

tested_boundary_by_speed = results["tested_boundary_by_speed"]

limiting_constraint_by_speed = results["limiting_constraint_by_speed"]

operating_envelope_matrix = results["operating_envelope_matrix"]

print("\n========================================")
print("        OPERATING ENVELOPE RESULTS")
print("========================================")

print("\nAnalytical Payload Limits:")
print("----------------------------------------")

for speed, payload in analytical_payload_by_speed.items():

    if payload < 0:
        print(f"{speed:.1f} m/s: Not achievable")
    else:
        print(f"{speed:.1f} m/s: {payload:.2f} kg")


print("\nAnalytical Cruise Payload Limits:")
print("----------------------------------------")

for speed, payload in analytical_cruise_payload_by_speed.items():

    if payload < 0:
        print(f"{speed:.1f} m/s: Not achievable")
    else:
        print(f"{speed:.1f} m/s: {payload:.2f} kg")


print("\nRobot Speed Capability:")
print("----------------------------------------")

for speed, payload in analytical_payload_by_speed.items():

    if payload < 0:
        print(f"{speed:.1f} m/s: Not achievable")

    elif payload < min_payload:
        print(f"{speed:.1f} m/s: Achievable only below tested payload range")

    else:
        print(f"{speed:.1f} m/s: Achievable within tested payload range")


print("\nFinal Operating Envelope:")
print("----------------------------------------")

for speed in speeds:

    analytical_limit = analytical_payload_by_speed[speed]

    if analytical_limit < 0:
        print(f"{speed:.1f} m/s: No operating point")

    elif analytical_limit < min_payload:
        print(
            f"{speed:.1f} m/s: "
            "Safe only below tested payload range"
        )

    else:
        print(
            f"{speed:.1f} m/s: "
            f"Safe up to {analytical_limit:.2f} kg payload"
        )


print("\nLimiting Constraint:")
print("----------------------------------------")

for speed in speeds:

    constraint = limiting_constraint_by_speed[speed]

    if constraint is None:

        print(
            f"{speed:.1f} m/s: "
            "No unsafe scenario in tested range"
        )

    else:

        print(
            f"{speed:.1f} m/s: "
            f"{constraint['constraint']}"
        )


plt.figure(figsize=(8, 5))
analytical_limits = [
    analytical_payload_by_speed[speed]
    for speed in speeds
]

tested_limits = [
    tested_boundary_by_speed[speed]
    for speed in speeds
]

plt.plot(
    speeds,
     analytical_limits,
     marker="o",
     label="Analytical Limit"
 )

plt.plot(
     speeds,
     tested_limits,
     marker="x",
     label="Tested Limit"
 )

plt.xlabel("Speed (m/s)")
plt.ylabel("Maximum Safe Payload (kg)")
plt.title("Robot Operating Envelope")
plt.legend()
plt.grid(True)

plt.show()
