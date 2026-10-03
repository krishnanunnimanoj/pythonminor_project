import matplotlib.pyplot as plt
from analyzer import RobotParameters, PhysicsAnalyzer

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

    return (
        min_payload,
        max_payload,
        payload_step,
        min_speed,
        max_speed,
        speed_step,
        slope_angle
    )


robot = RobotParameters()
analyzer = PhysicsAnalyzer(robot)


def generate_range(min_value, max_value, step):

    values = []

    current_value = min_value

    while current_value <= max_value:

        values.append(round(current_value, 2))

        current_value += step

    return values

# min_payload = 2
# max_payload = 8

# payloads = generate_range(min_payload,max_payload,0.5)



# print('Payload values: ')
# print(payloads)

# min_speed = 2
# max_speed = 7

# speeds = generate_range(min_speed, max_speed,1)

# slope_angle = 10

# print('Speed values: ')
# print(speeds)
(min_payload,max_payload,payload_step,min_speed,max_speed,speed_step,slope_angle) = get_user_inputs()

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

# print("\nAnalytical Cruise Payload Limits:")

# for speed, payload in analytical_cruise_payload_by_speed.items():
#     if payload < 0:
#         print(speed, "m/s: Robot itself exceeds limit")
#     else:
#         print(speed, "m/s:", round(payload, 2), "kg")

# print("\nAnalytical Payload Limits:")

# for speed, payload in analytical_payload_by_speed.items():

#     if payload < 0:
#         print(speed, "m/s: Robot itself exceeds limit")
#     else:
#         print(speed, "m/s:", round(payload, 2), "kg")
        
# print("\nRobot Speed Capability:")

# for speed, payload in analytical_payload_by_speed.items():

#     if payload < 0:
#         print(speed, "m/s: Not achievable")

#     elif payload < min_payload:
#         print(speed, "m/s: Achievable only below tested payload range")

#     else:
#         print(speed, "m/s: Achievable within tested payload range")

    

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

# print("\nSafe Payloads by Speed:")

# for speed, safe_payloads in safe_payload_by_speed.items():
#     print(speed, "m/s:", safe_payloads)


# print("\nOperating Envelope Matrix:")

# for speed in speeds:

#     print(speed, "m/s:", end=" ")

#     row = operating_envelope_matrix[speed]

#     for safe in row:

#         if safe:
#             print("✓", end=" ")
#         else:
#             print("✗", end=" ")

#     print()


# print("\nLimiting Constraint by Speed:")

# for speed in speeds:

#     constraint = limiting_constraint_by_speed[speed]

#     if constraint is None:

#         print(speed,"m/s: No unsafe scenario in tested range")

#     else:

#         print(speed,"m/s: Payload =",constraint["payload"],"kg, Constraint =",constraint["constraint"])


# print("\nFinal Operating Envelope:")

# for speed in speeds:

#     analytical_limit = analytical_payload_by_speed[speed]

#     if analytical_limit < 0:

#         print(speed,"m/s: No operating point")

#     elif analytical_limit < min_payload:

#         print(speed,"m/s: Safe only below tested payload range")

#     else:

#         print(speed,"m/s: Safe up to",round(analytical_limit, 2),"kg payload")


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
