import matplotlib.pyplot as plt


class ResultView:

    def print_results(
        self,
        analytical_payload_by_speed,
        analytical_cruise_payload_by_speed,
        safe_payload_by_speed,
        limiting_constraint_by_speed,
        speeds,
        min_payload
    ):

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
                print(
                    f"{speed:.1f} m/s: "
                    "Achievable only below tested payload range"
                )

            else:
                print(
                    f"{speed:.1f} m/s: "
                    "Achievable within tested payload range"
                )

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

    def plot_results(
        self,
        analytical_payload_by_speed,
        tested_boundary_by_speed,
        speeds
    ):

        analytical_limits = [
            analytical_payload_by_speed[speed]
            for speed in speeds
        ]

        tested_limits = [
            tested_boundary_by_speed[speed]
            for speed in speeds
        ]

        plt.figure(figsize=(8, 5))

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