import numpy
from matplotlib import pyplot


class Pareto:
    """
    Class related to Pareto distribution.

    Parameters
    ----------
    p : float, optional
        The probability that contributes to q=1-p outcome. For example, the standard
        80:20 rule implies that p = 0.8. By default 0.8.
    """

    def __init__(self, p: float = 0.8):
        # p must strictly be more than 0.5 as p=0.5 is asymptote to pareto index function
        if not 0.5 < p < 1:
            raise ValueError(f"{p=}; must be 0.5 < p < 1.")

        self.p = p
        self.q = 1 - p
        self.index = self._pareto_index()

    def _pareto_index(self) -> float:
        """
        Return the index of the Pareto distribution based on the proportion of p to q.

        Returns
        -------
        float
            The Pareto index
        """
        return numpy.log(self.q) / numpy.log(self.q / self.p)

    def pdf(self, x: float) -> float:
        """
        Pareto distribution probability density function (PDF).

        Parameters
        ----------
        x : float
            Input to the PDF

        Returns
        -------
        float
            Value of Pareto distribution PDF
        """
        return self.index / x ** (self.index + 1)

    def generate_truncated_pareto_distribution(
        self, depth: int, size: int = 100
    ) -> numpy.ndarray:
        """
        Generate an array of values sampled from truncated Pareto distribution.

        Parameters
        ----------
        depth : int
            The depth of the grid, also the higher end truncation of Pareto distribution
        size : int, optional
            The size of the array, by default 100

        Returns
        -------
        numpy.ndarray
            An array of values sampled from truncated Pareto distribution.
        """

        k = 0
        truncated_pareto_distribution = []
        while k < size:
            sample_value = int(numpy.random.pareto(a=self.index) + 1)
            if sample_value <= depth:
                truncated_pareto_distribution.append(sample_value)
                k += 1

        return numpy.array(truncated_pareto_distribution)


if __name__ == "__main__":
    pareto = Pareto(p=0.9)

    depth = 15
    pareto_list = pareto.generate_truncated_pareto_distribution(depth, size=10000)

    fig, ax = pyplot.subplots()
    ax.hist(pareto_list, bins=depth, density=True)
    x_range = numpy.linspace(1, depth, 100)
    f_range = [pareto.pdf(x) for x in x_range]
    ax.plot(x_range, f_range)
    ax.axis(xmax=depth, xmin=1)
    pyplot.show()
