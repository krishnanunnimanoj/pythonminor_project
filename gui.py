import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from application import Application

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RobotEnvelopeGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Robot Operating Envelope Analyzer"
        )

        self.root.geometry("1000x1000")
        self.root.minsize(900,700)

        self.application = Application()
        self.create_widgets()

    def create_widgets(self):

        title = ttk.Label(
            self.root,
            text="ROBOT OPERATING ENVELOPE ANALYZER",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=20)

        # -----------------------------
        # Robot configuration
        # -----------------------------

        robot_frame = ttk.LabelFrame(
            self.root,
            text="Robot Configuration"
        )

        robot_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            robot_frame,
            text="URDF File:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.urdf_entry = ttk.Entry(
            robot_frame,
            width=45
        )

        self.urdf_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.browse_button = ttk.Button(
            robot_frame,
            text="Browse",
            command=self.browse_urdf
        )

        self.browse_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )
        # -----------------------------
        # Robot information
        # -----------------------------

        self.robot_info = ttk.Label(
            robot_frame,
            text="Robot: Not loaded"
        )

        self.robot_info.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=10,
            pady=10
        )

        # -----------------------------
        # Payload
        # -----------------------------

        payload_frame = ttk.LabelFrame(
            self.root,
            text="Payload Range"
        )

        payload_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            payload_frame,
            text="Minimum (kg):"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.min_payload = ttk.Entry(
            payload_frame,
            width=10
        )

        self.min_payload.grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Label(
            payload_frame,
            text="Maximum (kg):"
        ).grid(row=0, column=2, padx=10)

        self.max_payload = ttk.Entry(
            payload_frame,
            width=10
        )

        self.max_payload.grid(
            row=0,
            column=3,
            padx=10
        )

        ttk.Label(
            payload_frame,
            text="Step:"
        ).grid(row=0, column=4, padx=10)

        self.payload_step = ttk.Entry(
            payload_frame,
            width=10
        )

        self.payload_step.grid(
            row=0,
            column=5,
            padx=10
        )

        # -----------------------------
        # Speed
        # -----------------------------

        speed_frame = ttk.LabelFrame(
            self.root,
            text="Speed Range"
        )

        speed_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            speed_frame,
            text="Minimum (m/s):"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.min_speed = ttk.Entry(
            speed_frame,
            width=10
        )

        self.min_speed.grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Label(
            speed_frame,
            text="Maximum (m/s):"
        ).grid(row=0, column=2, padx=10)

        self.max_speed = ttk.Entry(
            speed_frame,
            width=10
        )

        self.max_speed.grid(
            row=0,
            column=3,
            padx=10
        )

        ttk.Label(
            speed_frame,
            text="Step:"
        ).grid(row=0, column=4, padx=10)

        self.speed_step = ttk.Entry(
            speed_frame,
            width=10
        )

        self.speed_step.grid(
            row=0,
            column=5,
            padx=10
        )

        # -----------------------------
        # Environment
        # -----------------------------

        environment_frame = ttk.LabelFrame(
            self.root,
            text="Environment"
        )

        environment_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            environment_frame,
            text="Slope Angle (degrees):"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.slope_angle = ttk.Entry(
            environment_frame,
            width=10
        )

        self.slope_angle.grid(
            row=0,
            column=1,
            padx=10
        )

        # -----------------------------
        # Run button
        # -----------------------------

        self.run_button = ttk.Button(
        self.root,
        text="RUN ANALYSIS",
        command=self.run_analysis
        )

        self.run_button.pack(
            pady=20
        )

        # -----------------------------
        # Results
        # -----------------------------

        results_frame = ttk.LabelFrame(
            self.root,
            text="Results"
        )

        results_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.results_text = tk.Text(
            results_frame,
            height=8,
            width=80
        )

        self.results_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
                # -----------------------------
        # Operating Envelope Graph
        # -----------------------------

        graph_frame = ttk.LabelFrame(
            self.root,
            text="Operating Envelope Graph"
        )

        graph_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.figure = Figure(
            figsize=(9, 5),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def browse_urdf(self):

        file_path = filedialog.askopenfilename(
            title="Select URDF File",
            filetypes=[
                ("URDF files", "*.urdf"),
                ("All files", "*.*")
            ]
        )

        if file_path:

            self.urdf_entry.delete(
                0,
                tk.END
            )

            self.urdf_entry.insert(
                0,
                file_path
            )

    
    def update_graph(
        self,
        analytical_limits,
        tested_limits,
        speeds
    ):

        self.ax.clear()

        analytical_values = []
        tested_values = []

        for speed in speeds:

            analytical_value = analytical_limits[speed]
            tested_value = tested_limits[speed]

            # Analytical value
            if (
                analytical_value is not None
                and analytical_value >= 0
            ):
                analytical_values.append(
                    analytical_value
                )
            else:
                analytical_values.append(None)

            # Tested value
            if (
                tested_value is not None
                and tested_value >= 0
            ):
                tested_values.append(
                    tested_value
                )
            else:
                tested_values.append(None)

        self.ax.plot(
            speeds,
            analytical_values,
            marker="o",
            label="Analytical Limit"
        )

        self.ax.plot(
            speeds,
            tested_values,
            marker="x",
            label="Tested Limit"
        )

        self.ax.set_xlabel(
            "Speed (m/s)"
        )

        self.ax.set_ylabel(
            "Maximum Safe Payload (kg)"
        )

        self.ax.set_title(
            "Robot Operating Envelope"
        )

        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

    def run_analysis(self):

        try:

            urdf_path = self.urdf_entry.get()

            min_payload = float(
                self.min_payload.get()
            )

            max_payload = float(
                self.max_payload.get()
            )

            payload_step = float(
                self.payload_step.get()
            )

            min_speed = float(
                self.min_speed.get()
            )

            max_speed = float(
                self.max_speed.get()
            )

            speed_step = float(
                self.speed_step.get()
            )

            slope_angle = float(
                self.slope_angle.get()
            )

            if not self.application.load_configuration():
                return

            if not self.application.load_robot(
                urdf_path
            ):
                return

            robot = self.application.robot

            self.robot_info.config(
                text=(
                    f"Robot mass: {robot.robot_mass:.2f} kg    "
                    f"Wheel radius: {robot.wheel_radius:.2f} m    "
                    f"Wheels: {robot.number_of_motors}"
                )
            )

            self.application.create_analyzers()

            (
                payloads,
                speeds,
                results
            ) = self.application.run_analysis(
                min_payload,
                max_payload,
                payload_step,
                min_speed,
                max_speed,
                speed_step,
                slope_angle
            )

            self.results_text.delete(
                "1.0",
                tk.END
            )

            analytical_limits = results[
                "analytical_payload_by_speed"
            ]

            cruise_limits = results[
                "analytical_cruise_payload_by_speed"
            ]

            safe_limits = results[
                "safe_payload_by_speed"
            ]

            tested_limits = results[
            "tested_boundary_by_speed"
            ]

            constraints = results[
                "limiting_constraint_by_speed"
            ]

            # --------------------------------
            # Analytical Payload Limits
            # --------------------------------

            self.results_text.insert(
                tk.END,
                "ANALYTICAL PAYLOAD LIMITS\n"
            )

            self.results_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            for speed, payload in analytical_limits.items():

                if payload < 0:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Not achievable\n"
                    )

                else:

                    text = (
                        f"{speed:.1f} m/s: "
                        f"{payload:.2f} kg\n"
                    )

                self.results_text.insert(
                    tk.END,
                    text
                )

            # --------------------------------
            # Cruise Payload Limits
            # --------------------------------

            self.results_text.insert(
                tk.END,
                "\nANALYTICAL CRUISE PAYLOAD LIMITS\n"
            )

            self.results_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            for speed, payload in cruise_limits.items():

                if payload < 0:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Not achievable\n"
                    )

                else:

                    text = (
                        f"{speed:.1f} m/s: "
                        f"{payload:.2f} kg\n"
                    )

                self.results_text.insert(
                    tk.END,
                    text
                )

            # --------------------------------
            # Speed Capability
            # --------------------------------

            self.results_text.insert(
                tk.END,
                "\nROBOT SPEED CAPABILITY\n"
            )

            self.results_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            for speed, payload in analytical_limits.items():

                if payload < 0:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Not achievable\n"
                    )

                elif payload < min_payload:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Achievable only below "
                        "tested payload range\n"
                    )

                else:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Achievable within tested "
                        "payload range\n"
                    )

                self.results_text.insert(
                    tk.END,
                    text
                )

            # --------------------------------
            # Final Operating Envelope
            # --------------------------------

            self.results_text.insert(
                tk.END,
                "\nFINAL OPERATING ENVELOPE\n"
            )

            self.results_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            for speed in speeds:

                analytical_limit = (
                    analytical_limits[speed]
                )

                if analytical_limit < 0:

                    text = (
                        f"{speed:.1f} m/s: "
                        "No operating point\n"
                    )

                elif analytical_limit < min_payload:

                    text = (
                        f"{speed:.1f} m/s: "
                        "Safe only below tested "
                        "payload range\n"
                    )

                else:

                    text = (
                        f"{speed:.1f} m/s: "
                        f"Safe up to "
                        f"{analytical_limit:.2f} kg payload\n"
                    )

                self.results_text.insert(
                    tk.END,
                    text
                )

            # --------------------------------
            # Limiting Constraint
            # --------------------------------

            self.results_text.insert(
                tk.END,
                "\nLIMITING CONSTRAINT\n"
            )

            self.results_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            for speed in speeds:

                constraint = constraints[speed]

                if constraint is None:

                    text = (
                        f"{speed:.1f} m/s: "
                        "No unsafe scenario in "
                        "tested range\n"
                    )

                else:

                    text = (
                        f"{speed:.1f} m/s: "
                        f"{constraint['constraint']}\n"
                    )

                self.results_text.insert(
                    tk.END,
                    text
                )
            self.update_graph(
                analytical_limits,
                tested_limits,
                speeds
                )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numerical values."
            )

        except Exception as error:

            messagebox.showerror(
                "Analysis Error",
                str(error)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = RobotEnvelopeGUI(root)

    root.mainloop()