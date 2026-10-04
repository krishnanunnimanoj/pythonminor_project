# Robot Operating Envelope Analyzer

A Python-based robotics engineering tool for analyzing the safe operating envelope of a mobile robot under different payload, speed, and environmental conditions.

The project combines analytical physics-based calculations with ROS 2 and Gazebo simulation to study how payload and speed affect robot performance.

## Project Overview

The Robot Operating Envelope Analyzer determines whether a mobile robot can safely operate under specified conditions.

The analyzer considers:

* Robot mass and payload
* Vehicle speed
* Acceleration
* Wheel radius
* Number of drive motors
* Motor torque and current limits
* Gear ratio and drivetrain efficiency
* Rolling resistance
* Aerodynamic drag
* Ground traction
* Slope angle
* Turning radius
* Thermal limits
* Battery current limits

For each operating condition, the analyzer determines whether the robot is operating within its defined limits and identifies the limiting constraint.

## Key Features

### Analytical Operating Envelope

The analyzer evaluates combinations of:

* Payload
* Speed
* Slope angle

It calculates the maximum safe payload for each speed and identifies conditions where the robot cannot operate safely.

### Multiple Constraints

The analysis considers several engineering constraints, including:

* Motor current
* Motor torque
* Wheel traction
* Motor temperature
* Battery current
* Motor speed

### Cruise Analysis

The project separately evaluates constant-speed/cruise requirements in addition to acceleration requirements.

### URDF-Based Robot Model

Robot geometry and mass properties are represented using URDF.

The current test robot contains:

* 1 chassis
* 4 drive wheels
* 4 continuous wheel joints
* 4 kg total wheel mass
* 10 kg chassis mass
* 14 kg total base robot mass
* 0.10 m wheel radius

Payload is represented using separate URDF variants for simulation testing.

### ROS 2 and Gazebo Integration

The project includes a ROS 2 launch workflow for loading the robot into Gazebo Classic.

The simulation uses:

* ROS 2 Humble
* Gazebo Classic
* `gazebo_ros2_control`
* `diff_drive_controller`

### Velocity Validation

A ROS 2 velocity test node commands a target velocity and measures the simulated velocity through odometry.

The test reports:

* Target velocity
* Measured velocity
* Time required to reach 99% of the target
* Final measured velocity

### Graphical User Interface

The project includes a Tkinter GUI for:

* Loading a URDF
* Running the operating-envelope analysis
* Viewing analytical and tested limits
* Launching Gazebo
* Stopping Gazebo
* Running velocity tests
* Viewing velocity-test output
* Displaying the operating-envelope graph

## Project Structure

```text
robot_envelope_analyzer/
│
├── analyzer.py
├── application.py
├── config_loader.py
├── main.py
├── operating_envelope.py
├── result_view.py
├── robot_loader.py
├── urdf_parser.py
├── gui.py
│
├── configs/
│   ├── robot.yaml
│   └── controllers.yaml
│
├── robots/
│   ├── my_robot.urdf
│   ├── my_robot_2kg_payload.urdf
│   ├── my_robot_5kg_payload.urdf
│   ├── my_robot_5_44kg_payload.urdf
│   └── my_robot_6kg_payload.urdf
│
├── launch/
│   └── gazebo_robot.launch.py
│
├── ros2_nodes/
│   └── velocity_test.py
│
└── README.md
```

## Physics Model

The analyzer calculates the forces required to move the robot under different conditions.

The main force components include:

### Acceleration Force

```text
F_acceleration = m × a
```

### Rolling Resistance

```text
F_rolling = Crr × m × g
```

### Aerodynamic Drag

```text
F_drag = 0.5 × ρ × Cd × A × v²
```

### Slope Force

```text
F_slope = m × g × sin(θ)
```

### Lateral Force

For turning conditions:

```text
a_lateral = v² / R
```

The analyzer combines the longitudinal and lateral requirements when evaluating the available traction.

Motor torque, gear ratio, drivetrain efficiency, wheel radius, motor current and other constraints are then used to determine the safe operating region.

## Example Analytical Result

For the current 14 kg base robot, with a 10° slope and the configured motor and drivetrain parameters:

| Speed | Maximum Safe Payload |
| ----: | -------------------: |
| 2 m/s |              5.44 kg |
| 3 m/s |              4.91 kg |
| 4 m/s |       Not achievable |
| 5 m/s |       Not achievable |
| 6 m/s |       Not achievable |
| 7 m/s |       Not achievable |

The corresponding limiting constraints for the tested speeds are also reported by the analyzer.

These values are analytical results produced by the configured physics model and should not be interpreted as experimentally measured motor limits.

## Gazebo Validation

Gazebo is used to validate the simulation-side behavior of the robot.

The current workflow verifies:

* URDF loading
* Robot spawning
* Robot mass/payload integration
* Wheel configuration
* ROS 2 control integration
* Differential-drive controller operation
* Commanded velocity
* Measured simulated velocity
* Process cleanup

For example, a clean simulation test of the 14 kg robot at 2.0 m/s produced:

```text
Final measured velocity: 2.000 m/s
```

The velocity test also measures the time required to reach 99% of the commanded velocity.

## Important Validation Limitation

The current Gazebo controller does not automatically enforce the same motor torque and current limits used by the analytical model.

Therefore, Gazebo can successfully command a velocity at a payload that the analytical model considers unsafe.

This is expected.

The analytical analyzer answers:

> "According to the configured physical and motor limits, is this operating condition safe?"

Gazebo currently answers:

> "Can the simulated robot model and controller achieve the commanded motion?"

Therefore, Gazebo validation should currently be considered simulation and integration validation rather than direct experimental validation of the analytical motor-limit boundary.

## Configuration

Robot and system parameters are stored in:

```text
configs/robot.yaml
```

The ROS 2 controller configuration is stored in:

```text
configs/controllers.yaml
```

This separation allows robot and controller parameters to be changed without modifying the main analysis logic.

## Running the Analyzer

Activate the Python virtual environment:

```bash
source venv/bin/activate
```

Run the command-line analyzer:

```bash
python main.py
```

The program asks for:

* Payload range
* Speed range
* Payload step
* Speed step
* Slope angle

It then produces the analytical operating envelope and limiting constraints.

## Running the GUI

With the virtual environment active:

```bash
python gui.py
```

The GUI provides access to the analyzer, operating-envelope graph, Gazebo simulation controls and velocity testing.

## Running Gazebo

ROS 2 and Gazebo use the system ROS environment rather than the project virtual environment.

The launch file can be started with:

```bash
ros2 launch launch/gazebo_robot.launch.py
```

A payload-specific URDF can be selected with:

```bash
ros2 launch launch/gazebo_robot.launch.py \
    urdf_file:=my_robot_5kg_payload.urdf
```

After Gazebo starts, the differential-drive controller is loaded and activated.

## Velocity Test

The velocity test node can be run with:

```bash
python3 ros2_nodes/velocity_test.py \
    --ros-args -p target_speed:=2.0
```

The node publishes a velocity command and monitors the robot odometry.

## Current Technology Stack

* Python
* NumPy
* Matplotlib
* Tkinter
* YAML
* URDF
* ROS 2 Humble
* Gazebo Classic
* `gazebo_ros`
* `gazebo_ros2_control`
* `diff_drive_controller`
* Git / GitHub

## Current Status

The current implementation includes:

* Analytical operating-envelope calculation
* Payload and speed analysis
* Cruise analysis
* Constraint identification
* URDF loading
* GUI visualization
* Operating-envelope graph
* ROS 2 integration
* Gazebo simulation
* Differential-drive control
* Automated velocity testing
* Gazebo process management
* GitHub version control

The core analyzer and ROS/Gazebo workflow have been tested successfully.

## Future Improvements

Potential future improvements include:

* Separating acceleration-phase and constant-speed-phase models more explicitly
* Applying analytical motor torque/current limits directly to the Gazebo simulation
* Adding more detailed motor dynamics
* Adding configurable wheel-ground friction models
* Automated payload sweep testing in Gazebo
* Automated comparison between analytical and simulation results
* Improved URDF/configuration validation
* Additional ROS 2 analysis nodes
* Automated report generation
* Experimental validation using a physical robot

## Project Goal

The long-term goal is to develop a reusable engineering tool that can estimate a mobile robot's safe operating envelope before physical testing and provide a bridge between analytical calculations, robot description files, and ROS 2/Gazebo simulation.
