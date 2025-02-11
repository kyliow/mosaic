import streamlit

from ui import GridDesignerUI, SimulationInputUI
from input_creation import InputSkyCarSetup


def main():
    streamlit.title("Mosaic App")

    grid_designer_ui = GridDesignerUI()
    simulation_input_ui = SimulationInputUI()

    input_skycar_setup = InputSkyCarSetup(
        number_of_skycars=simulation_input_ui.number_of_skycars, model="C"
    )

    streamlit.write(input_skycar_setup.to_json())


if __name__ == "__main__":
    main()
