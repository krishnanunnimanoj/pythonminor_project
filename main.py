import matplotlib.pyplot as plt
import math
# import xml.etree.ElementTree as ET

# urdf_path = "robots/my_robot.urdf"

# with open(urdf_path, "r") as file:
#     urdf_content = file.read()

# print("\nURDF loaded successfully.")

# root = ET.fromstring(urdf_content)

# robot_mass = 0.0

# for link in root.findall("link"):
#     mass_element = link.find("inertial/mass")

#     if mass_element is not None:
#         robot_mass += float(mass_element.get("value"))

# print("Robot mass from URDF:", robot_mass, "kg")

def generate_range(min_value, max_value, step):

    values = []

    current_value = min_value

    while current_value <= max_value:

        values.append(round(current_value, 2))

        current_value += step

    return values







robot_mass = 10 #float(input("Enter robot mass: "))
min_payload = 2#float(input('Enter minimum payload: '))
max_payload = 8#float(input('Enter maximum payload: '))

payloads = generate_range(min_payload,max_payload,0.5)



print('Payload values: ')
print(payloads)

min_speed = 2#float(input('Enter minimum speed: '))
max_speed = 7#float(input('Enter maximum speed: '))

speeds = generate_range(min_speed, max_speed,1)

slope_angle = 10#float(input("Enter slope angle(degrees): "))

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
friction_coefficient = 0.7
gear_ratio = 2.0
drivetrain_efficiency = 0.9
motor_max_rpm = 3000
battery_voltage = 24.0
battery_max_current = 20.0
thermal_resistance = 2.0
thermal_capacitance = 100.0
motor_resistance = 0.2
analysis_time = 10.0
turning_radius = 2.0
###
def calculate_max_safe_payload(speed):
        maximum_safe_torque = (motor_max_current * motor_torque_constant)

        maximum_safe_force_per_motor = (maximum_safe_torque * gear_ratio * drivetrain_efficiency/ wheel_radius)

        maximum_safe_total_force = (maximum_safe_force_per_motor * number_of_motors)

        drag_force = (0.5 * air_density * drag_coefficient * frontal_area * speed ** 2)

        force_available_for_mass = (maximum_safe_total_force - drag_force)

        mass_factor = (acceleration + rolling_resistance_coefficient * gravity + gravity * math.sin(math.radians(slope_angle)))

        lateral_acceleration = (speed ** 2 / turning_radius)

        maximum_friction_acceleration = (friction_coefficient * gravity* math.cos(math.radians(slope_angle)))

        combined_mass_acceleration = math.sqrt(mass_factor ** 2 + lateral_acceleration ** 2)

        if combined_mass_acceleration >= maximum_friction_acceleration:
            return -1
        maximum_safe_total_mass = (force_available_for_mass / mass_factor)

        maximum_safe_payload = (maximum_safe_total_mass - robot_mass)

       
        return maximum_safe_payload

def calculate_max_cruise_payload(speed):

    maximum_safe_torque = (motor_max_current * motor_torque_constant)

    maximum_safe_force_per_motor = (maximum_safe_torque * gear_ratio * drivetrain_efficiency/ wheel_radius)

    maximum_safe_total_force = (maximum_safe_force_per_motor * number_of_motors)

    drag_force = (0.5 * air_density * drag_coefficient * frontal_area * speed ** 2)

    force_available_for_mass = (maximum_safe_total_force - drag_force)

    mass_factor = (rolling_resistance_coefficient * gravity + gravity * math.sin(math.radians(slope_angle)))

    lateral_acceleration = (speed ** 2 / turning_radius)

    maximum_friction_acceleration = (friction_coefficient * gravity * math.cos(math.radians(slope_angle)))

    combined_mass_acceleration = math.sqrt(mass_factor ** 2 + lateral_acceleration ** 2)

    if combined_mass_acceleration >= maximum_friction_acceleration:
        return -1
    maximum_safe_total_mass = (force_available_for_mass / mass_factor)

    maximum_safe_payload = (maximum_safe_total_mass - robot_mass)

    return maximum_safe_payload


analytical_payload_by_speed = {}

for speed in speeds:

    maximum_payload = calculate_max_safe_payload(speed)

    analytical_payload_by_speed[speed] = maximum_payload

analytical_cruise_payload_by_speed = {}

for speed in speeds:
    maximum_payload = calculate_max_cruise_payload(speed)
    analytical_cruise_payload_by_speed[speed] = maximum_payload

print("\nAnalytical Cruise Payload Limits:")

for speed, payload in analytical_cruise_payload_by_speed.items():
    if payload < 0:
        print(speed, "m/s: Robot itself exceeds limit")
    else:
        print(speed, "m/s:", round(payload, 2), "kg")

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

        slope_force = (total_mass * gravity * math.sin(math.radians(slope_angle)))
        normal_force = (total_mass * gravity * math.cos(math.radians(slope_angle)))
        normal_force_per_wheel = (normal_force / number_of_motors)
        maximum_traction_force_per_wheel = (friction_coefficient * normal_force_per_wheel)
        maximum_total_traction_force = (maximum_traction_force_per_wheel * number_of_motors)
      
      
        
        drag_force = (0.5 * air_density * drag_coefficient * frontal_area * speed ** 2)
        
        acceleration_force = total_mass * acceleration

        acceleration_required_force = (acceleration_force + rolling_force + drag_force + slope_force)

        lateral_force = (total_mass * speed ** 2 / turning_radius)

        combined_traction_force = (math.sqrt(acceleration_required_force ** 2 + lateral_force ** 2))

        cruise_required_force = (rolling_force + drag_force + slope_force)
        
        acceleration_force_per_motor = (acceleration_required_force / number_of_motors)

        cruise_force_per_motor = (cruise_required_force / number_of_motors)

        acceleration_wheel_torque = (acceleration_force_per_motor * wheel_radius)

        cruise_wheel_torque = (cruise_force_per_motor * wheel_radius)

        acceleration_motor_torque = (acceleration_wheel_torque / (gear_ratio * drivetrain_efficiency))

        cruise_motor_torque = (cruise_wheel_torque / (gear_ratio * drivetrain_efficiency))

        acceleration_motor_torque = round(acceleration_motor_torque, 2)

        cruise_motor_torque = round(cruise_motor_torque, 2)

        motor_current = round(acceleration_motor_torque / motor_torque_constant,2)

        heat_generated = ((motor_current ** 2) * motor_resistance * analysis_time)

        temperature_rise = (heat_generated / thermal_capacitance)

        dynamic_motor_temperature = (ambient_temperature + temperature_rise)

        motor_temperature = round(ambient_temperature + motor_current * temperature_rise_per_amp,2)

        cruise_motor_current = round(cruise_motor_torque / motor_torque_constant,2)

        cruise_motor_temperature = round(ambient_temperature + cruise_motor_current * temperature_rise_per_amp,2)

        wheel_rpm = (speed / (2 * math.pi * wheel_radius)) * 60

        motor_rpm = (wheel_rpm * gear_ratio)

        acceleration_mechanical_power = (acceleration_required_force * speed)

        cruise_mechanical_power = (cruise_required_force * speed)

        acceleration_electrical_power = (acceleration_mechanical_power / drivetrain_efficiency)

        cruise_electrical_power = (cruise_mechanical_power / drivetrain_efficiency)

        acceleration_battery_current = (acceleration_electrical_power/ battery_voltage)

        cruise_battery_current = (cruise_electrical_power/ battery_voltage)

        if dynamic_motor_temperature <= motor_max_temperature:
            dynamic_temperature_status = "OK"
        else:
            dynamic_temperature_status = "EXCEEDED"
        if combined_traction_force <= maximum_total_traction_force:
            traction_status = "OK"
        else:
            traction_status = "EXCEEDED"
        if (acceleration_motor_torque <= motor_max_torque and cruise_motor_torque <= motor_max_torque):
            motor_status = "OK"
        else:
            motor_status = "EXCEEDED"

        if (motor_current <= motor_max_current and cruise_motor_current <= motor_max_current):
            current_status = "OK"
        else:
            current_status = "EXCEEDED"
        if (motor_temperature <= motor_max_temperature and cruise_motor_temperature <= motor_max_temperature):
            temperature_status = "OK"
        else:
            temperature_status = "EXCEEDED"

        if motor_rpm <= motor_max_rpm:
            rpm_status = "OK"
        else:
            rpm_status = "EXCEEDED"

        if (acceleration_battery_current <= battery_max_current and cruise_battery_current <= battery_max_current):
            battery_status = "OK"
        else:
             battery_status = "EXCEEDED"

        if (motor_status == "EXCEEDED" or current_status == "EXCEEDED" or temperature_status == "EXCEEDED"or traction_status == "EXCEEDED" or rpm_status == "EXCEEDED" or battery_status == "EXCEEDED"):
    
            overall_status = "EXCEEDED"
        else:
            overall_status = "OK"
        if motor_status == "EXCEEDED":
            limiting_constraint = "Motor Torque"

        elif current_status == "EXCEEDED":
            limiting_constraint = "Motor Current"

        elif temperature_status == "EXCEEDED":
            limiting_constraint = "Motor Temperature"

        elif traction_status == "EXCEEDED":
            limiting_constraint = "Traction"

        elif rpm_status == "EXCEEDED":
            limiting_constraint = "Motor RPM"

        elif battery_status == "EXCEEDED":
            limiting_constraint = "Battery Current"

        else:
            limiting_constraint = "None"

        scenario = {
            "payload":payload,
            "speed":speed,

            "total_mass": total_mass,
            "required_force": acceleration_required_force,

            "acceleration_motor_torque": acceleration_motor_torque,
            "cruise_motor_torque": cruise_motor_torque,

            "acceleration_motor_current": motor_current,
            "cruise_motor_current": cruise_motor_current,

            "acceleration_motor_temperature": motor_temperature,
            "cruise_motor_temperature": cruise_motor_temperature,

            "motor_torque" : acceleration_motor_torque,
            "motor_status": motor_status,

            "motor_current":motor_current,
            "current_status":current_status,

            "motor_temperature": motor_temperature,
            "temperature_status": temperature_status,

            "heat_generated": round(heat_generated, 2),
            "dynamic_motor_temperature": round(dynamic_motor_temperature, 2),
            "dynamic_temperature_status": dynamic_temperature_status,

            "overall_status": overall_status,
            "limiting_constraint": limiting_constraint,

            "maximum_traction_force": maximum_total_traction_force,
            "traction_status": traction_status,

            "wheel_rpm": round(wheel_rpm, 2),
            "motor_rpm": round(motor_rpm, 2),
            "rpm_status": rpm_status,

            "acceleration_mechanical_power": round(acceleration_mechanical_power, 2),
            "cruise_mechanical_power": round(cruise_mechanical_power, 2),

            "acceleration_electrical_power": round(acceleration_electrical_power, 2),
            "cruise_electrical_power": round(cruise_electrical_power, 2),

            "acceleration_battery_current": round(acceleration_battery_current, 2),
            "cruise_battery_current": round(cruise_battery_current, 2),
            "battery_status": battery_status,
            "normal_force_per_wheel": round(normal_force_per_wheel, 2),

            "maximum_traction_force_per_wheel": round(maximum_traction_force_per_wheel, 2),

            "maximum_total_traction_force": round(maximum_total_traction_force, 2),

            "lateral_force": round(lateral_force, 2),

            "combined_traction_force": round(combined_traction_force, 2),
                    }
        
        scenarios.append(scenario)


print("\nScenarios:")



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
