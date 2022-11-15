r"""
Define your classes and create the instances that you need to expose
"""
import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from trame_simput import get_simput_manager

DEF_DIR = Path('/home/local/KHQ/will.dunklin/Desktop/work/pf_sim_2/pf_sim_2/app/definitions')

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class MyBusinessLogic:
    def __init__(self, server):
        self._server = server

        state, ctrl = server.state, server.controller

        state.update(
            {
                "dbFiles": {},
                "fileCategories": [
                    # {"value": cat.value, "text": file_category_label(cat)}
                    # for cat in FileCategories
                ],
                "uploadError": "",
                "dbSelectedFile": None,

                "currentView": "File Database",
                "views": [
                    "File Database",
                    "Simulation Type",
                    "Domain",
                    "Timing",
                    "Boundary Conditions",
                    "Subsurface Properties",
                    "Solver",
                    "Project Generation",
                ],
                #
                # **validated_args,
                # "dbFiles": entries,
                # "dbSelectedFile": None if not entries else list(entries.values())[0],
            }
        )

        ctrl.uploadFile = self.uploadFile
        ctrl.uploadLocalFile = self.uploadLocalFile
        ctrl.updateFiles = self.updateFiles

        # Simput
        self.simput_manager = get_simput_manager()

        self.pxm = self.simput_manager.proxymanager

        ctrl.get_pxm = lambda: self.pxm
        ctrl.get_simput_manager = lambda: self.simput_manager

        # add item
        self.simput_manager.load_model(yaml_file=DEF_DIR / "grid.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "grid_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "cycle.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "cycle_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "timing.yaml")

        state.gridId = self.pxm.create("ComputationalGrid").id
        state.timingId = self.pxm.create("Timing").id

    def uploadFile(self, kwargs):
        logger.info(f">>> uploadLocalFile: {kwargs}")

    def uploadLocalFile(self, entryId, fileMeta):
        logger.info(f">>> uploadLocalFile: {entryId} {fileMeta}")

    def updateFiles(self, update, entryId=None):
        logger.info(f">>> updateFiles: {update} {entryId}")

# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------


def initialize(server):
    state, ctrl = server.state, server.controller

    # @state.change("resolution")
    # def resolution_changed(resolution, **kwargs):
    #     logger.info(f">>> ENGINE(b): Slider updating resolution to {resolution}")

    def protocols_ready(**initial_state):
        logger.info(f">>> ENGINE(b): Server is ready {initial_state}")

    # ctrl.on_server_ready.add(protocols_ready)

    engine = MyBusinessLogic(server)
    return engine
