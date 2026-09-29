import matplotlib.pyplot as plt
def generate_range(min_value, max_value, step):

    values = []

    current_value = min_value

    while current_value <= max_value:

        values.append(round(current_value, 2))

        current_value += step

    return values




robot_mass = float(input("Enter robot mass: "))
min_payload = float(input('Enter minimum payload: '))
max_payload = float(input('Enter maximum payload: '))

payloads = generate_range(min_payload,max_payload,0.5)



print('Payload values: ')
print(payloads)

min_speed = float(input('Enter minimum speed: '))
max_speed = float(input('Enter maximum speed: '))

speeds = generate_range(min_speed, max_speed,1)

print('Speed values: ')
print(speeds)
#Robot Parameters#
wheel_radius = 0.1
motor_max_torque = 1.0
acceleration = 1.0

number_of_motors = 4
motor_torque_constant = 0.1
motor_max_current = 8.0

ambient_temperature = 25.0
temperature_rise_per_amp = 5.0
motor_max_temperature = 70.0

rolling_resistance_coefficient = 0.02
gravity = 9.81
air_density = 1.225
drag_coefficient = 1.0
frontal_area = 0.5
###
def calculate_max_safe_payload(speed):
        maximum_safe_torque = (motor_max_current * motor_torque_constant)

        maximum_safe_force_per_motor = (maximum_safe_torque / wheel_radius)

        maximum_safe_total_force = (maximum_safe_force_per_motor * number_of_motors)

        drag_force = (0.5 * air_density * drag_coefficient * frontal_area * speed ** 2)

        force_available_for_mass = (maximum_safe_total_force - drag_force)

        mass_factor = (acceleration + rolling_resistance_coefficient * gravity)

        maximum_safe_total_mass = (force_available_for_mass / mass_factor)

        maximum_safe_payload = (maximum_safe_total_mass - robot_mass)
        
        return maximum_safe_payload
# print("\nAnalytical Maximum Safe Payload by Speed:")

# for speed in speeds:

#     maximum_payload = calculate_max_safe_payload(speed)

#     if maximum_payload < 0:
#         print(speed, "m/s: Robot itself exceeds limit")
    
#     else:
#         print(speed, "m/s:", round(maximum_payload, 2), "kg")

analytical_payload_by_speed = {}

for speed in speeds:

    maximum_payload = calculate_max_safe_payload(speed)

    analytical_payload_by_speed[speed] = maximum_payload

print("\nAnalytical Payload Limits:")

for speed, payload in analytical_payload_by_speed.items():

    if payload < 0:
        print(speed, "m/s: Robot itself exceeds limit")
    else:
        print(speed, "m/s:", round(payload, 2), "kg")
        
print("\nRobot Speed Capability:")

for speed, payload in analytical_payload_by_speed.items():

    if payload < 0:
        print(speed, "m/s: Not achievable")

    elif payload < min_payload:
        print(speed, "m/s: Achievable only below tested payload range")

    else:
        print(speed, "m/s: Achievable within tested payload range")

    

scenarios = []

for payload in payloads:

    for speed in speeds:

        total_mass = robot_mass + payload

        rolling_force = (rolling_resistance_coefficient * total_mass * gravity)
        
        drag_force = (0.5 * air_density * drag_coefficient * frontal_area * speed ** 2)
        
        acceleration_force = total_mass * acceleration

        required_force = acceleration_force + rolling_force + drag_force
        
        force_per_motor = required_force / number_of_motors

        motor_torque = round(force_per_motor * wheel_radius, 2)

        motor_current = round(motor_torque / motor_torque_constant,2)
        motor_temperature = round(ambient_temperature + motor_current * temperature_rise_per_amp,2)
        
        if motor_torque <= motor_max_torque:
            motor_status = "OK"
        else:
            motor_status = "EXCEEDED"

        if motor_current <= motor_max_current:
            current_status = "OK"
        else:
            current_status = "EXCEEDED"

        if motor_temperature <= motor_max_temperature:
            temperature_status = "OK"
        else:
            temperature_status = "EXCEEDED"

        if (motor_status == "EXCEEDED"
            or current_status == "EXCEEDED"
            or temperature_status == "EXCEEDED"):
            
            overall_status = "EXCEEDED"
        else:
            overall_status = "OK"
        if motor_status == "EXCEEDED":
            limiting_constraint = "Motor Torque"

        elif current_status == "EXCEEDED":
            limiting_constraint = "Motor Current"

        elif temperature_status == "EXCEEDED":
            limiting_constraint = "Motor Temperature"

        else:
            limiting_constraint = "None"

        scenario = {
            "payload":payload,
            "speed":speed,
            "total_mass": total_mass,
            "required_force": required_force,
            "motor_torque" : motor_torque,
            "motor_status": motor_status,
            "motor_current":motor_current,
            "current_status":current_status,
            "motor_temperature": motor_temperature,
            "temperature_status": temperature_status,
            "overall_status": overall_status,
            "limiting_constraint": limiting_constraint
        }

        scenarios.append(scenario)

print("\nScenarios:")

#for scenario in scenarios:
  #  print(scenario)

safe_payload_by_speed = {}

for speed in speeds:

    safe_payloads = []

    for scenario in scenarios:

        if scenario["speed"] == speed and scenario["overall_status"] == "OK":
            safe_payloads.append(scenario["payload"])

    safe_payload_by_speed[speed] = safe_payloads

print("\nSafe Payloads by Speed:")

for speed, safe_payloads in safe_payload_by_speed.items():
    print(speed, "m/s:", safe_payloads)

print("\nOperating Envelope Matrix:")

for speed in speeds:

    print(speed, "m/s:", end=" ")

    for payload in payloads:

        safe = False

        for scenario in scenarios:
            if (
                scenario["speed"] == speed
                and scenario["payload"] == payload
                and scenario["overall_status"] == "OK"
            ):
                safe = True
                break

        if safe:
            print("✓", end=" ")
        else:
            print("✗", end=" ")

    print()

# print("\nMaximum Safe Payload by Speed:")

# for speed, payloads in safe_payload_by_speed.items():

#     if payloads:
#         maximum_payload = max(payloads)
#         print(speed, "m/s:", maximum_payload, "kg")

#     else:
#         print(speed, "m/s: No safe payload in tested range")

# print("\nOperating Boundary by Speed:")

# for speed, payloads in safe_payload_by_speed.items():

#     if payloads:
#         maximum_safe = max(payloads)

#         print(
#             speed,
#             "m/s: Maximum tested safe payload =",
#             maximum_safe,
#             "kg"
#         )

#     else:
#         print(
#             speed,
#             "m/s: No safe payload in tested range"
#         )

# print("\nAnalytical vs Tested Boundary:")

# for speed in speeds:

#     analytical_limit = analytical_payload_by_speed[speed]
#     tested_payloads = safe_payload_by_speed[speed]

#     if analytical_limit < 0:
#         print(
#             speed,
#             "m/s: No operating point for robot"
#         )

#     elif tested_payloads:
#         tested_limit = max(tested_payloads)

#         print(
#             speed,
#             "m/s: Analytical =",
#             round(analytical_limit, 2),
#             "kg, Tested =",
#             tested_limit,
#             "kg"
#         )

#     else:
#         print(
#             speed,
#             "m/s: Analytical =",
#             round(analytical_limit, 2),
#             "kg, Tested = No safe payload"
#         )

print("\nLimiting Constraint by Speed:")

for speed in speeds:

    speed_scenarios = []

    for scenario in scenarios:
        if scenario["speed"] == speed:
            speed_scenarios.append(scenario)

    unsafe_speed_scenarios = []

    for scenario in speed_scenarios:
        if scenario["overall_status"] == "EXCEEDED":
            unsafe_speed_scenarios.append(scenario)

    if unsafe_speed_scenarios:

        first_unsafe = min(
            unsafe_speed_scenarios,
            key=lambda scenario: scenario["payload"]
        )

        print(
            speed,
            "m/s: Payload =",
            first_unsafe["payload"],
            "kg, Constraint =",
            first_unsafe["limiting_constraint"]
        )

    else:
        print(
            speed,
            "m/s: No unsafe scenario in tested range"
        )

print("\nFinal Operating Envelope:")

for speed in speeds:

    analytical_limit = analytical_payload_by_speed[speed]

    if analytical_limit < 0:

        print(
            speed,
            "m/s: No operating point"
        )

    elif analytical_limit < min_payload:

        print(
            speed,
            "m/s: Safe only below tested payload range"
        )

    else:

        print(
            speed,
            "m/s: Safe up to",
            round(analytical_limit, 2),
            "kg payload"
        )

tested_boundary_by_speed = {}

for speed in speeds:

    safe_payloads = safe_payload_by_speed[speed]

    if safe_payloads:
        tested_boundary_by_speed[speed] = max(safe_payloads)
    else:
        tested_boundary_by_speed[speed] = None

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

# safe_scenarios = []

# for scenario in scenarios:

#     if scenario["overall_status"] == "OK":
#         safe_scenarios.append(scenario)

# print("\nSafe Operating Scenarios:")

# if safe_scenarios:

#     max_safe_payload = max(
#         scenario["payload"]
#         for scenario in safe_scenarios
#     )

#     print(
#         "Maximum Safe Payload:",
#         max_safe_payload,
#         "kg"
#     )

# else:

#     print("No safe operating scenarios found.")




# unsafe_scenarios = []

# for scenario in scenarios:
#     if scenario["overall_status"] == "EXCEEDED":
#         unsafe_scenarios.append(scenario)

# print("\nUnsafe Operating Scenarios:")

# #for scenario in unsafe_scenarios:
# #    print(scenario)

# min_unsafe_payload = min(
#     scenario["payload"]
#     for scenario in unsafe_scenarios
# )

# print("\nMinimum Unsafe Payload:",min_unsafe_payload,"kg")

# boundary_scenarios = []

# for scenario in unsafe_scenarios:
#     if scenario["payload"] == min_unsafe_payload:
#         boundary_scenarios.append(scenario)

# boundary_constraint = boundary_scenarios[0]["limiting_constraint"]

# print("\nBoundary Constraint:", boundary_constraint)

# print("\nBoundary Scenarios:")

#for scenario in boundary_scenarios:
 #   print(scenario)


# maximum_safe_current = motor_max_current

# maximum_safe_torque = maximum_safe_current * motor_torque_constant

# print("\nMaximum Safe Motor Current:", maximum_safe_current, "A")
# print("Maximum Safe Motor Torque:", maximum_safe_torque,"Nm")

# maximum_safe_force_per_motor = maximum_safe_torque / wheel_radius

# print(
#     "Maximum Safe Force per Motor:",
#     maximum_safe_force_per_motor,
#     "N"
# )

# maximum_safe_total_force = maximum_safe_force_per_motor * number_of_motors

# print(
#     "Maximum Safe Total Force:",
#     maximum_safe_total_force,
#     "N"
# )

# maximum_safe_total_mass = maximum_safe_total_force / acceleration

# print(
#     "Maximum Safe Total Mass:",
#     maximum_safe_total_mass,
#     "kg"
# )
# maximum_safe_payload = maximum_safe_total_mass - robot_mass

# print(
#     "Maximum Safe Payload:",
#     maximum_safe_payload,
#     "kg"
# )

# boundary_total_mass = robot_mass + maximum_safe_payload

# boundary_force = boundary_total_mass * acceleration

# boundary_force_per_motor = boundary_force / number_of_motors

# boundary_torque = boundary_force_per_motor * wheel_radius

# boundary_current = boundary_torque / motor_torque_constant

# print("\nCalculated Boundary Check:")
# print("Total Mass:", boundary_total_mass, "kg")
# print("Motor Torque:", boundary_torque, "Nm")
# print("Motor Current:", boundary_current, "A")
# print("Acceleration Force:", acceleration_force, "N")
# print("Rolling Force:", rolling_force, "N")
# print("Required Force:", required_force, "N")
# print("Speed:", speed, "m/s")
# print("Drag Force:", drag_force, "N")