class OperatingEnvelopeAnalyzer:

    def __init__(self, physics_analyzer):

        self.physics_analyzer = physics_analyzer

    def calculate(self, payloads, speeds, slope_angle):

        analytical_payload_by_speed = {}

        for speed in speeds:

            maximum_payload = (
                self.physics_analyzer.calculate_max_safe_payload(
                    speed,
                    slope_angle
                )
            )

            analytical_payload_by_speed[speed] = maximum_payload

        analytical_cruise_payload_by_speed = {}

        for speed in speeds:

            maximum_payload = (
                self.physics_analyzer.calculate_max_cruise_payload(
                    speed,
                    slope_angle
                )
            )

            analytical_cruise_payload_by_speed[speed] = maximum_payload

        scenarios = []

        for payload in payloads:

            for speed in speeds:

                scenario = self.physics_analyzer.analyze_scenario(
                    payload,
                    speed,
                    slope_angle
                )

                scenarios.append(scenario)

        results = self.physics_analyzer.analyze_operating_envelope(
            scenarios,
            speeds
        )

        return {
            "analytical_payload_by_speed":
                analytical_payload_by_speed,

            "analytical_cruise_payload_by_speed":
                analytical_cruise_payload_by_speed,

            "safe_payload_by_speed":
                results["safe_payload_by_speed"],

            "tested_boundary_by_speed":
                results["tested_boundary_by_speed"],

            "limiting_constraint_by_speed":
                results["limiting_constraint_by_speed"],

            "operating_envelope_matrix":
                results["operating_envelope_matrix"]
        }