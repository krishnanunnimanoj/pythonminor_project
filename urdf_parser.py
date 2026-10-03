import xml.etree.ElementTree as ET


class URDFParser:

    def __init__(self, urdf_path):

        self.urdf_path = urdf_path

        try:
            self.tree = ET.parse(urdf_path)
            self.root = self.tree.getroot()

        except ET.ParseError as error:
            raise ValueError(
                f"Invalid URDF XML: {error}"
            )
    def get_total_mass(self):

        total_mass = 0.0

        for link in self.root.findall("link"):

            inertial = link.find("inertial")

            if inertial is not None:

                mass = inertial.find("mass")

                if mass is not None:
                    total_mass += float(mass.get("value"))

        return total_mass

    def get_wheel_radius(self):

        for link in self.root.findall("link"):

            if "wheel" in link.get("name", ""):

                collision = link.find("collision")

                if collision is not None:

                    geometry = collision.find("geometry")

                    if geometry is not None:

                        cylinder = geometry.find("cylinder")

                        if cylinder is not None:
                            return float(cylinder.get("radius"))

        return None

    def get_robot_parameters(self):

        robot_mass = self.get_total_mass()
        wheel_radius = self.get_wheel_radius()

        if robot_mass <= 0:
            raise ValueError("Robot mass must be greater than zero.")

        if wheel_radius is None or wheel_radius <= 0:
            raise ValueError("Valid wheel radius not found in URDF.")

        return {
            "robot_mass": robot_mass,
            "wheel_radius": wheel_radius
        }