import os
import yaml


class ConfigLoader:

    def __init__(self, config_path):

        self.config_path = config_path

    def load(self):

        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:

            with open(self.config_path, "r") as file:
                config = yaml.safe_load(file)

            return config

        except yaml.YAMLError as error:

            raise ValueError(
                f"Configuration error: {error}"
            )