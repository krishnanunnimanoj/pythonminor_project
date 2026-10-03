import math
class RobotParameters:
    def __init__(self):
        
        self.robot_mass = 10

        self.wheel_radius = 0.1
        self.motor_max_torque = 1.0
        self.acceleration = 1.0

        self.number_of_motors = 4
        self.motor_torque_constant = 0.1
        self.motor_max_current = 8.0


        self.ambient_temperature = 25.0
        self.temperature_rise_per_amp = 5.0
        self.motor_max_temperature = 70.0

        self.rolling_resistance_coefficient = 0.02
        self.gravity = 9.81

        self.air_density = 1.225
        self.drag_coefficient = 1.0
        self.frontal_area = 0.5

        self.friction_coefficient = 0.7

        self.gear_ratio = 2.0
        self.drivetrain_efficiency = 0.9

        self.motor_max_rpm = 3000

        self.battery_voltage = 24.0
        self.battery_max_current = 20.0

        self.thermal_resistance = 2.0
        self.thermal_capacitance = 100.0
        self.motor_resistance = 0.2
        self.analysis_time = 10.0

        self.turning_radius = 2.0


class PhysicsAnalyzer:
    def __init__(self,robot):
        self.robot = robot

    
    def calculate_max_safe_payload(self,speed,slope_angle):
        maximum_safe_torque = (self.robot.motor_max_current * self.robot.motor_torque_constant)

        maximum_safe_force_per_motor = (maximum_safe_torque * self.robot.gear_ratio * self.robot.drivetrain_efficiency/ self.robot.wheel_radius)

        maximum_safe_total_force = (maximum_safe_force_per_motor * self.robot.number_of_motors)

        drag_force = (0.5 * self.robot.air_density * self.robot.drag_coefficient * self.robot.frontal_area * speed ** 2)

        force_available_for_mass = (maximum_safe_total_force - drag_force)

        mass_factor = (self.robot.acceleration + self.robot.rolling_resistance_coefficient * self.robot.gravity + self.robot.gravity * math.sin(math.radians(slope_angle)))

        lateral_acceleration = (speed ** 2 / self.robot.turning_radius)

        maximum_friction_acceleration = (self.robot.friction_coefficient * self.robot.gravity* math.cos(math.radians(slope_angle)))

        combined_mass_acceleration = math.sqrt(mass_factor ** 2 + lateral_acceleration ** 2)

        if combined_mass_acceleration >= maximum_friction_acceleration:
            return -1
        maximum_safe_total_mass = (force_available_for_mass / mass_factor)

        maximum_safe_payload = (maximum_safe_total_mass - self.robot.robot_mass)

       
        return maximum_safe_payload

    def calculate_max_cruise_payload(self,speed,slope_angle):


        maximum_safe_torque = (self.robot.motor_max_current * self.robot.motor_torque_constant)

        maximum_safe_force_per_motor = (maximum_safe_torque * self.robot.gear_ratio * self.robot.drivetrain_efficiency/ self.robot.wheel_radius)

        maximum_safe_total_force = (maximum_safe_force_per_motor * self.robot.number_of_motors)

        drag_force = (0.5 * self.robot.air_density * self.robot.drag_coefficient * self.robot.frontal_area * speed ** 2)

        force_available_for_mass = (maximum_safe_total_force - drag_force)

        mass_factor = (self.robot.rolling_resistance_coefficient * self.robot.gravity + self.robot.gravity * math.sin(math.radians(slope_angle)))

        lateral_acceleration = (speed ** 2 / self.robot.turning_radius)

        maximum_friction_acceleration = (self.robot.friction_coefficient * self.robot.gravity * math.cos(math.radians(slope_angle)))

        combined_mass_acceleration = math.sqrt(mass_factor ** 2 + lateral_acceleration ** 2)

        if combined_mass_acceleration >= maximum_friction_acceleration:
            return -1
        maximum_safe_total_mass = (force_available_for_mass / mass_factor)

        maximum_safe_payload = (maximum_safe_total_mass - self.robot.robot_mass)

        return maximum_safe_payload
    

    def analyze_scenario(self,payload,speed,slope_angle):

        total_mass = self.robot.robot_mass + payload

        rolling_force = (self.robot.rolling_resistance_coefficient * total_mass * self.robot.gravity)

        slope_force = (total_mass * self.robot.gravity * math.sin(math.radians(slope_angle)))
        
        normal_force = (total_mass * self.robot.gravity * math.cos(math.radians(slope_angle)))
        
        normal_force_per_wheel = (normal_force / self.robot.number_of_motors)
        
        maximum_traction_force_per_wheel = (self.robot.friction_coefficient * normal_force_per_wheel)
       
        maximum_total_traction_force = (maximum_traction_force_per_wheel * self.robot.number_of_motors)
    
    
        
        drag_force = (0.5 * self.robot.air_density * self.robot.drag_coefficient * self.robot.frontal_area * speed ** 2)
        
        acceleration_force = total_mass * self.robot.acceleration

        acceleration_required_force = (acceleration_force + rolling_force + drag_force + slope_force)

        lateral_force = (total_mass * speed ** 2 / self.robot.turning_radius)

        combined_traction_force = (math.sqrt(acceleration_required_force ** 2 + lateral_force ** 2))

        cruise_required_force = (rolling_force + drag_force + slope_force)
        
        acceleration_force_per_motor = (acceleration_required_force / self.robot.number_of_motors)

        cruise_force_per_motor = (cruise_required_force / self.robot.number_of_motors)

        acceleration_wheel_torque = (acceleration_force_per_motor * self.robot.wheel_radius)

        cruise_wheel_torque = (cruise_force_per_motor * self.robot.wheel_radius)

        acceleration_motor_torque = (acceleration_wheel_torque / (self.robot.gear_ratio * self.robot.drivetrain_efficiency))

        cruise_motor_torque = (cruise_wheel_torque / (self.robot.gear_ratio * self.robot.drivetrain_efficiency))

        acceleration_motor_torque = round(acceleration_motor_torque, 2)

        cruise_motor_torque = round(cruise_motor_torque, 2)

        motor_current = round(acceleration_motor_torque / self.robot.motor_torque_constant,2)

        heat_generated = ((motor_current ** 2) * self.robot.motor_resistance * self.robot.analysis_time)

        temperature_rise = (heat_generated / self.robot.thermal_capacitance)

        dynamic_motor_temperature = (self.robot.ambient_temperature + temperature_rise)

        motor_temperature = round(self.robot.ambient_temperature + motor_current * self.robot.temperature_rise_per_amp,2)

        cruise_motor_current = round(cruise_motor_torque / self.robot.motor_torque_constant,2)

        cruise_motor_temperature = round(self.robot.ambient_temperature + cruise_motor_current * self.robot.temperature_rise_per_amp,2)

        wheel_rpm = (speed / (2 * math.pi * self.robot.wheel_radius)) * 60

        motor_rpm = (wheel_rpm * self.robot.gear_ratio)

        acceleration_mechanical_power = (acceleration_required_force * speed)

        cruise_mechanical_power = (cruise_required_force * speed)

        acceleration_electrical_power = (acceleration_mechanical_power / self.robot.drivetrain_efficiency)

        cruise_electrical_power = (cruise_mechanical_power / self.robot.drivetrain_efficiency)

        acceleration_battery_current = (acceleration_electrical_power/ self.robot.battery_voltage)

        cruise_battery_current = (cruise_electrical_power/ self.robot.battery_voltage)

        if dynamic_motor_temperature <= self.robot.motor_max_temperature:
            dynamic_temperature_status = "OK"
        else:
            dynamic_temperature_status = "EXCEEDED"

        if combined_traction_force <= maximum_total_traction_force:
            traction_status = "OK"
        else:
            traction_status = "EXCEEDED"

        if (acceleration_motor_torque <= self.robot.motor_max_torque and cruise_motor_torque <= self.robot.motor_max_torque):
            motor_status = "OK"
        else:
            motor_status = "EXCEEDED"

        if (motor_current <= self.robot.motor_max_current and cruise_motor_current <= self.robot.motor_max_current):
            current_status = "OK"
        else:
            current_status = "EXCEEDED"

        if (motor_temperature <= self.robot.motor_max_temperature and cruise_motor_temperature <= self.robot.motor_max_temperature):
            temperature_status = "OK"
        else:
            temperature_status = "EXCEEDED"

        if motor_rpm <= self.robot.motor_max_rpm:
            rpm_status = "OK"
        else:
            rpm_status = "EXCEEDED"

        if (acceleration_battery_current <= self.robot.battery_max_current and cruise_battery_current <= self.robot.battery_max_current):
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
        return scenario

    def analyze_operating_envelope(self,scenarios,speeds):

        safe_payload_by_speed = {}

        for speed in speeds:

            safe_payloads = []

            for scenario in scenarios:

                if (scenario["speed"] == speed and scenario["overall_status"] == "OK"):
                    
                    safe_payloads.append(scenario["payload"])

            safe_payload_by_speed[speed] = safe_payloads


        tested_boundary_by_speed = {}

        for speed in speeds:

            safe_payloads = safe_payload_by_speed[speed]

            if safe_payloads:
                tested_boundary_by_speed[speed] = max(safe_payloads)
            else:
                tested_boundary_by_speed[speed] = None


        limiting_constraint_by_speed = {}

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

                limiting_constraint_by_speed[speed] = {
                    "payload": first_unsafe["payload"],
                    "constraint": first_unsafe["limiting_constraint"]
                }

            else:

                limiting_constraint_by_speed[speed] = None


        operating_envelope_matrix = {}

        for speed in speeds:

            row = []

            for payload in self._get_payloads_from_scenarios(
                scenarios,
                speed
            ):

                safe = False

                for scenario in scenarios:

                    if (
                        scenario["speed"] == speed
                        and scenario["payload"] == payload
                        and scenario["overall_status"] == "OK"
                    ):
                        safe = True
                        break

                row.append(safe)

            operating_envelope_matrix[speed] = row


        return {
            "safe_payload_by_speed": safe_payload_by_speed,
            "tested_boundary_by_speed": tested_boundary_by_speed,
            "limiting_constraint_by_speed": limiting_constraint_by_speed,
            "operating_envelope_matrix": operating_envelope_matrix
        }          

    def _get_payloads_from_scenarios(self, scenarios, speed):

        payloads = []

        for scenario in scenarios:

            if (
                scenario["speed"] == speed and scenario["payload"] not in payloads):
                
                payloads.append(scenario["payload"])

        return payloads
