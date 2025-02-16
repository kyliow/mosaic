import numpy
import pandas


class ABCDistribution:

    def __init__(self, abc_df: pandas.DataFrame, z_size: int):
        self.abc_df = abc_df

        if self.abc_df["number_of_bin_depth"].sum() != z_size:
            raise ValueError(f"Sum of number of bins is not equal to {z_size}.")
        if self.abc_df["percentage_of_jobs"].sum() != 100:
            raise ValueError(f"Sum of percentage of jobs is not equal to 100.")

    def pdf(self) -> numpy.ndarray:
        number_of_bin_depths = self.abc_df["number_of_bin_depth"].values

        pdf_heights = (
            self.abc_df["percentage_of_jobs"] / self.abc_df["number_of_bin_depth"] / 100
        ).values

        pdf_list = (
            [pdf_heights[0]] * number_of_bin_depths[0]
            + [pdf_heights[1]] * number_of_bin_depths[1]
            + [pdf_heights[2]] * number_of_bin_depths[2]
        )

        return numpy.array(pdf_list)
