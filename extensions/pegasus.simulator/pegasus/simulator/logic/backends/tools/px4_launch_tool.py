"""
| File: px4_launch_tool.py
| Author: Marcelo Jacinto (marcelo.jacinto@tecnico.ulisboa.pt)
| Description: Defines an auxiliary tool to launch the PX4 process in the background
| License: BSD-3-Clause. Copyright (c) 2023, Marcelo Jacinto. All rights reserved.
"""
from pegasus.simulator.logic.backends.tools.px4_launch_tool import BackendLaunchTool

class PX4LaunchTool(BackendLaunchTool):
    """
    A class that manages the start/stop of a px4 process. It requires only the path to the PX4 installation (assuming that
    PX4 was already built with 'make px4_sitl_default none'), the vehicle id and the vehicle model. 
    """

    def __init__(self, backend_dir, vehicle_id: int = 0, model_name: str = "iris"):
        """Construct the PX4LaunchTool object

        Args:
            px4_dir (str): A string with the path to the PX4-Autopilot directory
            vehicle_id (int): The ID of the vehicle. Defaults to 0.
            px4_model (str): The vehicle model. Defaults to "iris".
        """

        super().__init__(backend_dir, vehicle_id, model_name)

        # Configurations to whether autostart px4 (SITL) automatically or have the user launch it manually on another
        # terminal
        self.rc_script = self.backend_dir + "/ROMFS/px4fmu_common/init.d-posix/rcS"

        self.environment["PX4_SIM_MODEL"] = model_name

        self.execute_command = [
                self.backend_dir + "/build/px4_sitl_default/bin/px4",
                self.backend_dir + "/ROMFS/px4fmu_common/",
                "-s",
                self.rc_script,
                "-i",
                str(self.vehicle_id),
                "-d",
        ]