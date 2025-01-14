from matplotlib.pyplot import grid
import numpy
import pandas
import plotly.graph_objects as go
import streamlit

EXCEL_OPTIONS = [0, 1, 2, 3]
MAX_SIZE = 50

def main():
    streamlit.title("Mosaic App")

    streamlit.header("Grid Design")
    streamlit.text("Upload an excel sheet to start, or define the size of the grid.")
    col1, col2 = streamlit.columns(2)
    x_size = col1.number_input(label="X", min_value=1, max_value=MAX_SIZE, step=1, value=20)
    y_size = col2.number_input(label="Y", min_value=1, max_value=MAX_SIZE, step=1, value=20)

    grid_excel_file = streamlit.file_uploader("Upload grid excel")
    if grid_excel_file is not None:
        grid_data = pandas.read_excel(grid_excel_file, header=None)
        if MAX_SIZE in grid_data.shape:
            streamlit.warning(
                f"One of the dimensions exceeds the allowed size of {MAX_SIZE}."
                icon="⚠️",
            )

        if not grid_data.isin(EXCEL_OPTIONS).all().all():
            streamlit.warning(
                "Excel grid contains blank cells or numbers not in "
                + f"{EXCEL_OPTIONS}; changing these cells to 3 - SM & TC obstacles.",
                icon="⚠️",
            )

            grid_data = grid_data.map(lambda x: x if x in EXCEL_OPTIONS else 3)

    else:
        grid_data = pandas.DataFrame(numpy.zeros((y_size, x_size)))

    grid_data = streamlit.data_editor(grid_data)
    grid_data.columns = range(grid_data.shape[1])

    if not grid_data.isin(EXCEL_OPTIONS).all().all():
        streamlit.warning(
            "Resultant grid contains numbers not in "
            + f"{EXCEL_OPTIONS}; changing these cells to 3 - SM & TC obstacles.",
            icon="⚠️",
        )

        grid_data = grid_data.map(lambda x: x if x in EXCEL_OPTIONS else 3)

    discrete_colourscale = [
        [0.0, "#47b39d"],
        [0.25, "#47b39d"],
        [0.25, "#ffc153"],
        [0.5, "#ffc153"],
        [0.5, "#eb6156"],
        [0.75, "#eb6156"],
        [0.75, "#462446"],
        [1.0, "#462446"],
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=grid_data.values,
            x=list(grid_data.columns),
            y=list(grid_data.index),
            colorscale=discrete_colourscale,
            colorbar=dict(
                tickvals=EXCEL_OPTIONS,
                ticktext=[
                    "0 - Empty",
                    "1 - SM Obstacles",
                    "2 - TC Obstacles",
                    "3 - SM & TC Obstacles",
                ],
                title="Legend",
            ),
            zmin=-0.5,
            zmax=3.5,
        )
    )

    for col in range(grid_data.shape[1] + 1):
        fig.add_shape(
            type="line",
            x0=col - 0.5,
            x1=col - 0.5,
            y0=-0.5,
            y1=grid_data.shape[0] - 0.5,
            line=dict(color="gray", width=1),
        )

    for row in range(grid_data.shape[0] + 1):
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=grid_data.shape[1] - 0.5,
            y0=row - 0.5,
            y1=row - 0.5,
            line=dict(color="gray", width=1),
        )

    fig.update_layout(
        title="Grid Layout",
        xaxis=dict(
            title="X", tickvals=list(grid_data.columns), scaleanchor="y", showgrid=False
        ),
        yaxis=dict(
            title="Y",
            tickvals=list(grid_data.index),
            autorange="reversed",
            scaleanchor="x",
            showgrid=False,
        ),
    )

    streamlit.plotly_chart(fig)


if __name__ == "__main__":
    main()
