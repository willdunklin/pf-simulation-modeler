from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput, html
from pf_sim_2.widgets import pf_sim_2 as pf_widgets
from . import ui_elements as ui


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "pf_sim_2"

    # Initialize UI components
    domain = ui.Domain(server)
    timing = ui.Timing(server)
    boundary_conditions = ui.BoundaryConditions(server)

    simput_widget = simput.Simput(ctrl.get_simput_manager(), trame_server=server)
    ctrl.simput_apply = simput_widget.apply
    ctrl.simput_reset = simput_widget.reset
    simput_widget.reload_domain()

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("PF Migration Test")
        layout.root = simput_widget

        with layout.toolbar:
            vuetify.VSpacer()
            pf_widgets.NavigationDropDown(v_model="currentView", views=("views",))
            vuetify.VSpacer()
            vuetify.VBtn("Save", click=ctrl.simput_apply)

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True):
                pf_widgets.FileDatabase(
                    v_if="currentView === 'File Database'",
                    files=("dbFiles",),
                    fileCategories=("fileCategories",),
                    error=("uploadError",),
                    db_update="updateFiles",
                    v_model="dbSelectedFile",
                    uploadFile=(ctrl.uploadFile, "[$event]"),
                    uploadLocalFile=ctrl.uploadLocalFile,
                    updateFiles=ctrl.updateFiles,
                )
                pf_widgets.SimulationType(
                    v_if="currentView === 'Simulation Type'",
                    shortcuts=(
                        "simTypeShortcuts",
                        {
                            "wells": False,
                            "climate": True,
                            "contaminants": False,
                            "saturated": "Variably Saturated",
                        },
                    ),
                )

            with html.Div(v_if="currentView === 'Domain'"):
                domain.page()

            with html.Div(v_if="currentView === 'Timing'"):
                timing.page()

            with html.Div(v_if="currentView === 'Boundary Conditions'"):
                boundary_conditions.page()
