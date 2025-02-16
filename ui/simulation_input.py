import math

from numpy import number
import pandas
import streamlit

from abc_distribution import ABCDistribution


class SimulationInputUI:
    """
    The UI for simulation input.
    """

    def __init__(self):
        pass

    def show(self):
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

        streamlit.write("#### Station capacity")
        col1, col2 = streamlit.columns(2)
        pick_capacity = col1.number_input("Pick capacity (bins)", min_value=1, value=1)
        drop_capacity = col2.number_input("Drop capacity (bins)", min_value=1, value=2)

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
            return False

        if abc_df["percentage_of_jobs"].sum() != 100:
            streamlit.error(
                f"Sum of percentage of jobs is not equal to 100; please amend the "
                + "values in the ABC input table."
            )
            return False

        # TODO: Fix ABC to suit job creation
        abc = ABCDistribution(abc_df=abc_df, z_size=z_size)

        # Assign values for later use
        self.pick_throughput = pick_throughput
        self.goods_in_throughput = goods_in_throughput
        self.pick_time = pick_time
        self.goods_in_time = goods_in_time
        self.z_size = z_size
        self.number_of_skycars = number_of_skycars
        self.pick_capacity = pick_capacity
        self.drop_capacity = drop_capacity

        streamlit.divider()

        return True
