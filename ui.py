import math

import numpy
import pandas
import plotly.graph_objects as go
import streamlit

from abc_distribution import ABCDistribution

EXCEL_OPTIONS = [0, 1, 2, 3]
MAX_SIZE = 50


class UserInterface:

    def show_grid_designer():
        """
        The UI for grid designer.
        """
        streamlit.write("## Grid Design")
        streamlit.write(
            "Upload an excel sheet to start, or define the size of the grid."
        )
        streamlit.write(
            "Input 0 for empty spaces, 1 for SM obstacles (e.g., a physical "
            + "pillar), 2 for TC obstacles (e.g. bins can be stacked but cars are not "
            + "possible to pass through), or 3 for SM + TC obstacles."
        )

        col1, col2 = streamlit.columns(2)
        x_size = col1.number_input(
            label="X", min_value=1, max_value=MAX_SIZE, step=1, value=20
        )
        y_size = col2.number_input(
            label="Y", min_value=1, max_value=MAX_SIZE, step=1, value=20
        )

        grid_excel_file = streamlit.file_uploader("Upload grid excel.")
        if grid_excel_file is not None:
            grid_data = pandas.read_excel(grid_excel_file, write=None)
            if MAX_SIZE in grid_data.shape:
                streamlit.warning(
                    f"One of the dimensions exceeds the allowed size of {MAX_SIZE}.",
                    icon="⚠️",
                )

            if (
                grid_data.apply(lambda x: pandas.to_numeric(x, errors="coerce"))
                .isna()
                .any()
                .any()
            ) or (
                not grid_data.isin(EXCEL_OPTIONS).all().all()
                and not (grid_data >= 10).any().any()
            ):
                streamlit.warning(
                    "Excel grid contains blank cells or invalid inputs; changing "
                    + "these cells to 3 - SM & TC obstacles.",
                    icon="⚠️",
                )

                grid_data = grid_data.map(
                    lambda x: (
                        x if x in EXCEL_OPTIONS or (type(x) == int and x >= 10) else 3
                    )
                )

        else:
            grid_data = pandas.DataFrame(numpy.zeros((y_size, x_size)))

        grid_data = streamlit.data_editor(grid_data)
        grid_data.columns = range(grid_data.shape[1])

        if (
            not grid_data.isin(EXCEL_OPTIONS).all().all()
            and not (grid_data >= 10).any().any()
        ):
            streamlit.warning(
                "Resultant grid contains invalid inputs; changing these cells to "
                + "3 - SM & TC obstacles.",
                icon="⚠️",
            )

            grid_data = grid_data.map(
                lambda x: x if x in EXCEL_OPTIONS or x >= 10 else 3
            )

        stations = grid_data.copy()[grid_data >= 10].stack().values

        if any(i % 10 not in [0, 1, 2] for i in stations):
            streamlit.error(
                "Invalid values for stations detected; make sure the values end with 0, "
                + "1 or 2.",
                icon="❌️",
            )
            return

        # Check for duplicated stations
        unique_stations, counts = numpy.unique(
            numpy.array(stations, dtype=int), return_counts=True
        )
        duplicates = unique_stations[counts > 1]
        if len(duplicates) > 0:
            streamlit.error(
                f"Duplicated values for stations detected: {duplicates}", icon="❌️"
            )
            return

        # Check for missing drop-pair stations if any
        drop_station_ids = [(i - 1) / 10 for i in stations if i % 10 == 1]
        pick_station_ids = [(i - 2) / 10 for i in stations if i % 10 == 2]

        station_ids_with_missing_pair = list(
            set(drop_station_ids).symmetric_difference(set(pick_station_ids))
        )

        if station_ids_with_missing_pair:
            streamlit.error(
                "Values for stations with missing drop/pick pair detected; make sure "
                + "the values ended with 1 (drop stations) have to pair with the "
                + "complementary values that end with 2 (pick stations).",
                icon="❌️",
            )
            return

        discrete_colourscale = [
            [0.0, "#47b39d"],
            [0.2, "#47b39d"],
            [0.2, "#ffc153"],
            [0.4, "#ffc153"],
            [0.4, "#eb6156"],
            [0.6, "#eb6156"],
            [0.6, "#462446"],
            [0.8, "#462446"],
            [0.8, "#b05f6d"],
            [1.0, "#b05f6d"],
        ]

        grid_data[grid_data >= 10] = 4
        fig = go.Figure(
            data=go.Heatmap(
                z=grid_data.values,
                x=list(grid_data.columns),
                y=list(grid_data.index),
                colorscale=discrete_colourscale,
                colorbar=dict(
                    tickvals=EXCEL_OPTIONS + [4],
                    ticktext=[
                        "0 - Empty",
                        "1 - SM Obstacles",
                        "2 - TC Obstacles",
                        "3 - SM & TC Obstacles",
                        ">= 10 - Stations",
                    ],
                    title="Legend",
                ),
                zmin=-0.5,
                zmax=4.5,
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
                title="X",
                tickvals=list(grid_data.columns),
                scaleanchor="y",
                showgrid=False,
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

        streamlit.divider()

    def show_simulation_input():
        """
        The UI for simulation input.
        """
        streamlit.write("## Simulation Input")

        streamlit.write("#### Peak throughput")
        col1, col2 = streamlit.columns(2)
        pick_throughput = col1.number_input(
            "Pick throughput (bins/h)", min_value=1, value=1000
        )
        goods_in_throughput = col2.number_input(
            "Goods-in throughput (bins/h)", min_value=1, value=100
        )

        streamlit.write("#### Operator handling times")
        col1, col2 = streamlit.columns(2)
        pick_time = col1.number_input("Pick handling time (s)", min_value=1, value=20)
        goods_in_time = col2.number_input(
            "Goods-in handling time (s)", min_value=1, value=20
        )

        streamlit.write("### Simulation input")
        col1, col2 = streamlit.columns(2)
        z_size = col1.number_input(
            "Height of grid (bins)", min_value=3, max_value=30, value=15
        )
        number_of_skycars = col2.number_input(
            "Number of skycars", min_value=1, max_value=100, value=10
        )

        streamlit.write("### ABC categories")
        streamlit.write(
            """
            The default values assume that 
            - the top (A) 20% of the bins receive 70% of the jobs,
            - the middle (B) 30% of the bins receive 20% of the jobs, and
            - the bottom (C) 50% of the bins receive 10% of the jobs.
            """
        )
        a_default_bin_depth = max(1, math.ceil(z_size * 0.2))
        b_default_bin_depth = max(1, math.ceil(z_size * 0.3))
        c_default_bin_depth = z_size - a_default_bin_depth - b_default_bin_depth
        abc_df = pandas.DataFrame(
            {
                "category": ["Top (A)", "Middle (B)", "Bottom (C)"],
                "number_of_bin_depth": [
                    a_default_bin_depth,
                    b_default_bin_depth,
                    c_default_bin_depth,
                ],
                "percentage_of_jobs": [70, 20, 10],
            }
        )

        abc_df = streamlit.data_editor(
            abc_df,
            column_config={
                "category": "Category",
                "number_of_bin_depth": streamlit.column_config.NumberColumn(
                    "Number of bins",
                    min_value=1,
                    max_value=z_size,
                    step=1,
                ),
                "percentage_of_jobs": streamlit.column_config.NumberColumn(
                    "Percentage of jobs",
                    min_value=1,
                    max_value=100,
                    step=1,
                ),
            },
            disabled=["category"],
            hide_index=True,
        )
        abc_df["category"] = ["A", "B", "C"]

        if abc_df["number_of_bin_depth"].sum() != z_size:
            streamlit.error(
                f"Sum of number of bins is not equal to {z_size}; please amend the "
                + "values in the ABC input table."
            )
            return

        if abc_df["percentage_of_jobs"].sum() != 100:
            streamlit.error(
                f"Sum of percentage of jobs is not equal to 100; please amend the "
                + "values in the ABC input table."
            )
            return
        
        abc = ABCDistribution(abc_df=abc_df, z_size=z_size)

        streamlit.divider()