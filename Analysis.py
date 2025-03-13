from FunctionFitPlot import *

from FunctionsFit import *

bead_experiment = 4.5/2 ######## we want the radius of a 4.5um bead
want_to_plot = "yes"
details_of_fit = "yes"
### Put your points and radii here, an example of imageJ macro output is given below:
data =[
[ 4.9600, 4.4800, 4.3200, 4, 3.5200],
[7.52, 7.2, 4.5],
[7.84, 7.36, 5],
[7.68, 7.2, 5.5],
[7.68, 7.2, 6],
[7.68, 7.36, 6.5]
]

bead_data = [
[0.9600, 1.1200, 1.4400, 1.4400, 0.8000],
[6.88, 6.72, 3.5],
[6.72, 6.72, 4],
[6.88, 6.72, 4.5],
[6.88, 6.72, 5],
[6.88, 6.72, 5.5]
]
Zstack = len(data)
