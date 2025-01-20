import streamlit

from ui import UserInterface


def main():
    streamlit.title("Mosaic App")

    UserInterface.show_grid_designer()

    # UserInterface.show_simulation_input()


if __name__ == "__main__":
    main()
