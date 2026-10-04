import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import signal

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
        self.gazebo_process = None
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
            text="Payload Condition:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.payload_selection = ttk.Combobox(
            robot_frame,
            values=[
                "Base Robot (0 kg)",
                "2 kg Payload",
                "5 kg Payload",
                "5.44 kg Payload",
                "6 kg Payload"
            ],
            state="readonly",
            width=30
        )

        self.payload_selection.current(0)

        self.payload_selection.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.payload_selection.bind(
            "<<ComboboxSelected>>",
            self.select_payload_urdf
        )

        ttk.Label(
            robot_frame,
            text="URDF File:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        self.urdf_entry = ttk.Entry(
            robot_frame,
            width=45
        )

        self.urdf_entry.grid(
            row=1,
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
            row=1,
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
        # Gazebo controls
        # -----------------------------

        gazebo_frame = ttk.LabelFrame(
            self.root,
            text="Gazebo Simulation"
        )

        gazebo_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.launch_gazebo_button = ttk.Button(
            gazebo_frame,
            text="LAUNCH GAZEBO",
            command=self.launch_gazebo
        )

        self.launch_gazebo_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.stop_gazebo_button = ttk.Button(
            gazebo_frame,
            text="STOP GAZEBO",
            command=self.stop_gazebo
        )

        self.stop_gazebo_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.gazebo_status = ttk.Label(
            gazebo_frame,
            text="Gazebo: Not running"
        )

        self.gazebo_status.grid(
            row=0,
            column=2,
            padx=20,
            pady=10
        )

        # Velocity test controls
        velocity_frame = ttk.LabelFrame(
            self.root,
            text="Gazebo Velocity Test"
        )
        velocity_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            velocity_frame,
            text="Target velocity (m/s):"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.velocity_entry = ttk.Entry(
            velocity_frame,
            width=10
        )
        self.velocity_entry.insert(0, "2.0")
        self.velocity_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.velocity_test_button = ttk.Button(
            velocity_frame,
            text="RUN VELOCITY TEST",
            command=self.run_velocity_test
        )
        self.velocity_test_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        self.velocity_status = ttk.Label(
            velocity_frame,
            text="Velocity test: Not started"
        )
        self.velocity_status.grid(
            row=0,
            column=3,
            padx=20,
            pady=10
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

        results_container = ttk.Frame(
            results_frame
        )

        results_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.results_text = tk.Text(
            results_container,
            height=12,
            width=80,
            wrap="none"
        )

        self.results_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        results_scrollbar = ttk.Scrollbar(
            results_container,
            orient="vertical",
            command=self.results_text.yview
        )

        results_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.results_text.config(
            yscrollcommand=results_scrollbar.set
        )
         # -----------------------------
        # Operating Envelope Graph
        # -----------------------------

        self.graph_button = ttk.Button(
            self.root,
            text="SHOW OPERATING ENVELOPE GRAPH",
            command=self.show_graph
        )

        self.graph_button.pack(
            padx=20,
            pady=10
        )


    def select_payload_urdf(self,event=None):

        payload_files = {
            "Base Robot (0 kg)": "my_robot.urdf",
            "2 kg Payload": "my_robot_2kg_payload.urdf",
            "5 kg Payload": "my_robot_5kg_payload.urdf",
            "5.44 kg Payload": "my_robot_5_44kg_payload.urdf",
            "6 kg Payload": "my_robot_6kg_payload.urdf"
        }

        selected_payload = self.payload_selection.get()

        urdf_file = payload_files[selected_payload]

        urdf_path = os.path.join(
            os.path.expanduser(
                "~/python_project/robot_envelope_analyzer"
            ),
            "robots",
            urdf_file
        )

        self.urdf_entry.delete(
            0,
            tk.END
        )

        self.urdf_entry.insert(
            0,
            urdf_path
        )
        self.robot_info.config(
            text=f"Selected: {selected_payload}"
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

        # Create graph window if it does not exist
        if (
            not hasattr(self, "graph_window")
            or not self.graph_window.winfo_exists()
        ):

            self.show_graph()

        self.graph_ax.clear()

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

        self.graph_ax.plot(
            speeds,
            analytical_values,
            marker="o",
            label="Analytical Limit"
        )

        self.graph_ax.plot(
            speeds,
            tested_values,
            marker="x",
            label="Tested Limit"
        )

        self.graph_ax.set_xlabel(
            "Speed (m/s)"
        )

        self.graph_ax.set_ylabel(
            "Maximum Safe Payload (kg)"
        )

        self.graph_ax.set_title(
            "Robot Operating Envelope"
        )

        self.graph_ax.legend()
        self.graph_ax.grid(True)

        self.graph_canvas.draw()

    def show_graph(self):

        if (
            hasattr(self, "graph_window")
            and self.graph_window.winfo_exists()
        ):
            self.graph_window.lift()
            return

        self.graph_window = tk.Toplevel(
            self.root
        )

        self.graph_window.title(
            "Operating Envelope Graph"
        )

        self.graph_window.geometry(
            "1000x700"
        )

        graph_frame = ttk.Frame(
            self.graph_window
        )

        graph_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.graph_figure = Figure(
            figsize=(10, 6),
            dpi=100
        )

        self.graph_ax = self.graph_figure.add_subplot(
            111
        )

        self.graph_canvas = FigureCanvasTkAgg(
            self.graph_figure,
            master=graph_frame
        )

        self.graph_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def run_velocity_test(self):

        if self.gazebo_process is None:
            messagebox.showerror(
                "Velocity Test",
                "Please launch Gazebo first."
            )
            return

        try:
            target_speed = float(
                self.velocity_entry.get()
            )

        except ValueError:
            messagebox.showerror(
                "Velocity Test",
                "Please enter a valid velocity."
            )
            return

        if target_speed <= 0:
            messagebox.showerror(
                "Velocity Test",
                "Velocity must be greater than 0."
            )
            return

        self.velocity_status.config(
            text=f"Velocity test: Running at {target_speed:.2f} m/s"
        )

        self.velocity_test_button.config(
            state="disabled"
        )

        command = (
            "source /opt/ros/humble/setup.bash && "
            "cd ~/python_project/robot_envelope_analyzer && "
            f"python3 ros2_nodes/velocity_test.py "
            f"--ros-args -p target_speed:={target_speed}"
        )

        ros_env = os.environ.copy()

        ros_env.pop("VIRTUAL_ENV", None)
        ros_env.pop("PYTHONHOME", None)
        ros_env.pop("PYTHONPATH", None)

        ros_env["PATH"] = (
            "/usr/bin:/bin:/opt/ros/humble/bin"
        )

        threading.Thread(
            target=self.execute_velocity_test,
            args=(command, ros_env),
            daemon=True
        ).start()
    def execute_velocity_test(self, command, ros_env):

        try:

            process = subprocess.Popen(
                ["bash", "-c", command],
                env=ros_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            output_lines = []

            for line in process.stdout:

                line = line.rstrip()

                if line:
                    output_lines.append(line)

                    print(
                        f"[Velocity Test] {line}"
                    )

            process.wait()

            output = "\n".join(output_lines)

            self.root.after(
                0,
                lambda: self.velocity_test_finished(
                    output,
                    process.returncode
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.velocity_test_finished(
                    str(error),
                    1
                )
            )
    def velocity_test_finished(self, output, returncode):

        self.velocity_test_button.config(
            state="normal"
        )

        if returncode == 0:

            self.velocity_status.config(
                text="Velocity test: Completed"
            )

            self.show_velocity_result(
            output,
            success=True
            )

        else:

            self.velocity_status.config(
                text="Velocity test: Failed"
            )

            self.show_velocity_result(
                output,
                success=False
                )

    def show_velocity_result(self,output,success=True):

        result_window = tk.Toplevel(
            self.root
        )

        result_window.title(
            "Velocity Test Result"
            if success
            else "Velocity Test Error"
        )

        result_window.geometry(
            "700x500"
        )

        result_frame = ttk.Frame(
            result_window
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        result_text = tk.Text(
            result_frame,
            wrap="none"
        )

        result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=result_text.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        result_text.config(
            yscrollcommand=scrollbar.set
        )

        result_text.insert(
            tk.END,
            output
        )

        result_text.config(
            state="disabled"
        )

        close_button = ttk.Button(
            result_window,
            text="CLOSE",
            command=result_window.destroy
        )

        close_button.pack(
            pady=(0, 10)
        )

    def launch_gazebo(self):

        if self.gazebo_process is not None:
            messagebox.showinfo(
                "Gazebo",
                "Gazebo is already running."
            )
            return

        urdf_path = self.urdf_entry.get().strip()

        if not urdf_path:
            messagebox.showerror(
                "Gazebo Error",
                "Please select a URDF file first."
            )
            return

        urdf_file = os.path.basename(urdf_path)

        try:

            command = (
                "source /opt/ros/humble/setup.bash && "
                "cd ~/python_project/robot_envelope_analyzer && "
                f"ros2 launch launch/gazebo_robot.launch.py "
                f"urdf_file:={urdf_file}"
            )
            ros_env = os.environ.copy()

            ros_env.pop("VIRTUAL_ENV", None)
            ros_env.pop("PYTHONHOME", None)
            ros_env.pop("PYTHONPATH", None)

            ros_env["PATH"] = (
                "/usr/bin:/bin:/opt/ros/humble/bin"
            )

            self.gazebo_process = subprocess.Popen(
                ["bash", "-c", command],
                env=ros_env,
                start_new_session=True
            )

            self.gazebo_status.config(
                text="Gazebo: Starting..."
            )

            self.launch_gazebo_button.config(
                state="disabled"
            )

            threading.Thread(
                target=self.activate_controller,
                daemon=True
            ).start()

        except Exception as error:

            self.gazebo_process = None

            messagebox.showerror(
                "Gazebo Error",
                str(error)
            )


    def activate_controller(self):

        import time

        time.sleep(8)

        try:

            command = (
                "source /opt/ros/humble/setup.bash && "
                "ros2 control load_controller "
                "diff_drive_controller && "
                "ros2 control set_controller_state "
                "diff_drive_controller inactive && "
                "ros2 control set_controller_state "
                "diff_drive_controller active"
            )

            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                self.root.after(
                    0,
                    lambda: self.gazebo_status.config(
                        text="Gazebo: READY - Controller Active"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.gazebo_status.config(
                        text="Gazebo: Running - Controller Error"
                    )
                )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.gazebo_status.config(
                    text="Gazebo: Controller Error"
                )
            )


    def stop_gazebo(self):

        if self.gazebo_process is None:
            return

        try:

            process_group = os.getpgid(
                self.gazebo_process.pid
            )

            # Ask the entire process group to shut down
            os.killpg(
                process_group,
                signal.SIGTERM
            )

            # Give Gazebo time to shut down
            import time
            time.sleep(2)

            # Check whether anything from the process group remains
            try:

                os.killpg(
                    process_group,
                    0
                )

                # Something is still alive → force termination
                os.killpg(
                    process_group,
                    signal.SIGKILL
                )

            except ProcessLookupError:
                pass

            self.gazebo_process = None

            self.gazebo_status.config(
                text="Gazebo: Not running"
            )

            self.launch_gazebo_button.config(
                state="normal"
            )

        except ProcessLookupError:

            self.gazebo_process = None

            self.gazebo_status.config(
                text="Gazebo: Not running"
            )

            self.launch_gazebo_button.config(
                state="normal"
            )

        except Exception as error:

            messagebox.showerror(
                "Gazebo Error",
                str(error)
            )
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