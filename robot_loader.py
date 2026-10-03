import os

from analyzer import RobotParameters
from urdf_parser import URDFParser


class RobotLoader:

    def __init__(self, urdf_path, config):

        self.urdf_path = urdf_path
        self.config = config

    def load(self):

        if not os.path.isfile(self.urdf_path):
            raise FileNotFoundError(
                f"URDF file not found: {self.urdf_path}"
            )

        try:

            parser = URDFParser(self.urdf_path)

            robot_data = parser.get_robot_parameters()

            robot = RobotParameters(
                robot_mass=robot_data["robot_mass"],
                wheel_radius=robot_data["wheel_radius"],
                config=self.config
            )

            robot.number_of_motors = robot_data["wheel_count"]

            return robot

        except ValueError as error:

            raise ValueError(f"URDF error: {error}")