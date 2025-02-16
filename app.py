import streamlit

from ui import GridDesignerUI, SimulationInputUI
from input_creation import InputSkyCarSetup, InputZonesAndStations


def main():
    streamlit.title("Mosaic App")

    grid_designer_ui = GridDesignerUI()
    is_grid_designer_ui_success = grid_designer_ui.show()

    simulation_input_ui = SimulationInputUI()
    is_simulation_input_ui_success = simulation_input_ui.show()

    if not is_grid_designer_ui_success or not is_simulation_input_ui_success:
        return

    input_zones_and_stations = InputZonesAndStations(
        grid_data=grid_designer_ui.grid_data, simulation_input=simulation_input_ui
    )

    # input_skycar_setup = InputSkyCarSetup(
    #     number_of_skycars=simulation_input_ui.number_of_skycars, model="C"
    # )

    streamlit.json(input_zones_and_stations.to_json())


if __name__ == "__main__":
    main()
