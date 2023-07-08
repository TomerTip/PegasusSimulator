"""
| File: px4_launch_tool.py
| Author: Marcelo Jacinto (marcelo.jacinto@tecnico.ulisboa.pt)
| Description: Defines an auxiliary tool to launch the PX4 process in the background
| License: BSD-3-Clause. Copyright (c) 2023, Marcelo Jacinto. All rights reserved.
"""

# System tools used to launch the ArduPilot process in the background
import os
import tempfile
import subprocess


class BackendLaunchTool:
    """
    A class that manages the start/stop of a ardupilot process. It requires only the path to the ardupilot installation, the vehicle id and the vehicle model. 
    """

    def __init__(self, backend_dir, vehicle_id: int = 0, model_name: str = "iris"):
        """Construct the PX4LaunchTool object

        Args:
            backend_dir (str): A string with the path to the flightcontroller-backend directory
            vehicle_id (int): The ID of the vehicle. Defaults to 0.
            model (str): The vehicle model. Defaults to "iris".
        """

        # Attribute that will hold the backend process once it is running
        self.process = None

        # The vehicle id (used for the mavlink port open in the system)
        self.vehicle_id = vehicle_id

        # Configurations to whether autostart px4 (SITL) automatically or have the user launch it manually on another
        # terminal
        self.backend_dir = backend_dir
        
        # Create a temporary filesystem for px4 to write data to/from (and modify the origin rcS files)
        self.root_fs = tempfile.TemporaryDirectory()

        # Set the environement variables that let PX4 know which vehicle model to use internally
        self.environment = os.environ

        self.execute_command = []


    def launch_backend(self):
        """
        Method that will launch a px4 instance with the specified configuration
        """
        self.process = subprocess.Popen(
            self.execute_command,
            cwd=self.root_fs.name,
            shell=False,
            env=self.environment,
        )

    def kill_backend(self):
        """
        Method that will kill a px4 instance with the specified configuration
        """
        if self.process is not None:
            self.process.kill()
            self.process = None

    def __del__(self):
        """
        If the px4 process is still running when the PX4 launch tool object is whiped from memory, then make sure
        we kill the px4 instance so we don't end up with hanged px4 instances
        """

        # Make sure the PX4 process gets killed
        if self.process:
            self.kill_backend()

        # Make sure we clean the temporary filesystem used for the simulation
        self.root_fs.cleanup()