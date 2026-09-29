def generate_range(min_value,max_value):
    number_of_points = 5

    step = (max_value - min_value) / (number_of_points - 1)

    values = []

    for i in range(number_of_points):
        value  = min_value + i * step
        values.append(value)
    return values




robot_mass = float(input("Enter robot mass: "))
min_payload = float(input('Enter minimum payload: '))
max_payload = float(input('Enter maximum payload: '))

payloads = generate_range(min_payload,max_payload)



print('Payload values: ')
print(payloads)

min_speed = float(input('Enter minimum speed: '))
max_speed = float(input('Enter maximum speed: '))

speeds = generate_range(min_speed, max_speed)

print('Speed values: ')
print(speeds)
wheel_radius = 0.1
motor_max_torque = 1.0
acceleration = 1.0

number_of_motors = 2
motor_torque_constant = 0.1
motor_max_current = 8.0

ambient_temperature = 25.0
temperature_rise_per_amp = 5.0
motor_max_temperature = 70.0

scenarios = []

for payload in payloads:

    for speed in speeds:

        total_mass = robot_mass + payload

        

        required_force = total_mass * acceleration
        
        force_per_motor = required_force / 2

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

for scenario in scenarios:
    print(scenario)

safe_scenarios = []

for scenario in scenarios:

    if scenario["overall_status"] == "OK":
        safe_scenarios.append(scenario)

print("\nSafe Operating Scenarios:")

for scenario in safe_scenarios:
    print(scenario)

max_safe_payload = max(
    scenario["payload"]
    for scenario in safe_scenarios
)

print("\nMaximum Safe Payload:", max_safe_payload, "kg")

unsafe_scenarios = []

for scenario in scenarios:
    if scenario["overall_status"] == "EXCEEDED":
        unsafe_scenarios.append(scenario)

print("\nUnsafe Operating Scenarios:")

for scenario in unsafe_scenarios:
    print(scenario)

min_unsafe_payload = min(
    scenario["payload"]
    for scenario in unsafe_scenarios
)

print("\nMinimum Unsafe Payload:",min_unsafe_payload,"kg")

boundary_scenarios = []

for scenario in unsafe_scenarios:
    if scenario["payload"] == min_unsafe_payload:
        boundary_scenarios.append(scenario)

boundary_constraint = boundary_scenarios[0]["limiting_constraint"]

print("\nBoundary Constraint:", boundary_constraint)

print("\nBoundary Scenarios:")

for scenario in boundary_scenarios:
    print(scenario)

maximum_safe_current = motor_max_current

maximum_safe_torque = maximum_safe_current * motor_torque_constant

print("\nMaximum Safe Motor Current:", maximum_safe_current, "A")
print("Maximum Safe Motor Torque:", maximum_safe_torque,"Nm")

maximum_safe_force_per_motor = maximum_safe_torque / wheel_radius

print(
    "Maximum Safe Force per Motor:",
    maximum_safe_force_per_motor,
    "N"
)

maximum_safe_total_force = maximum_safe_force_per_motor * number_of_motors

print(
    "Maximum Safe Total Force:",
    maximum_safe_total_force,
    "N"
)

maximum_safe_total_mass = maximum_safe_total_force / acceleration

print(
    "Maximum Safe Total Mass:",
    maximum_safe_total_mass,
    "kg"
)
maximum_safe_payload = maximum_safe_total_mass - robot_mass

print(
    "Maximum Safe Payload:",
    maximum_safe_payload,
    "kg"
)

boundary_total_mass = robot_mass + maximum_safe_payload

boundary_force = boundary_total_mass * acceleration

boundary_force_per_motor = boundary_force / number_of_motors

boundary_torque = boundary_force_per_motor * wheel_radius

boundary_current = boundary_torque / motor_torque_constant

print("\nCalculated Boundary Check:")
print("Total Mass:", boundary_total_mass, "kg")
print("Motor Torque:", boundary_torque, "Nm")
print("Motor Current:", boundary_current, "A")