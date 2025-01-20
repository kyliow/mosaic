import numpy 
from matplotlib import pyplot 

pareto = numpy.random.pareto(1, 100)

f, ax = pyplot.subplots()
ax.hist(pareto, bins=50)
pyplot.show()
